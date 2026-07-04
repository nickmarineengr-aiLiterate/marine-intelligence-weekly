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

VOID_ELEMENTS = {"br", "img", "meta", "link", "hr", "input", "area", "base",
                  "col", "embed", "source", "track", "wbr"}

MANDATORY_CLASSES = ["q-card", "reg-box", "ce-tip", "q-footer"]

EMAIL_TO = os.environ.get("QB_HEALTH_EMAIL_TO", "contactus@marineintelligenceweekly.com")
EMAIL_FROM = os.environ.get("BREVO_SMTP_LOGIN", "")
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


def check_file(filename, content_bytes):
    try:
        html_text = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return {"file": filename, "errors": ["File is not valid UTF-8"], "question_count": 0}

    base = filename.split("/")[-1]
    is_cheatsheet = "cheatsheet" in base.lower()
    is_qb_question_file = bool(re.match(r"QB\d", base, re.I)) and not is_cheatsheet

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

    return {"file": filename, "errors": errors, "question_count": q_count}


def check_manifest(files):
    """Validate qb_content_index.json is parseable and its file list matches disk reality."""
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
    if not EMAIL_FROM or not smtp_key:
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
        server.login(EMAIL_FROM, smtp_key)
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())
    print(f"Email sent to {EMAIL_TO}")


def main():
    print("Fetching repo tarball...")
    try:
        files = fetch_repo_tarball()
    except Exception as e:
        send_email("🔴 MIW QB Health Check — FETCH FAILED",
                    f"Could not fetch the repo to run health checks.\n\nError: {e}")
        sys.exit(1)

    manifest_errors, manifest_files = check_manifest(files)

    html_files = {name: content for name, content in files.items()
                  if name.lower().endswith(".html")}

    results = []
    for name, content in sorted(html_files.items()):
        results.append(check_file(name, content))

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
