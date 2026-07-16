#!/usr/bin/env python3
"""
QB Health Check — Marine Intelligence Weekly
Scans all QB HTML files (via qb_content_index.json manifest) on GitHub,
runs structural/regulatory-safety checks, and emails a daily report via Brevo SMTP.

Run locally:
    QB_ALWAYS_EMAIL=1 python3 qb_health_check.py

Run in GitHub Actions: see .github/workflows/qb-health-check.yml
"""

import os
import re
import json
import smtplib
import ssl
import sys
import tarfile
import io
import urllib.request
from email.mime.text import MIMEText
from datetime import datetime, timezone

# ---------- Config ----------
GITHUB_REPO = "nickmarineengr-aiLiterate/marine-intelligence-weekly"
GITHUB_BRANCH = "main"
QB_FOLDER_PREFIX = "meoclass1/"          # folder inside repo where QB html + manifest live
MANIFEST_NAME = "qb_content_index.json"
GA4_TAG = "G-0YEE2CBNP5"
KNOWN_TRAPS_PATH = "known_traps.md"   # relative to QB_FOLDER_PREFIX, e.g. meoclass1/known_traps.md

VOID_ELEMENTS = {"br", "img", "meta", "link", "hr", "input", "area", "base",
                  "col", "embed", "source", "track", "wbr"}

MANDATORY_CLASSES = ["q-card", "reg-box", "ce-tip", "q-footer"]

EMAIL_TO = os.environ.get("QB_HEALTH_EMAIL_TO", "contactus@marineintelligenceweekly.com")
SMTP_LOGIN = os.environ.get("BREVO_SMTP_LOGIN", "")  # auth credential only — NOT a valid From address
EMAIL_FROM = os.environ.get("BREVO_SENDER_EMAIL", "contactus@marineintelligenceweekly.com")  # verified sender in Brevo
SMTP_HOST = "smtp-relay.brevo.com"
SMTP_PORT = 587


# ---------- Fetch repo snapshot ----------
def fetch_repo_tarball():
    """Download the repo tarball via codeload.github.com and return a dict
    of {relative_path: bytes} for everything under QB_FOLDER_PREFIX."""
    url = f"https://codeload.github.com/{GITHUB_REPO}/tar.gz/refs/heads/{GITHUB_BRANCH}"
    req = urllib.request.Request(url, headers={"User-Agent": "qb-health-check"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()

    files = {}
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:gz") as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue
            # strip the leading "<repo>-<branch>/" component
            parts = member.name.split("/", 1)
            if len(parts) != 2:
                continue
            rel_path = parts[1]
            if not rel_path.startswith(QB_FOLDER_PREFIX):
                continue
            f = tar.extractfile(member)
            if f is None:
                continue
            files[rel_path[len(QB_FOLDER_PREFIX):]] = f.read()
    return files


# ---------- Individual checks ----------
def check_tag_balance(html_text, filename):
    """Stack-based unclosed-tag checker, excluding void elements and script/style contents."""
    errors = []
    # strip script/style bodies (they can contain angle brackets that aren't HTML tags)
    cleaned = re.sub(r"<script.*?</script>", "", html_text, flags=re.S | re.I)
    cleaned = re.sub(r"<style.*?</style>", "", cleaned, flags=re.S | re.I)
    cleaned = re.sub(r"<!--.*?-->", "", cleaned, flags=re.S)

    tag_re = re.compile(r"<(/?)([a-zA-Z][a-zA-Z0-9]*)\b[^>]*?(/?)>")
    stack = []
    for m in tag_re.finditer(cleaned):
        closing, tag, self_close = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID_ELEMENTS or self_close == "/":
            continue
        if not closing:
            stack.append(tag)
        else:
            if stack and stack[-1] == tag:
                stack.pop()
            elif tag in stack:
                # pop until match — flag the skipped tags as likely unclosed
                while stack and stack[-1] != tag:
                    errors.append(f"Unclosed <{stack.pop()}> (closed out of order before </{tag}>)")
                if stack:
                    stack.pop()
            else:
                errors.append(f"Stray closing tag </{tag}> with no matching open tag")
    for leftover in stack:
        errors.append(f"Unclosed <{leftover}>")
    return errors


def _count_exact_class(html_text, cls):
    """Count elements whose class attribute contains cls as a whole token
    (space-separated), not as a substring of a longer class like 'reg-box-title'."""
    count = 0
    for m in re.finditer(r'class="([^"]*)"', html_text):
        if cls in m.group(1).split():
            count += 1
    return count


def check_mandatory_block_counts(html_text):
    """Verify each real question card (id="qN", numeric) contains exactly one
    reg-box, one ce-tip, and one q-footer. Special non-numeric-id cards (map/
    summary cards, inline cheat-sheet blocks reusing the q-card class) are
    intentionally excluded from this requirement."""
    errors = []
    card_starts = [(m.start(), m.group(1)) for m in
                   re.finditer(r'<div class="q-card(?:\s[^"]*)?"[^>]*\bid="(q\d+)"', html_text)]
    all_card_tags = list(re.finditer(r'<div class="q-card(?:\s[^"]*)?"', html_text))
    card_starts_sorted = sorted(card_starts, key=lambda x: x[0])
    boundaries = [s for s, _ in card_starts_sorted] + [len(html_text)]

    for i, (start, qid) in enumerate(card_starts_sorted):
        end = boundaries[i + 1]
        block = html_text[start:end]
        reg = block.count('"reg-box"')
        tip = block.count('"ce-tip"')
        foot = block.count('"q-footer"')
        missing = []
        if reg < 1:
            missing.append("reg-box")
        if tip < 1:
            missing.append("ce-tip")
        if foot < 1:
            missing.append("q-footer")
        if missing:
            errors.append(f"{qid}: missing {', '.join(missing)}")

    q_count = len(card_starts_sorted)
    if q_count == 0:
        errors.append("No numbered q-card elements found — file may be empty or malformed")
    return errors, q_count


def check_ga4_tag(html_text):
    return [] if GA4_TAG in html_text else [f"Missing GA4 tag ({GA4_TAG})"]


def check_robots_meta(html_text):
    if re.search(r'<meta[^>]+name="robots"[^>]+content="[^"]*noindex[^"]*"', html_text, re.I):
        return []
    return ["Missing or incorrect robots noindex meta tag"]


def check_q_id_sequence(html_text):
    """Ids should be sequential with no internal gaps or dupes. Some companion
    files (e.g. QB1_G continuing from QB1_F) legitimately start above q1, so
    gaps are checked relative to the file's own min/max, not an assumed start of 1."""
    errors = []
    ids = re.findall(r'<div class="q-card"[^>]*\bid="q(\d+)"', html_text)
    nums = [int(x) for x in ids]
    if not nums:
        return errors
    seen = set()
    dupes = set()
    for n in nums:
        if n in seen:
            dupes.add(n)
        seen.add(n)
    if dupes:
        errors.append(f"Duplicate q-card id(s): {sorted(dupes)}")
    expected = set(range(min(nums), max(nums) + 1))
    missing = expected - seen
    if missing:
        errors.append(f"Gap(s) in q-card numbering — missing id(s): {sorted(missing)}")
    return errors


def check_toc_anchors(html_text):
    """Every TOC anchor must have a matching id="qN" q-card, and vice versa (best effort).
    Attribute order (class before/after href) is not assumed."""
    errors = []
    toc_hrefs = set()
    for m in re.finditer(r'<a\b[^>]*>', html_text):
        tag = m.group(0)
        if re.search(r'class="[^"]*\btoc-link\b[^"]*"', tag):
            href_m = re.search(r'href="#(q\d+)"', tag)
            if href_m:
                toc_hrefs.add(href_m.group(1))
    card_ids = set(re.findall(r'<div class="q-card"[^>]*\bid="(q\d+)"', html_text))
    broken = toc_hrefs - card_ids
    orphan = card_ids - toc_hrefs
    if broken:
        errors.append(f"TOC link(s) point to non-existent card id(s): {sorted(broken)}")
    if orphan:
        errors.append(f"Card id(s) with no TOC entry: {sorted(orphan)}")
    return errors


def check_formula_rendering(html_text):
    """Flag raw/unrendered LaTeX left in answer text. The site has no MathJax/KaTeX
    pipeline, so any LaTeX-style markup that leaks into visible HTML (practice-block,
    answer-body, deep-dive-body, ce-tip) renders as literal backslashes and braces to
    the reader instead of a formula. Formulas must instead be either:
      - plain HTML/Unicode (e.g. 'GM<sub>0</sub>', '√', '≈', '×'), or
      - wrapped in <p class="formula">...</p> using plain text/Unicode only.
    This check does not touch <script>/<style> contents."""
    errors = []

    cleaned = re.sub(r"<script.*?</script>", "", html_text, flags=re.S | re.I)
    cleaned = re.sub(r"<style.*?</style>", "", cleaned, flags=re.S | re.I)

    # Patterns indicating unrendered LaTeX leaking into visible markup
    latex_command_re = re.compile(r'\\(?:frac|sqrt|times|rightarrow|Delta|theta|approx|ge|le|text|pm|cdot|div|circ)\b')
    # Only flag $...$ as unrendered LaTeX if it contains actual math markup
    # (backslash command, ^, _, {}) — plain currency like "$10m ... $100m" is
    # not LaTeX and must not be flagged just because two $ signs appear nearby.
    dollar_math_re = re.compile(r'\$[^$\n]{0,80}?[\\^_{}][^$\n]{0,80}?\$')
    subscript_brace_re = re.compile(r'[A-Za-z]_\{[^}]+\}')          # e.g. GM_{0}
    subscript_plain_re = re.compile(r'\b[A-Za-z]{1,4}_[0-9A-Za-z]{1,10}\b')  # e.g. GM_0, X_max — best-effort

    latex_hits = latex_command_re.findall(cleaned)
    dollar_hits = dollar_math_re.findall(cleaned)
    subscript_hits = subscript_brace_re.findall(cleaned)

    if latex_hits:
        sample = ", ".join(sorted(set(latex_hits))[:6])
        errors.append(f"Unrendered LaTeX command(s) found ({len(latex_hits)} occurrence(s)): {sample}")
    if dollar_hits:
        sample = "; ".join(dollar_hits[:4])
        errors.append(f"Unrendered $...$ math delimiter(s) found ({len(dollar_hits)} occurrence(s)): {sample}")
    if subscript_hits:
        sample = ", ".join(sorted(set(subscript_hits))[:6])
        errors.append(f"Unrendered LaTeX subscript brace syntax found: {sample}")

    return errors


def check_image_rendering(html_text, all_files=None):
    """Flag broken or improperly-referenced <img> tags in visible QB HTML.
    Catches the classes of image bug most likely to slip through manual review:
      - missing src / missing alt text (accessibility + SEO)
      - leftover data: URIs or blob: URLs from drafting (should be hosted assets)
      - localhost/127.0.0.1/file:// paths (dev-only, will 404 in production)
      - relative image paths (site convention is absolute /meoclass1/assets/...)
      - /meoclass1/assets/... references to files that don't actually exist in the repo
        (only checked when all_files, a {relative_path: bytes} map of the repo
        snapshot under meoclass1/, is supplied)
    """
    errors = []
    cleaned = re.sub(r"<script.*?</script>", "", html_text, flags=re.S | re.I)
    cleaned = re.sub(r"<style.*?</style>", "", cleaned, flags=re.S | re.I)

    img_tags = re.findall(r'<img\b[^>]*>', cleaned, flags=re.I)

    for tag in img_tags:
        src_m = re.search(r'src\s*=\s*["\']([^"\']*)["\']', tag, re.I)
        alt_m = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', tag, re.I)
        id_m = re.search(r'id\s*=\s*["\']([^"\']*)["\']', tag, re.I)
        src = src_m.group(1).strip() if src_m else ""

        # Lightbox placeholder <img id="lightbox-img" src=""> is intentionally empty —
        # populated by JS on click. Skip the missing-src check for this known pattern.
        if id_m and "lightbox" in id_m.group(1).lower() and not src:
            continue

        if not src:
            errors.append(f"<img> tag missing or empty src attribute: {tag[:80]}")
            continue

        if not alt_m or not alt_m.group(1).strip():
            errors.append(f"<img> missing alt text (accessibility/SEO): src={src}")

        if src.startswith("data:"):
            errors.append(f"<img> uses a data: URI — likely a drafting leftover, should be a hosted asset: {src[:50]}...")
        elif re.match(r'^(blob:|file://)', src, re.I):
            errors.append(f"<img> src is a local/dev-only URL, will break in production: {src}")
        elif re.match(r'^https?://(localhost|127\.0\.0\.1)', src, re.I):
            errors.append(f"<img> src points to localhost, will break in production: {src}")
        elif src.startswith("/meoclass1/assets/"):
            if all_files is not None:
                rel = "assets/" + src.split("/meoclass1/assets/", 1)[1]
                if rel not in all_files:
                    errors.append(f"<img> src references an asset not found in the repo: {src}")
        elif src.startswith("/"):
            pass  # other absolute site-root paths — not this script's concern
        elif not re.match(r'^https?://', src, re.I):
            errors.append(f"<img> src is a relative path, not the site convention (/meoclass1/assets/...): {src}")

    return errors


def parse_known_traps(md_bytes):
    """Extract auto-scannable wrong phrases from known_traps.md 'GREP:' lines.
    Format: a line 'GREP: <exact phrase>' under each numbered entry. Entries
    marked 'GREP: SKIP' are intentionally excluded from automated scanning
    (too generic / context-dependent) and remain manual-review-only."""
    if md_bytes is None:
        return []
    try:
        text = md_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return []
    traps = []
    for line in text.splitlines():
        m = re.match(r'^GREP:\s*(.+)$', line.strip())
        if m:
            phrase = m.group(1).strip()
            if phrase and phrase.upper() != "SKIP":
                traps.append(phrase)
    return traps


def check_known_traps(html_text, traps):
    """Flag any live HTML containing a phrase from the known_traps WRONG list.
    A hit means a previously-identified error pattern has resurfaced —
    escalate for manual review rather than auto-correct."""
    errors = []
    cleaned = re.sub(r"<[^>]+>", " ", html_text)  # strip tags so phrase matching works on visible text
    for phrase in traps:
        if phrase.lower() in cleaned.lower():
            errors.append(f"KNOWN TRAP resurfaced: \"{phrase}\" found in visible text — check against known_traps.md")
    return errors


def check_file(filename, content_bytes, all_files=None, known_traps=None):
    try:
        html_text = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return {"file": filename, "errors": ["File is not valid UTF-8"], "question_count": 0}

    base = filename.split("/")[-1]
    is_cheatsheet = "cheatsheet" in base.lower()
    is_qb_file = bool(re.match(r"QB\d", base, re.I))  # covers both Q&A cards and cheat sheets
    is_qb_question_file = is_qb_file and not is_cheatsheet

    errors = []
    errors += check_tag_balance(html_text, filename)
    errors += check_ga4_tag(html_text)
    errors += check_robots_meta(html_text)

    q_count = 0
    if is_qb_question_file:
        block_errors, q_count = check_mandatory_block_counts(html_text)
        errors += block_errors
        errors += check_q_id_sequence(html_text)
        errors += check_toc_anchors(html_text)

    if is_qb_file:
        # Formula rendering and image checks apply to both Q&A cards and cheat sheets —
        # diagrams and formulas now live in either place depending on the diagram
        # placement policy (Section 6b of the QB production skill).
        errors += check_formula_rendering(html_text)
        errors += check_image_rendering(html_text, all_files)
        if known_traps:
            errors += check_known_traps(html_text, known_traps)

    return {"file": filename, "errors": errors, "question_count": q_count}


def check_manifest(files, file_results=None):
    """Validate qb_content_index.json is parseable and cross-check it against
    disk reality in both directions:
      1. Manifest references a file that isn't on disk (deleted/renamed but
         manifest not updated — a 'file didn't get reflected' symptom)
      2. A QB html file exists on disk but has no manifest entry (built and
         pushed, but manifest update step was skipped — the other half of the
         same symptom)
      3. Manifest's stated question_count for a file doesn't match the actual
         q-card count found on disk (partial edit landed, index wasn't
         re-synced)
    """
    errors = []
    manifest_bytes = files.get(MANIFEST_NAME)
    if manifest_bytes is None:
        return [f"{MANIFEST_NAME} not found in repo"], {}
    try:
        manifest = json.loads(manifest_bytes.decode("utf-8"))
    except json.JSONDecodeError as e:
        return [f"{MANIFEST_NAME} is not valid JSON: {e}"], {}

    manifest_files = manifest.get("files", {})
    html_files_on_disk = {f for f in files if f.lower().endswith(".html")}

    missing_on_disk = set(manifest_files.keys()) - html_files_on_disk
    if missing_on_disk:
        errors.append(f"Manifest references file(s) not found in repo: {sorted(missing_on_disk)}")

    # Orphan QB files: built HTML present on disk, but never added to the manifest.
    # Cheat sheets are excluded — they follow a separate A/B pattern and are not
    # required to carry manifest entries (per QB naming conventions).
    qb_html_on_disk = {f for f in html_files_on_disk
                        if re.match(r"QB\d", f.split("/")[-1], re.I)
                        and "cheatsheet" not in f.lower()}
    orphan_files = qb_html_on_disk - set(manifest_files.keys())
    if orphan_files:
        errors.append(f"QB file(s) on disk but missing from manifest (index not updated after build): {sorted(orphan_files)}")

    if file_results:
        counts_on_disk = {r["file"]: r["question_count"] for r in file_results}
        for fname, meta in manifest_files.items():
            manifest_qcount = meta.get("question_count")
            actual_qcount = counts_on_disk.get(fname)
            # Only flag when disk count EXCEEDS manifest (a clean signal of a real
            # under-indexed edit). Manifest > disk is expected/benign when a file
            # includes non-numeric summary/map cards (e.g. id="family-trees") that
            # the numeric q-card scanner intentionally excludes but the manifest
            # legitimately counts — so that direction is not flagged.
            if manifest_qcount is not None and actual_qcount is not None and actual_qcount > 0 \
                    and actual_qcount > manifest_qcount:
                errors.append(
                    f"Question count mismatch for {fname}: manifest says {manifest_qcount}, "
                    f"disk has {actual_qcount} numeric q-cards — manifest likely stale after an edit"
                )

    return errors, manifest_files


# ---------- Report + email ----------
def build_report(manifest_errors, file_results, total_files, total_questions_manifest):
    ts = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    files_with_errors = [r for r in file_results if r["errors"]]
    total_q_counted = sum(r["question_count"] for r in file_results)

    lines = []
    lines.append(f"MIW QB Health Check — {ts}")
    lines.append("=" * 50)
    lines.append(f"Files scanned: {total_files}")
    lines.append(f"Questions found on disk: {total_q_counted}  |  Manifest total: {total_questions_manifest}")
    lines.append(f"Files with errors: {len(files_with_errors)}")
    lines.append("")

    if manifest_errors:
        lines.append("MANIFEST ISSUES")
        lines.append("-" * 30)
        for e in manifest_errors:
            lines.append(f"  ⚠ {e}")
        lines.append("")

    if files_with_errors:
        lines.append("FILE-LEVEL ISSUES")
        lines.append("-" * 30)
        for r in sorted(files_with_errors, key=lambda x: x["file"]):
            lines.append(f"\n▶ {r['file']}  ({r['question_count']} questions)")
            for e in r["errors"]:
                lines.append(f"    ✗ {e}")
    else:
        lines.append("✅ No structural errors found in any QB file.")

    lines.append("")
    lines.append("-" * 50)
    lines.append("Clean files: " + ", ".join(
        sorted(r["file"] for r in file_results if not r["errors"])
    ) if any(not r["errors"] for r in file_results) else "")

    return "\n".join(lines), len(files_with_errors) + len(manifest_errors)


def send_email(subject, body):
    smtp_key = os.environ.get("BREVO_SMTP_KEY")
    if not SMTP_LOGIN or not smtp_key:
        print("BREVO_SMTP_LOGIN / BREVO_SMTP_KEY not set — printing report instead of emailing.\n")
        print(body)
        return

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_LOGIN, smtp_key)          # auth uses the SMTP relay login
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())  # envelope/From uses the verified sender
    print(f"Email sent to {EMAIL_TO}")


def main():
    print("Fetching repo tarball...")
    try:
        files = fetch_repo_tarball()
    except Exception as e:
        send_email("🔴 MIW QB Health Check — FETCH FAILED",
                    f"Could not fetch the repo to run health checks.\n\nError: {e}")
        sys.exit(1)

    known_traps = parse_known_traps(files.get(KNOWN_TRAPS_PATH))

    html_files = {name: content for name, content in files.items()
                  if name.lower().endswith(".html")}

    results = []
    for name, content in sorted(html_files.items()):
        results.append(check_file(name, content, all_files=files, known_traps=known_traps))

    # manifest check runs after file results so it can cross-check question counts
    manifest_errors, manifest_files = check_manifest(files, file_results=results)
    if known_traps == [] and KNOWN_TRAPS_PATH not in files:
        manifest_errors.append(
            f"{KNOWN_TRAPS_PATH} not found in repo — known-traps check skipped this run"
        )

    total_questions_manifest = sum(
        f.get("question_count", 0) for f in manifest_files.values()
    ) if manifest_files else "?"

    report, error_count = build_report(manifest_errors, results, len(html_files), total_questions_manifest)

    status = "🔴" if error_count else "✅"
    subject = f"{status} MIW QB Health Check — {error_count} issue(s) found" if error_count \
        else "✅ MIW QB Health Check — all clear"

    send_email(subject, report)
    print(report)


if __name__ == "__main__":
    main()
