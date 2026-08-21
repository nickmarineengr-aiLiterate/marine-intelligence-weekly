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
import collections
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
INDEX_NAME = "index.html"   # relative to QB_FOLDER_PREFIX, e.g. meoclass1/index.html
# Manifest filenames are defined canonically in tools/notes/miw_paths.py. This checker
# scans the GitHub tree rather than local disk, so it keeps its own repo-relative copies
# instead of importing. If a manifest is ever renamed, change BOTH places.
# NOTE: the oral-notes manifest uses UNDERSCORES. A hyphenated `notes-content-index.json`
# was a stale duplicate, deleted 2026-08-06 (commit 89291e5). Never reintroduce it.
NOTES_MANIFEST_NAME = "oralnotes/notes_content_index.json"
WRITTEN_MANIFEST_NAME = "oralnotes/written_content_index.json"
LEGACY_NOTES_MANIFEST_NAME = "oralnotes/notes-content-index.json"   # must never exist
NOTES_FOLDER_PREFIX = "oralnotes/"
NOTES_INDEX_UTILITY_FILES = {"index.html", "notes-master-index.html", "uday-index-crossref.html"}
SQ_FOLDER_PREFIX = "SQ/"
SQ_UTILITY_FILES = {"index.html", "pay.html", "examiner-index.html"}
GA4_TAG = "G-0YEE2CBNP5"
KNOWN_TRAPS_PATH = "known_traps.md"   # relative to QB_FOLDER_PREFIX, e.g. meoclass1/known_traps.md

VOID_ELEMENTS = {"br", "img", "meta", "link", "hr", "input", "area", "base",
                  "col", "embed", "source", "track", "wbr"}

MANDATORY_CLASSES = ["q-card", "reg-box", "ce-tip", "q-footer"]

# An env var that is SET BUT EMPTY must not beat the fallback. The
# workflow passes QB_HEALTH_EMAIL_TO: ${{ secrets.QB_HEALTH_EMAIL_TO }},
# and an undefined secret interpolates to "" -- so the name is ALWAYS
# present in that job and os.environ.get's default could never fire.
# An empty recipient reaches the relay as `RCPT TO:<>` and comes back
# as SMTPRecipientsRefused 501, which reads in the Actions UI as a
# failed health check rather than as an unset address. This is the same
# defect that took the SolvedQP checker down; see
# tools/pastpapers/solvedqp_health_check.py.
EMAIL_TO = (os.environ.get("QB_HEALTH_EMAIL_TO") or "").strip() \
    or "contactus@marineintelligenceweekly.com"
SMTP_LOGIN = os.environ.get("BREVO_SMTP_LOGIN", "")  # auth credential only — NOT a valid From address
EMAIL_FROM = os.environ.get("BREVO_SENDER_EMAIL", "contactus@marineintelligenceweekly.com")  # verified sender in Brevo
SMTP_HOST = "smtp-relay.brevo.com"
SMTP_PORT = 587


# ---------- Repo snapshot sources ----------
#
# THE SOURCE IS EXPLICIT, AND THAT IS THE POINT.
#
# Until 21 August 2026 this checker had exactly one source: it downloaded a
# tarball of remote `main` from codeload.github.com. It never read local disk.
#
# That made a whole class of release evidence structurally vacuous. Several
# handoffs recorded "N findings on the branch and N on a clean origin/main —
# 0 new, 0 gone" as PRE-MERGE proof that a batch introduced no regression.
# Both runs were reading the same remote `main`; neither could see the change
# under test. E6 proved it rather than inferring it: five `q-card` tags were
# corrupted in a clean tree and the re-run produced a byte-identical finding
# set. A local regression was invisible.
#
# The underlying releases are NOT thereby defective — the other gates
# (validators, mutation suites, digests, determinism) did the real work. Only
# that specific health-check comparison was non-load-bearing, and it should not
# be cited as proof of local branch health in any earlier handoff.
#
# Every check in this file is a pure function of a {relative_path: bytes} dict,
# so the fix is a second and third loader for that same dict — not a change to
# any check.
#
# All loaders normalise CRLF to LF. A Windows working copy can hold CRLF while
# the git blob holds LF; without normalisation, `--source local` and
# `--source ref` would disagree on files that are identical in content, and the
# comparison the caller is trying to make would be noise.


class SourceInfo:
    """What was actually scanned. Reported so a result cannot be misread."""

    def __init__(self, source_type, location, commit=None, file_count=0):
        self.source_type = source_type      # "remote-main" | "local" | "ref"
        self.location = location            # URL, filesystem path, or git ref
        self.commit = commit                # resolved SHA where knowable
        self.file_count = file_count

    def describe(self):
        lines = [
            f"source_type : {self.source_type}",
            f"source      : {self.location}",
            f"commit      : {self.commit or '(not resolved)'}",
            f"files       : {self.file_count}",
            f"eol         : normalised CRLF -> LF",
        ]
        return "\n".join(lines)


def _keep(rel_path):
    """Map a repo-relative path into the scan dict, or None to drop it.

    meoclass1/ files lose their prefix; SQ/ files keep theirs, because SQ/ is a
    sibling of meoclass1/ rather than nested inside it (the free-sample teaser
    copies live there).
    """
    if rel_path.startswith(QB_FOLDER_PREFIX):
        return rel_path[len(QB_FOLDER_PREFIX):]
    if rel_path.startswith(SQ_FOLDER_PREFIX):
        return rel_path
    return None


def _normalise(raw):
    return raw.replace(b"\r\n", b"\n").replace(b"\r", b"\n")


def _extract_tar(fileobj, mode, strip_leading_component):
    """Shared tar walk for the remote tarball and for `git archive` output."""
    files = {}
    with tarfile.open(fileobj=fileobj, mode=mode) as tar:
        for member in tar.getmembers():
            if not member.isfile():
                continue
            name = member.name
            if strip_leading_component:
                parts = name.split("/", 1)
                if len(parts) != 2:
                    continue
                name = parts[1]
            key = _keep(name)
            if key is None:
                continue
            handle = tar.extractfile(member)
            if handle is None:
                continue
            files[key] = _normalise(handle.read())
    return files


def _repo_root():
    """The repository root, derived from this file's location."""
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _git(args, binary=False):
    import subprocess
    out = subprocess.run(["git"] + args, cwd=_repo_root(),
                         capture_output=True, check=False)
    if out.returncode != 0:
        err = out.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"git {' '.join(args)} failed: {err}")
    return out.stdout if binary else out.stdout.decode("utf-8").strip()


def fetch_repo_tarball():
    """Remote `main` via codeload.github.com. The GitHub Actions default."""
    url = f"https://codeload.github.com/{GITHUB_REPO}/tar.gz/refs/heads/{GITHUB_BRANCH}"
    req = urllib.request.Request(url, headers={"User-Agent": "qb-health-check"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        raw = resp.read()
    files = _extract_tar(io.BytesIO(raw), "r:gz", strip_leading_component=True)
    try:
        commit = _git(["rev-parse", f"origin/{GITHUB_BRANCH}"])
    except Exception:
        commit = None
    info = SourceInfo("remote-main", url, commit, len(files))
    return files, info


def fetch_local_tree():
    """The CURRENT WORKING TREE on local disk — uncommitted edits included.

    This is the mode a pre-merge release gate wants: it sees the change under
    test, which remote-main mode cannot.
    """
    root = _repo_root()
    files = {}
    for prefix in (QB_FOLDER_PREFIX, SQ_FOLDER_PREFIX):
        base = os.path.join(root, prefix.rstrip("/"))
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in (".git", "__pycache__")]
            for filename in filenames:
                full = os.path.join(dirpath, filename)
                rel = os.path.relpath(full, root).replace(os.sep, "/")
                key = _keep(rel)
                if key is None:
                    continue
                try:
                    with open(full, "rb") as fh:
                        files[key] = _normalise(fh.read())
                except OSError:
                    continue
    try:
        commit = _git(["rev-parse", "HEAD"])
        dirty = bool(_git(["status", "--porcelain"]))
    except Exception:
        commit, dirty = None, False
    label = f"{root} (working tree{', DIRTY' if dirty else ', clean'})"
    return files, SourceInfo("local", label, commit, len(files))


def fetch_ref_tree(ref):
    """Any git ref or exported tree — e.g. a clean `origin/main` baseline."""
    raw = _git(["archive", "--format=tar", ref], binary=True)
    files = _extract_tar(io.BytesIO(raw), "r:", strip_leading_component=False)
    try:
        commit = _git(["rev-parse", ref])
    except Exception:
        commit = None
    return files, SourceInfo("ref", ref, commit, len(files))


def load_source(source="remote", ref=None):
    """Dispatch to the requested loader. Never silently substitutes another."""
    if source == "remote":
        return fetch_repo_tarball()
    if source == "local":
        return fetch_local_tree()
    if source == "ref":
        if not ref:
            raise ValueError("--source ref requires --ref REF")
        return fetch_ref_tree(ref)
    raise ValueError(f"unknown source: {source!r}")


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


def check_pipe_table_format(html_text):
    """Flag markdown-style pipe-delimited tables leaked into live HTML instead of
    being converted to real <table> markup. These render as unscannable wrapped
    text on mobile (the primary subscriber device) and defeat the purpose of a
    comparison table. Pattern: a separator row like '| --- | --- |' (any dash
    count/spacing), whether alone in a <p> or embedded inline with newlines.
    Fixed repo-wide 2026-07-29 across QB1_B, QB1_F, QB1_G, QB2_A, QB3_H — see
    known_traps.md entry on pipe-table formatting."""
    if re.search(r'\|\s*-{2,}\s*\|', html_text):
        count = len(re.findall(r'\|\s*-{2,}\s*\|', html_text))
        return [f"Pipe-delimited markdown table detected ({count} instance(s)) — convert to real <table> markup"]
    return []


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
            raw = m.group(1).strip()
            if not raw:
                continue
            # "SKIP" entries (with or without a trailing explanation in
            # parentheses, e.g. "SKIP (91.16 is legitimate when...)") are
            # manual-review-only and must not become literal scan targets.
            if raw.upper() == "SKIP" or raw.upper().startswith("SKIP "):
                continue
            # NOTE: some GREP lines legitimately contain a comma inside a
            # single phrase (e.g. "Merchant Shipping Act, 1958"), while others
            # use the comma to separate multiple independent phrases (e.g.
            # "60 Flag State Inspections, 60 FSIs"). These are not
            # distinguishable by a generic rule without risking a regression
            # (a naive split turns "Merchant Shipping Act, 1958" into a
            # standalone "1958" trap, which would false-positive on almost
            # any year mention). Kept as one literal phrase per line, as
            # before — flagged to Nixon as a known limitation rather than
            # silently "fixed" in an unsafe way. To make multi-phrase lines
            # actually scannable, known_traps.md should move to one GREP
            # line per phrase instead of comma-joining them.
            traps.append(raw)
    return traps


NEGATION_MARKERS = [
    "superseded by", "supersedes", "replaced by", "replaces",
    "repealed", "not... but", "not the... but", "does not designate",
    "is not", "formerly", "now succeeded by", "since replaced by",
    "prior revision incorrectly stated", "previously stated",
    "previously cited", "previous revision", "old error", "the old",
    "corrected from", "corrected to", "incorrectly stated",
    "re-enacted as", "reenacted as", "re-enacted", "now in force as",
    # Word-stem markers (2026-08-01): substring matches on the stem catch
    # every grammatical form (supersede/supersedes/superseded/superseding,
    # replace/replaces/replaced/replacing, repeal/repeals/repealed/repealing)
    # instead of whack-a-mole exact phrases. Safe to broaden — a hit here
    # only DOWNGRADES an error to a [REVIEW] note, it never suppresses
    # visibility, so a slightly loose stem match trades a few over-cautious
    # reviews for catching real supersession/correction framing that the
    # exact-phrase list above was missing (e.g. "...superseding A.1185(33)"
    # and "has already been replaced" were both missed pre-fix).
    "supersed", "replac", "repeal", "revok", "carried into", "carried from",
    "carried forward into",
]


def _split_sentences(text):
    # Cheap sentence splitter — good enough for negation-marker co-occurrence
    # checks; doesn't need to be linguistically perfect, just needs to keep
    # the trap phrase and a same-sentence marker together.
    return re.split(r'(?<=[.!?])\s+', text)


def check_known_traps(html_text, traps):
    """Flag any live HTML containing a phrase from the known_traps WRONG list.
    A hit means a previously-identified error pattern has resurfaced —
    escalate for manual review rather than auto-correct.

    Negation-aware: per known_traps.md ("Health-check grep — negation-context
    noise", added 2026-07-19), a bare substring hit is frequently a correctly-
    framed sentence citing the old/wrong term in order to supersede, repeal,
    or debunk it (e.g. a `.correction-note` block, "superseded by" prose).
    Before flagging as a confirmed resurfaced error, check whether a
    negation/supersession marker appears in the same sentence as the trap
    phrase — if so, downgrade to a "review" note instead of an error, so it's
    still visible but doesn't count as a structural fault requiring urgent fix.
    """
    errors = []
    reviews = []
    cleaned = re.sub(r"<[^>]+>", " ", html_text)  # strip tags so phrase matching works on visible text
    cleaned = re.sub(r"\s+", " ", cleaned)
    sentences = _split_sentences(cleaned)
    for phrase in traps:
        phrase_l = phrase.lower()
        if phrase_l not in cleaned.lower():
            continue
        hit_sentences = [s for s in sentences if phrase_l in s.lower()]
        if not hit_sentences:
            hit_sentences = [cleaned]  # fallback if sentence split missed it (e.g. spans a split point)
        for s in hit_sentences:
            s_l = s.lower()
            if any(marker in s_l for marker in NEGATION_MARKERS):
                reviews.append(
                    f"KNOWN TRAP phrase present but in negation/correction context: \"{phrase}\" "
                    f"— likely correctly framed (supersession/correction note); verify manually rather than treating as a resurfaced error"
                )
            else:
                errors.append(f"KNOWN TRAP resurfaced: \"{phrase}\" found in visible text — check against known_traps.md")
    return errors + [f"[REVIEW] {r}" for r in reviews]


# ---------- Notes-series checks (Simon Sir Notes / Engineering Management Notes /
#             Current Topics / WA Written QA — all live under oralnotes/) ----------

def check_topic_block_counts(html_text):
    """For files using the topic-block architecture (Simon Sir Notes, Engineering
    Management Notes, Current Topics): verify each numbered topic-block has a
    matching topic-footer, and count real (non-CSS) occurrences of each.
    Accepts both the standard `id="topic-N"` convention and the variant
    `id="topic-pN-M"` seen in some Parts, flagging the latter as a naming
    deviation worth a quick look rather than a structural break.
    Files without any topic-block divs (e.g. WA single-chapter files) are not
    applicable — caller should skip this check when topic_ids is empty."""
    errors = []
    block_divs = re.findall(r'<div class="topic-block"[^>]*\bid="(topic-[a-zA-Z0-9-]+)"', html_text)
    footer_divs = re.findall(r'<div class="topic-footer">', html_text)
    if len(block_divs) != len(footer_divs):
        errors.append(
            f"topic-block count ({len(block_divs)}) does not match topic-footer count "
            f"({len(footer_divs)}) — a topic may be missing its closing footer/version tag"
        )
    non_standard = [t for t in block_divs if not re.fullmatch(r'topic-\d+', t)]
    if non_standard:
        errors.append(
            f"Topic id(s) don't follow the standard 'topic-N' convention (found {non_standard[:3]}"
            f"{'...' if len(non_standard) > 3 else ''}) — check against notes-mgmt skill Section 4"
        )
    return errors, block_divs


def check_topic_id_sequence(topic_ids):
    """Topic ids should have no duplicates and no internal numbering gaps within
    this file. Cross-Part continuity (T-numbers continuing from the prior Part)
    is a separate, manual check per the notes-mgmt skill — not verified here."""
    errors = []
    nums = [int(re.search(r'\d+', t).group()) for t in topic_ids]
    if not nums:
        return errors
    seen, dupes = set(), set()
    for n in nums:
        if n in seen:
            dupes.add(n)
        seen.add(n)
    if dupes:
        errors.append(f"Duplicate topic id(s): {sorted(dupes)}")
    expected = set(range(min(nums), max(nums) + 1))
    missing = expected - seen
    if missing:
        errors.append(f"Gap(s) in topic numbering — missing topic-id(s): {sorted(missing)}")
    return errors


def check_notes_gate(html_text, filename):
    """Gated notes/WA files must carry the canonical auth-gate script. Flags
    files that carry the FULL paywall robots signature (noindex, nofollow,
    noarchive, nosnippet — the standard applied to genuinely gated content per
    the notes-mgmt skill) but are missing the miw_auth cookie check. A partial
    'noindex, nofollow' alone (used on some intentionally free/ungated pages)
    does not trigger this — that's a different, legitimate pattern. Index/nav
    utility pages are excluded entirely by the caller."""
    errors = []
    has_full_paywall_noindex = bool(re.search(
        r'name="robots"[^>]+noindex[^"]*nofollow[^"]*noarchive[^"]*nosnippet', html_text, re.I))
    has_gate = "miw_auth=1" in html_text
    if has_full_paywall_noindex and not has_gate:
        errors.append("Marked with full paywall noindex signature but no miw_auth gate script found — check if gating step was skipped")
    return errors


def check_notes_file(filename, content_bytes, known_traps=None):
    try:
        html_text = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return {"file": NOTES_FOLDER_PREFIX + filename, "errors": ["File is not valid UTF-8"], "topic_count": 0}

    is_utility_page = filename in NOTES_INDEX_UTILITY_FILES

    errors = []
    errors += check_tag_balance(html_text, filename)
    errors += check_ga4_tag(html_text)
    errors += check_robots_meta(html_text)
    errors += check_pipe_table_format(html_text)
    if not is_utility_page:
        errors += check_notes_gate(html_text, filename)
    if known_traps:
        errors += check_known_traps(html_text, known_traps)

    block_errors, topic_ids = check_topic_block_counts(html_text)
    if not is_utility_page:
        errors += block_errors
    standard_ids = [t for t in topic_ids if re.fullmatch(r'topic-\d+', t)]
    if standard_ids:
        errors += check_topic_id_sequence(standard_ids)

    return {"file": NOTES_FOLDER_PREFIX + filename, "errors": errors, "topic_count": len(topic_ids)}


def check_notes_manifest(files, notes_results):
    """Cross-check notes_content_index.json and written_content_index.json against
    disk reality in both directions, same pattern as check_manifest() for QB."""
    errors = []
    notes_files_on_disk = {f[len(NOTES_FOLDER_PREFIX):] for f in files
                            if f.startswith(NOTES_FOLDER_PREFIX) and f.lower().endswith(".html")}
    manifest_listed = set()

    # Duplicate-truth guard. A second, divergent copy of the oral-notes manifest
    # (hyphenated) coexisted with the canonical one for 11 days in Jul-Aug 2026 and
    # was invisible because nothing loads these manifests at request time. Fail loudly
    # if it ever returns.
    if LEGACY_NOTES_MANIFEST_NAME in files:
        errors.append(
            f"RETIRED MANIFEST HAS REAPPEARED: {NOTES_FOLDER_PREFIX.rstrip('/')}/"
            f"{LEGACY_NOTES_MANIFEST_NAME.split('/')[-1]} exists in the repo. The canonical "
            f"oral-notes manifest is notes_content_index.json (underscores). Delete the "
            f"hyphenated file — do not edit or read it. See tools/notes/SKILL.md section 8a."
        )

    for manifest_path, label in ((NOTES_MANIFEST_NAME, "notes_content_index.json"),
                                  (WRITTEN_MANIFEST_NAME, "written_content_index.json")):
        raw = files.get(manifest_path)
        if raw is None:
            errors.append(f"{label} not found in repo")
            continue
        try:
            manifest = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError as e:
            errors.append(f"{label} is not valid JSON: {e}")
            continue
        for series_key, series in manifest.get("series", {}).items():
            for fname in series.get("files", {}).keys():
                manifest_listed.add(fname)
                if fname not in notes_files_on_disk:
                    errors.append(f"{label} series '{series_key}' references file not found on disk: {fname}")

    orphans = notes_files_on_disk - manifest_listed - NOTES_INDEX_UTILITY_FILES
    if orphans:
        errors.append(f"oralnotes/ file(s) on disk but not listed in either manifest: {sorted(orphans)}")

    return errors


def extract_citations(html_text):
    """Pull regulatory citation tokens out of an HTML page for drift comparison.

    Catches the citation shapes this repo actually uses: IMO Assembly and
    committee resolutions (A.982(24), MEPC.267(68), MSC.290(87)), MEPC/MSC
    circulars including revisions (MEPC.1/Circ.510, MEPC.1/Circ.778/Rev.5),
    and SOLAS/MARPOL regulation references. Returns a set, so ordering and
    repetition are ignored — only presence matters.

    This exists because file-length comparison cannot see a one-line citation
    correction. Fixing a resolution number in the gated copy and forgetting the
    SQ teaser copy changes the byte count by a few dozen characters, which is
    invisible to a 15% size check but is exactly the drift that matters: the
    free sample is the copy prospective subscribers read first.
    """
    text = re.sub(r"<[^>]+>", " ", html_text)
    text = text.replace("&amp;", "&")
    pats = [
        r"\b(?:A|MEPC|MSC|LEG|FAL)\.\d+\(\d+\)",                 # A.982(24), MEPC.267(68)
        r"\b(?:MEPC|MSC|COLREG)\.\d+/Circ\.\d+(?:/Rev\.\d+)?",    # MEPC.1/Circ.778/Rev.5
        r"\bMSC-MEPC\.\d+/Circ\.\d+",
        r"\bUNCLOS\s+Art(?:icle)?\.?\s*\d+(?:\(\d+\))?",
        r"\bSOLAS\s+(?:Ch\.?\s*)?[IVX]+-?\d*/(?:Reg\.?\s*)?[\d.\-]+",
        r"\bMARPOL\s+Annex\s+[IVX]+",
    ]
    found = set()
    for p in pats:
        for m in re.finditer(p, text, re.I):
            found.add(re.sub(r"\s+", " ", m.group(0)).strip().upper())
    return found


def citation_bases(html_text):
    """Map instrument -> set of revision/session numbers cited for it.

    Used for contradiction detection between a gated file and its SQ teaser
    copy. Keying on the base instrument (MSC.1/Circ.1405, A.982) rather than
    the full citation string means a disagreement about WHICH revision is
    current becomes visible, while a copy that simply omits the instrument
    entirely is ignored.

    Real example this was built from: the gated notes page cited
    MSC.1/Circ.1405/Rev.2 (correct - Rev.2 of 25 May 2012 is the final
    revision) while the public teaser still cited a non-existent
    "MSC.1/Circ.1405/Rev.3", conflating it with the companion flag-State
    circular MSC.1/Circ.1406/Rev.3. The size-based drift check could not see
    a one-character difference.
    """
    text = re.sub(r"<[^>]+>", " ", html_text)
    bases = {}
    for m in re.finditer(
            r"\b((?:MEPC|MSC|COLREG|MSC-MEPC|MSC-FAL)\.\d+/Circ\.\d+)(?:/Rev\.(\d+))?",
            text, re.I):
        if m.group(2):
            # Only explicit revisions are recorded. A bare "MSC.1/Circ.1206"
            # asserts nothing about which revision is current, so it can never
            # contradict anything and must not be treated as a claim.
            bases.setdefault(m.group(1).upper(), set()).add("Rev." + m.group(2))
    for m in re.finditer(r"\b((?:A|MEPC|MSC|LEG|FAL)\.\d+)\((\d+)\)", text, re.I):
        bases.setdefault(m.group(1).upper(), set()).add("(" + m.group(2) + ")")
    return bases


def check_sq_file(filename, content_bytes, all_files=None, known_traps=None, main_copy_bytes=None):
    """Files under SQ/ are intentionally free/ungated sample teasers — the
    miw_auth gate check and manifest cross-check do not apply here by design.
    Still run: tag balance, GA4, known-traps, and (for QB-style files)
    formula/image rendering. Also flags if this SQ copy has silently diverged
    from the corresponding main meoclass1/ copy — SQ files are duplicated by
    hand and have no automated sync, so drift is a known risk, not something
    to auto-resolve."""
    try:
        html_text = content_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return {"file": SQ_FOLDER_PREFIX + filename, "errors": ["File is not valid UTF-8"], "question_count": 0}

    if filename in SQ_UTILITY_FILES:
        return {"file": SQ_FOLDER_PREFIX + filename, "errors": [], "question_count": 0}

    errors = []
    errors += check_tag_balance(html_text, filename)
    errors += check_ga4_tag(html_text)
    if known_traps:
        errors += check_known_traps(html_text, known_traps)

    is_qb_style = bool(re.match(r"QB\d", filename, re.I))
    is_notes_style = "topic-block" in html_text

    q_count = 0
    if is_qb_style:
        errors += check_formula_rendering(html_text)
        errors += check_image_rendering(html_text, all_files)
        q_ids = re.findall(r'<div class="q-card"[^>]*\bid="q(\d+)"', html_text)
        q_count = len(q_ids)
    elif is_notes_style:
        block_errors, topic_ids = check_topic_block_counts(html_text)
        errors += block_errors
        q_count = len(topic_ids)

    if main_copy_bytes is not None:
        try:
            main_text = main_copy_bytes.decode("utf-8")
            # Compare only the shared trailing content (strip SQ-specific topbar/CTA banner
            # differences at the top) — a crude but effective drift signal: same file length
            # class and same closing quiz/topic count wildly different flags a stale duplicate.
            if abs(len(main_text) - len(html_text)) > 0.15 * len(main_text):
                errors.append(
                    f"SQ copy size differs from meoclass1/{filename} by >15% — "
                    f"likely diverged/stale duplicate, check both copies are in sync"
                )

            # Citation drift, in two tiers.
            #
            # Tier 1 - CONTRADICTION. Same instrument cited at different
            # revisions/sessions in the two copies. This is truncation-proof:
            # it only compares instruments that appear in BOTH files, so a
            # short teaser that simply omits most of the gated content never
            # trips it. This is the high-signal case - one of the two copies
            # is factually wrong, and if it is the teaser then the error is
            # sitting in the free sample a prospective subscriber reads first.
            main_bases = citation_bases(main_text)
            sq_bases = citation_bases(html_text)
            for base in sorted(set(main_bases) & set(sq_bases)):
                # Disjoint, not merely unequal. If one copy cites Rev.1 and
                # Rev.2 of the same circular while the other cites only Rev.2,
                # that is a subset, not a disagreement - the shared revision
                # means both copies agree on what is current.
                if main_bases[base].isdisjoint(sq_bases[base]):
                    errors.append(
                        f"SQ copy cites {base} at "
                        f"{'/'.join(sorted(sq_bases[base])) or '(no revision)'} but "
                        f"meoclass1/{filename} cites it at "
                        f"{'/'.join(sorted(main_bases[base])) or '(no revision)'} - "
                        f"one of the two copies is wrong, verify against the IMO text"
                    )

            # Tier 2 - OMISSION. Only meaningful when the SQ copy is a full
            # mirror rather than a deliberately truncated teaser, so it is
            # gated on relative size. Without this gate every short teaser
            # would report dozens of false "missing citation" errors.
            if len(html_text) >= 0.85 * len(main_text):
                missing = sorted(extract_citations(main_text) - extract_citations(html_text))
                if missing:
                    errors.append(
                        f"SQ copy is a full mirror of meoclass1/{filename} but is missing "
                        f"citation(s): {', '.join(missing[:8])}"
                        + (f" (+{len(missing) - 8} more)" if len(missing) > 8 else "")
                        + " - the gated copy was likely corrected without updating this teaser"
                    )
        except UnicodeDecodeError:
            pass

    return {"file": SQ_FOLDER_PREFIX + filename, "errors": errors, "question_count": q_count}


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
    errors += check_pipe_table_format(html_text)

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


def check_index_linkage(files, manifest_files):
    """Cross-check meoclass1/index.html against the manifest.

    A QB file can be built, gated, manifested and pushed and still be
    unreachable, because index.html carries its own two data structures:
      QB_GROUPS - the card list that renders the links
      Q_INDEX   - the question-text search index
    Neither is generated from qb_content_index.json, so a batch that updates
    the manifest but not index.html ships files no subscriber can navigate to
    and questions the on-page search cannot find. That is exactly what
    happened to the 4 Aug 2026 July batch (commit 78caad4): eight QB files
    landed manifested and gated, with no card and no search records.

    Checks, in order:
      1. index.html present and both structures parseable
      2. every non-cheat-sheet manifest file has a card in QB_GROUPS
      3. every card's qcount matches the manifest question_count
      4. every card's Q_INDEX record count matches that same number
      5. the hero counters agree with the structures they summarise
    """
    errors = []
    raw = files.get(INDEX_NAME)
    if raw is None:
        return [f"{INDEX_NAME} not found in repo"]
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return [f"{INDEX_NAME} is not valid UTF-8"]

    def _block(name):
        m = re.search(r"const %s = (\[.*?\]);" % name, text, re.S)
        if not m:
            return None
        try:
            return json.loads(m.group(1))
        except json.JSONDecodeError:
            return False

    groups = _block("QB_GROUPS")
    q_index = _block("Q_INDEX")
    for label, val in (("QB_GROUPS", groups), ("Q_INDEX", q_index)):
        if val is None:
            errors.append(f"{INDEX_NAME}: {label} array not found")
        elif val is False:
            errors.append(f"{INDEX_NAME}: {label} is present but not valid JSON")
    if not groups or not q_index:
        return errors

    cards = {c.get("file"): c for g in groups for c in g.get("cards", [])}
    cheatsheets = {m.get("cheatsheet") for m in manifest_files.values() if m.get("cheatsheet")}
    qb_files = {f for f in manifest_files if f not in cheatsheets}

    unlinked = sorted(qb_files - set(cards))
    if unlinked:
        errors.append(
            f"{INDEX_NAME}: manifest QB file(s) have no card in QB_GROUPS and are "
            f"unreachable from the index: {unlinked}"
        )

    stray = sorted(set(cards) - set(manifest_files))
    if stray:
        errors.append(f"{INDEX_NAME}: QB_GROUPS cards reference file(s) absent from the manifest: {stray}")

    counts = collections.Counter(e.get("file") for e in q_index)
    for fname, card in sorted(cards.items()):
        meta = manifest_files.get(fname)
        if not meta:
            continue
        expected = meta.get("question_count")
        if expected is None:
            continue
        if card.get("qcount") != expected:
            errors.append(
                f"{INDEX_NAME}: card qcount for {fname} is {card.get('qcount')} "
                f"but the manifest says {expected}"
            )
        if counts.get(fname, 0) != expected:
            errors.append(
                f"{INDEX_NAME}: Q_INDEX holds {counts.get(fname, 0)} search record(s) for "
                f"{fname} but the manifest says {expected} question(s) — on-page search "
                f"will not find the missing one(s)"
            )

    stats = re.findall(r'<span class="stat-val"[^>]*>([^<]+)</span>', text)
    if len(stats) >= 2:
        for pos, actual, label in ((0, len(q_index), "Questions Live"),
                                   (1, len(cards), "QB Files")):
            shown = stats[pos].strip()
            if shown.isdigit() and int(shown) != actual:
                errors.append(
                    f"{INDEX_NAME}: hero counter '{label}' shows {shown} but the page "
                    f"actually carries {actual}"
                )
    return errors


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
    # SQ/ files are excluded — these are public marketing/teaser copies (free
    # samples) that intentionally live outside the gated meoclass1/ manifest
    # scope, even when their basename matches the QB\d pattern (e.g.
    # SQ/QB1_A.html is a teaser mirroring meoclass1/QB1_A.html's content but
    # is not itself a manifest-tracked file).
    qb_html_on_disk = {f for f in html_files_on_disk
                        if re.match(r"QB\d", f.split("/")[-1], re.I)
                        and "cheatsheet" not in f.lower()
                        and not f.lower().startswith("sq/")}
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

    # Changelog completeness: a file mentioned in a recently_updated note
    # should have a corrections_applied entry to match — otherwise the fix
    # landed in the file but the audit trail was never appended (the exact
    # gap found in the 2026-07-26 manifest audit: QB6_C, QB6_E, QB7_A, QB9_C,
    # QB9_D, QB4_I all had version bumps + live fixes but zero-length
    # corrections_applied arrays).
    recently_updated = manifest.get("recently_updated", [])
    filename_pattern = re.compile(r'\bQB\d+(?:_[A-Za-z]+)*(?:\.html)?\b')
    for entry in recently_updated:
        # canonical correction-log contract: {date, note, files}; "note" is the
        # human description (the hub renders it), "files" is metadata. This
        # check reads the description only, as it always has.
        note = entry.get("note", "")
        date = entry.get("date", "unknown date")
        mentioned = set()
        for m in filename_pattern.findall(note):
            base = m if m.lower().endswith(".html") else m + ".html"
            mentioned.add(base)
        for fname in mentioned:
            meta = manifest_files.get(fname)
            if meta is None:
                continue  # not a QB-series file this manifest tracks (e.g. cheat sheet), skip
            corrections = meta.get("corrections_applied", [])
            if len(corrections) == 0:
                errors.append(
                    f"Changelog gap: {fname} is named in the {date} recently_updated note "
                    f"but has an empty corrections_applied array — fix likely landed without a logged entry"
                )

    return errors, manifest_files


# ---------- Report + email ----------
def build_report(manifest_errors, file_results, total_files, total_questions_manifest,
                  notes_manifest_errors=None, notes_results=None, sq_results=None):
    ts = datetime.now(timezone.utc).strftime("%d %b %Y, %H:%M UTC")
    files_with_errors = [r for r in file_results if r["errors"]]
    total_q_counted = sum(r["question_count"] for r in file_results)
    notes_manifest_errors = notes_manifest_errors or []
    notes_results = notes_results or []
    notes_with_errors = [r for r in notes_results if r["errors"]]
    sq_results = sq_results or []
    sq_with_errors = [r for r in sq_results if r["errors"]]

    lines = []
    lines.append(f"MIW QB + Notes Health Check — {ts}")
    lines.append("=" * 50)
    lines.append("--- QB SERIES ---")
    lines.append(f"Files scanned: {total_files}")
    lines.append(f"Questions found on disk: {total_q_counted}  |  Manifest total: {total_questions_manifest}")
    lines.append(f"Files with errors: {len(files_with_errors)}")
    lines.append("")

    if manifest_errors:
        lines.append("QB MANIFEST ISSUES")
        lines.append("-" * 30)
        for e in manifest_errors:
            lines.append(f"  ⚠ {e}")
        lines.append("")

    if files_with_errors:
        lines.append("QB FILE-LEVEL ISSUES")
        lines.append("-" * 30)
        for r in sorted(files_with_errors, key=lambda x: x["file"]):
            lines.append(f"\n▶ {r['file']}  ({r['question_count']} questions)")
            for e in r["errors"]:
                lines.append(f"    ✗ {e}")
    else:
        lines.append("✅ No structural errors found in any QB file.")

    lines.append("")
    lines.append("--- NOTES / WA SERIES (oralnotes/) ---")
    lines.append(f"Files scanned: {len(notes_results)}")
    lines.append(f"Files with errors: {len(notes_with_errors)}")
    lines.append("")

    if notes_manifest_errors:
        lines.append("NOTES MANIFEST ISSUES")
        lines.append("-" * 30)
        for e in notes_manifest_errors:
            lines.append(f"  ⚠ {e}")
        lines.append("")

    if notes_with_errors:
        lines.append("NOTES FILE-LEVEL ISSUES")
        lines.append("-" * 30)
        for r in sorted(notes_with_errors, key=lambda x: x["file"]):
            lines.append(f"\n▶ {r['file']}  ({r['topic_count']} topic-blocks)")
            for e in r["errors"]:
                lines.append(f"    ✗ {e}")
    elif notes_results:
        lines.append("✅ No structural errors found in any notes/WA file.")

    lines.append("")
    lines.append("--- SQ/ FREE SAMPLES ---")
    lines.append(f"Files scanned: {len(sq_results)}")
    lines.append(f"Files with errors: {len(sq_with_errors)}")
    lines.append("")

    if sq_with_errors:
        lines.append("SQ FILE-LEVEL ISSUES")
        lines.append("-" * 30)
        for r in sorted(sq_with_errors, key=lambda x: x["file"]):
            lines.append(f"\n▶ {r['file']}")
            for e in r["errors"]:
                lines.append(f"    ✗ {e}")
    elif sq_results:
        lines.append("✅ No structural errors found in any SQ sample file.")

    lines.append("")
    lines.append("-" * 50)
    lines.append("Clean QB files: " + ", ".join(
        sorted(r["file"] for r in file_results if not r["errors"])
    ) if any(not r["errors"] for r in file_results) else "")
    lines.append("Clean notes files: " + ", ".join(
        sorted(r["file"] for r in notes_results if not r["errors"])
    ) if any(not r["errors"] for r in notes_results) else "")

    total_errors = len(files_with_errors) + len(manifest_errors) + len(notes_with_errors) \
        + len(notes_manifest_errors) + len(sq_with_errors)
    return "\n".join(lines), total_errors


def _safe_console_print(text):
    """Print text to stdout without crashing on consoles using a narrow
    codec (e.g. Windows cp1252) that can't encode report glyphs like
    checkmarks/warning signs, and without leaving stdout in a broken
    state for later prints.

    IMPORTANT: do NOT construct a new io.TextIOWrapper around
    sys.stdout.buffer here — TextIOWrapper takes ownership of the
    underlying buffer, and when the wrapper is garbage-collected it
    closes sys.stdout.buffer as a side effect, breaking every print()
    call for the rest of the process (raises "I/O operation on closed
    file"). Write bytes to the buffer directly instead, with no wrapper
    object left holding ownership.
    """
    try:
        print(text)
    except UnicodeEncodeError:
        encoding = getattr(sys.stdout, "encoding", None) or "utf-8"
        payload = (text + "\n").encode(encoding, errors="replace")
        sys.stdout.buffer.write(payload)
        sys.stdout.buffer.flush()


def send_email(subject, body):
    """Returns True if the report was actually emailed, False if it fell
    back to console printing (so callers don't double-print it)."""
    smtp_key = os.environ.get("BREVO_SMTP_KEY")
    if not SMTP_LOGIN or not smtp_key:
        _safe_console_print("BREVO_SMTP_LOGIN / BREVO_SMTP_KEY not set — printing report instead of emailing.\n")
        _safe_console_print(body)
        return False

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    context = ssl.create_default_context()
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls(context=context)
        server.login(SMTP_LOGIN, smtp_key)          # auth uses the SMTP relay login
        server.sendmail(EMAIL_FROM, [EMAIL_TO], msg.as_string())  # envelope/From uses the verified sender
    _safe_console_print(f"Email sent to {EMAIL_TO}")
    return True


def parse_args(argv=None):
    import argparse

    ap = argparse.ArgumentParser(
        prog="qb_health_check",
        description="QB + Notes health check. Scans remote main by default; "
                    "use --source local for a pre-merge regression check.")
    ap.add_argument("--source", choices=("remote", "local", "ref"), default="remote",
                    help="what to scan: remote main (default, as CI runs it), "
                         "the local working tree, or a git ref")
    ap.add_argument("--ref", default=None,
                    help="git ref for --source ref, e.g. origin/main")
    ap.add_argument("--no-email", action="store_true",
                    help="print the report; never send it")
    ap.add_argument("--json", dest="json_out", default=None,
                    help="also write a machine-readable result to this path")
    ap.add_argument("--fail-on-findings", action="store_true",
                    help="exit 1 when findings exist (off by default: the daily "
                         "job would be red every day on standing findings)")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    # A local or ref run is a developer/gate invocation, not the daily digest.
    # It must not mail the team unless explicitly told to.
    emailing = not args.no_email and (
        args.source == "remote" or os.environ.get("QB_ALWAYS_EMAIL"))

    print(f"Loading source: {args.source}"
          + (f" ({args.ref})" if args.ref else "") + " ...")
    try:
        files, source_info = load_source(args.source, args.ref)
    except Exception as e:
        message = f"Could not load the {args.source} source to run health checks.\n\nError: {e}"
        if emailing:
            send_email("🔴 MIW QB Health Check — FETCH FAILED", message)
        else:
            _safe_console_print(message)
        sys.exit(1)

    print(source_info.describe())

    known_traps = parse_known_traps(files.get(KNOWN_TRAPS_PATH))

    # Exclude SQ/ and oralnotes/ files here — they get dedicated handling via
    # check_sq_file() and check_notes_file() below, which know about their
    # different rules (e.g. SQ/ files are intentionally free/ungated and use
    # "index, follow" rather than the paywall noindex signature, and aren't
    # tracked in qb_content_index.json). Without this exclusion these files
    # were also run through the generic check_file() meant for meoclass1/
    # gated QB content, producing false-positive robots/manifest errors.
    html_files = {name: content for name, content in files.items()
                  if name.lower().endswith(".html")
                  and not name.startswith(SQ_FOLDER_PREFIX)
                  and not name.startswith(NOTES_FOLDER_PREFIX)}

    results = []
    for name, content in sorted(html_files.items()):
        results.append(check_file(name, content, all_files=files, known_traps=known_traps))

    # manifest check runs after file results so it can cross-check question counts
    manifest_errors, manifest_files = check_manifest(files, file_results=results)
    # index.html linkage: a file can be manifested and gated yet unreachable
    manifest_errors.extend(check_index_linkage(files, manifest_files))
    if known_traps == [] and KNOWN_TRAPS_PATH not in files:
        manifest_errors.append(
            f"{KNOWN_TRAPS_PATH} not found in repo — known-traps check skipped this run"
        )

    total_questions_manifest = sum(
        f.get("question_count", 0) for f in manifest_files.values()
    ) if manifest_files else "?"

    # --- Notes / WA series (oralnotes/) ---
    notes_files = {name[len(NOTES_FOLDER_PREFIX):]: content for name, content in files.items()
                   if name.startswith(NOTES_FOLDER_PREFIX) and name.lower().endswith(".html")}
    notes_results = []
    for name, content in sorted(notes_files.items()):
        notes_results.append(check_notes_file(name, content, known_traps=known_traps))
    notes_manifest_errors = check_notes_manifest(files, notes_results)

    # --- SQ/ free sample teasers ---
    sq_files = {name[len(SQ_FOLDER_PREFIX):]: content for name, content in files.items()
                if name.startswith(SQ_FOLDER_PREFIX) and name.lower().endswith(".html")}
    sq_results = []
    for name, content in sorted(sq_files.items()):
        main_copy = files.get(name) or files.get(NOTES_FOLDER_PREFIX + name)
        sq_results.append(check_sq_file(name, content, all_files=files, known_traps=known_traps,
                                          main_copy_bytes=main_copy))

    report, error_count = build_report(manifest_errors, results, len(html_files), total_questions_manifest,
                                        notes_manifest_errors=notes_manifest_errors, notes_results=notes_results,
                                        sq_results=sq_results)

    status = "🔴" if error_count else "✅"
    subject = f"{status} MIW QB + Notes Health Check — {error_count} issue(s) found" if error_count \
        else "✅ MIW QB + Notes Health Check — all clear"

    # Every run states what it scanned, so a finding count can never be
    # mistaken for evidence about a tree it did not read.
    banner = (
        "=" * 62 + "\n"
        + "HEALTH CHECK SOURCE\n"
        + source_info.describe() + "\n"
        + f"findings    : {error_count}\n"
        + "=" * 62 + "\n"
    )
    report = banner + "\n" + report

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as fh:
            json.dump({
                "source_type": source_info.source_type,
                "source": source_info.location,
                "commit": source_info.commit,
                "file_count": source_info.file_count,
                "findings": error_count,
            }, fh, indent=2, sort_keys=True)

    emailed = send_email(subject, report) if emailing else False
    if emailed or not emailing:
        _safe_console_print(report)

    # EXIT CONTRACT — deliberately unchanged for the daily job.
    #
    # There are ~369 standing findings, so exiting non-zero on findings would
    # turn the GitHub Action red every single day and train everyone to ignore
    # it. A successful scan exits 0; only a load failure exits 1. Callers that
    # genuinely want a hard gate opt in with --fail-on-findings, and a release
    # gate should compare finding SETS against a baseline rather than counts.
    return 1 if (error_count and args.fail_on_findings) else 0


if __name__ == "__main__":
    sys.exit(main())
