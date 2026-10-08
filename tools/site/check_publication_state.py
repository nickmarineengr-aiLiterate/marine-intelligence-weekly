#!/usr/bin/env python3
"""MIW publication-state checker (2026-10-08).

Catches "latest issue" drift across the site after a publication: a surface
that still presents an older numbered issue as current, a counter that lags the
published inventory, a social card whose alt text names another issue, a stale
media placeholder, or a brand-history line bumped as if it were a count.

Run:   python tools/site/check_publication_state.py            (exit 1 on findings)
       python tools/site/check_publication_state.py --json
       python tools/site/check_publication_state.py --inventory-out FILE.json
Tests: python tools/site/test_check_publication_state.py

WHAT COUNTS AS "LATEST" (source-of-truth order, see tools/site/SKILL.md §2)
  The published numbered-issue inventory is read from the tree, not from prose:
    * Issues 1-16 from archive/thematicmapissues01to16.html (range in its title);
    * every root page indexN.html.
  latest   = max(inventory)
  count    = len(inventory)          -- NOT max: a numbering gap must not be
                                        papered over by a counter.
  Special Briefs, articles and videos are never numbered issues and are never
  in the inventory, so they cannot move "latest" or any counter.

CLASSIFICATION BY AFFORDANCE, NOT BY MENTION
  Only an anchor whose visible text says "latest" (or a list under a
  "Latest Issue(s)" label) is held to "must point at the latest issue". Prose
  such as "between Issue 30 and Issue 31", a back-issue card, or "Read Issue
  30" carries no such affordance and is never flagged. Frozen issue pages
  (indexN.html, archive/issueN.html) are historical by definition and are not
  scanned for latest-links.
"""
import argparse, html, json, os, re, sys
from collections import namedtuple

# Founder decision, 2 Oct 2026: Issue 31 is the first issue published as
# "MIW — Marine Intelligence". "Issues 1–30 were published as Marine
# Intelligence Weekly" is therefore a fixed brand-transition statement, not a
# running count, and must NOT follow later issues. Change only by Founder
# decision on the brand history.
LAST_LEGACY_BRAND_ISSUE = 30

SKIP_DIRS = {'.git', 'node_modules', 'tools', 'docs', 'reports', 'production-system',
             'engineering-reports', 'Claude skill', 'meoclass1', 'solvedQP', 'RulesApp'}
ISSUE_PAGE = re.compile(r'(^|/)(index\d+|archive/issue\d+)\.html$')
HOSTS = ('https://marineintelligenceweekly.com', 'https://www.marineintelligenceweekly.com',
         'http://marineintelligenceweekly.com')
ANCHOR = re.compile(r'<a\b([^>]*)>([\s\S]*?)</a>', re.I)
HREF = re.compile(r'\bhref\s*=\s*"([^"]*)"', re.I)
PLACEHOLDERS = re.compile(r'dropping thursday|coming soon|walkthrough\s+—\s+dropping|placeholder',
                          re.I)
YT_ID = re.compile(r'youtube\.com/(?:shorts/|watch\?v=|embed/)([A-Za-z0-9_-]{11})|'
                   r'youtu\.be/([A-Za-z0-9_-]{11})')

Finding = namedtuple('Finding', 'code path detail')
Finding.__str__ = lambda f: '%s  %s  %s' % (f.code, f.path, f.detail)


def _read(root, rel):
    p = os.path.join(root, rel)
    if not os.path.exists(p):
        return None
    with open(p, encoding='utf-8', errors='replace') as f:
        return f.read()


def issue_target(href):
    """Issue number an href points at (absolute, root- or archive-relative), else None."""
    h = (href or '').strip()
    if not h or h.startswith('#'):
        return None
    for host in HOSTS:
        if h.lower().startswith(host):
            h = h[len(host):]
            break
    h = h.split('#')[0].split('?')[0]
    m = re.search(r'(?:^|/)index(\d+)\.html$', h)
    return int(m.group(1)) if m else None


def visible(inner):
    t = re.sub(r'<[^>]+>', ' ', inner)
    return re.sub(r'\s+', ' ', html.unescape(t)).strip()


def anchors(text):
    for m in ANCHOR.finditer(text):
        h = HREF.search(m.group(1))
        yield (h.group(1) if h else ''), visible(m.group(2)), m.start()


def strip_noncontent(text):
    text = re.sub(r'<!--[\s\S]*?-->', ' ', text)
    return re.sub(r'<(script|style)\b[\s\S]*?</\1>', ' ', text, flags=re.I)


def public_pages(root):
    for dp, dn, fn in os.walk(root):
        rel_dir = os.path.relpath(dp, root).replace(os.sep, '/')
        dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith('wt-')]
        for f in fn:
            if f.endswith('.html'):
                rel = f if rel_dir == '.' else rel_dir + '/' + f
                yield rel


# --------------------------------------------------------------- inventory

def inventory(root):
    nums = set()
    legacy = _read(root, 'archive/thematicmapissues01to16.html') or ''
    m = re.search(r'Issues\s+0?(\d+)\s*[–—-]\s*0?(\d+)', legacy)
    if m:
        nums.update(range(int(m.group(1)), int(m.group(2)) + 1))
    for f in os.listdir(root):
        mm = re.fullmatch(r'index(\d+)\.html', f)
        if mm:
            nums.add(int(mm.group(1)))
    ordered = sorted(nums)
    latest = ordered[-1] if ordered else None
    return {
        'numbered': ordered,
        'latest': latest,
        'previous': ordered[-2] if len(ordered) > 1 else None,
        'count': len(ordered),
        'gaps': [n for n in range(1, (latest or 0) + 1) if n not in nums],
        'last_legacy_brand_issue': LAST_LEGACY_BRAND_ISSUE,
    }


# ------------------------------------------------------------------ checks

def check(root):
    inv = inventory(root)
    latest, count = inv['latest'], inv['count']
    out = []
    add = lambda code, path, detail: out.append(Finding(code, path, detail))
    if latest is None:
        return [Finding('NO_INVENTORY', '.', 'no numbered issue pages found')]
    if inv['gaps']:
        add('NUMBERING_GAP', '.', 'numbers missing from inventory: %s — counters use count=%d, '
            'latest=%d; confirm the gap is real' % (inv['gaps'], count, latest))

    home = _read(root, 'index.html') or ''
    arch = _read(root, 'archive/index.html') or ''

    # Homepage featured card.
    sec = re.search(r'<div class="issue-card-featured">([\s\S]*?)<!--', home)
    feat = [issue_target(h) for h, _, _ in anchors(sec.group(1))] if sec else []
    feat = [n for n in feat if n]
    if not feat:
        add('HOME_FEATURED_MISSING', 'index.html', 'no issue link in .issue-card-featured')
    elif feat[0] != latest:
        add('HOME_FEATURED_NOT_LATEST', 'index.html',
            'featured card links Issue %d; latest published is %d' % (feat[0], latest))

    # Archive badge.
    b = arch.find('Latest in Archive')
    if b >= 0:
        start = arch.rfind('<a ', 0, b)
        n = issue_target((HREF.search(arch[start:b]) or [None, ''])[1]) if start >= 0 else None
        if n != latest:
            add('ARCHIVE_BADGE_NOT_LATEST', 'archive/index.html',
                "'Latest in Archive' sits on Issue %s; latest is %d" % (n, latest))

    # Counters (lifetime published numbered issues).
    for path, text, rx in (
            ('index.html', home, r'Issues Published\s*<strong>(\d+)</strong>'),
            ('index.html', home, r'"numberOfItems"\s*:\s*(\d+)'),
            ('archive/index.html', arch, r'id="s-issues"[^>]*>(\d+)<')):
        for m in re.finditer(rx, text):
            if int(m.group(1)) != count:
                add('COUNTER_MISMATCH', path, '%s = %s; published inventory count is %d'
                    % (rx.split('\\')[0].strip('"'), m.group(1), count))

    # Social card on the homepage.
    for prop in ('og:image', 'twitter:image'):
        m = re.search(r'(?:property|name)="%s"\s+content="[^"]*cover(\d+)\.webp"' % prop, home)
        if m and int(m.group(1)) != latest:
            add('SOCIAL_COVER_NOT_LATEST', 'index.html',
                '%s uses cover%s.webp; latest is %d' % (prop, m.group(1), latest))
        a = re.search(r'(?:property|name)="%s:alt"\s+content="([^"]*)"' % prop, home)
        if a:
            for n in re.findall(r'Issue\s+(\d+)', a.group(1)):
                if int(n) != latest:
                    add('SOCIAL_ALT_NOT_LATEST', 'index.html',
                        '%s:alt names Issue %s; latest is %d' % (prop, n, latest))

    # Site-wide: anything labelled "latest" must point at the latest issue.
    for rel in public_pages(root):
        if ISSUE_PAGE.search(rel):
            continue
        text = _read(root, rel)
        for href, vis, _ in anchors(text):
            n = issue_target(href)
            if n is not None and re.search(r'\blatest\b|current issue', vis, re.I) and n != latest:
                add('LATEST_LINK_STALE', rel,
                    '"%s" -> index%d.html; latest is %d' % (vis[:60], n, latest))
        for m in re.finditer(r'>\s*Latest Issues?\s*</', text):
            first = next((issue_target(h) for h, _, _ in anchors(text[m.end():m.end() + 1500])
                          if issue_target(h)), None)
            if first is not None and first != latest:
                add('LATEST_LIST_STALE', rel,
                    "list under 'Latest Issue(s)' starts at Issue %d; latest is %d" % (first, latest))
        # Brand history is fixed, not a count.
        for m in re.finditer(r'Issues\s+0?1\s*[–—-]\s*(\d+)\s+were published as Marine '
                             r'Intelligence Weekly', text):
            if int(m.group(1)) != LAST_LEGACY_BRAND_ISSUE:
                add('BRAND_HISTORY_CHANGED', rel,
                    "brand-history line says 1–%s; the brand transition is fixed at 1–%d"
                    % (m.group(1), LAST_LEGACY_BRAND_ISSUE))

    # Same-site issue links on hubs must resolve.
    for rel in ('index.html', 'archive/index.html', 'youtube/index.html', 'articles/index.html'):
        text = _read(root, rel)
        if text is None:
            continue
        for href, _, _ in anchors(text):
            n = issue_target(href)
            if n is not None and not os.path.exists(os.path.join(root, 'index%d.html' % n)):
                add('MISSING_TARGET', rel, '%s -> index%d.html does not exist' % (href, n))

    # Media: placeholders and hub consistency. On the homepage only the media
    # slot is a media surface; "Coming Soon" on an article-series teaser is an
    # editorial decision, not media drift.
    hub = _read(root, 'youtube/index.html') or ''
    slot = re.search(r'<!-- YOUTUBE WALKTHROUGH[\s\S]*?(?=</section>|<!-- [A-Z])', home)
    for rel, text in (('index.html', slot.group(0) if slot else ''), ('youtube/index.html', hub)):
        for m in PLACEHOLDERS.finditer(strip_noncontent(text)):
            add('STALE_PLACEHOLDER', rel, 'visible placeholder text: "%s"' % m.group(0))
    if home.count('<!-- YOUTUBE WALKTHROUGH') != 1:
        add('YOUTUBE_ANCHOR', 'index.html', "expected exactly one '<!-- YOUTUBE WALKTHROUGH' "
            "comment (factory store_patch anchor); found %d" % home.count('<!-- YOUTUBE WALKTHROUGH'))
    hub_ids = {a or b for a, b in YT_ID.findall(hub)}
    for vid in sorted({a or b for a, b in YT_ID.findall(home)}):
        if vid not in hub_ids:
            add('SHORT_NOT_ON_HUB', 'index.html', 'homepage video %s is not listed on /youtube/' % vid)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split('\n')[0])
    ap.add_argument('--root', default=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--inventory-out')
    a = ap.parse_args(argv)
    inv = inventory(a.root)
    found = check(a.root)
    if a.inventory_out:
        with open(a.inventory_out, 'w', encoding='utf-8') as f:
            json.dump(inv, f, indent=2)
    if a.json:
        print(json.dumps({'inventory': inv, 'findings': [f._asdict() for f in found]}, indent=2))
    else:
        print('latest=%s previous=%s count=%s gaps=%s' % (inv['latest'], inv['previous'],
                                                         inv['count'], inv['gaps']))
        for f in found:
            print(f)
        print('%d finding(s)' % len(found))
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main())
