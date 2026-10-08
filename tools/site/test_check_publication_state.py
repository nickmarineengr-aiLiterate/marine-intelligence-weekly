#!/usr/bin/env python3
"""Publication-state checker self-tests (2026-10-08).

Every fixture below is a hand-written synthetic site, never a page sampled
from the corpus: a self-test harvested from live content stops discriminating
the moment that content changes, and does so silently.

Run:  python tools/site/test_check_publication_state.py
      (also collected by pytest)
"""
import os, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_publication_state as cps  # noqa: E402

ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))


# ---------------------------------------------------------------- fixtures

def make_site(d, latest=31, home_latest=None, home_count=None, archive_count=None,
              jsonld_count=None, badge=None, alt_issue=None, cover=None, brand_k=30,
              footer_latest=None, extra=None, numbered=None, short_on_hub=True,
              home_short='rfSRtGuUy_o', placeholder=False):
    """Write a minimal MIW-shaped site. Defaults are a consistent site whose
    latest numbered issue is `latest` (legacy 1-16 + root pages 17..latest)."""
    numbered = list(range(17, latest + 1)) if numbered is None else numbered
    count = 16 + len(numbered)
    home_latest = latest if home_latest is None else home_latest
    home_count = count if home_count is None else home_count
    archive_count = count if archive_count is None else archive_count
    jsonld_count = count if jsonld_count is None else jsonld_count
    badge = latest if badge is None else badge
    alt_issue = latest if alt_issue is None else alt_issue
    cover = latest if cover is None else cover
    footer_latest = latest if footer_latest is None else footer_latest
    prev = home_latest - 1

    def w(rel, text):
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(text)

    for n in numbered:
        w('index%d.html' % n, '<html><title>Issue %d</title></html>' % n)
        w('archive/issue%d.html' % n, '<html><title>Issue %d</title></html>' % n)
    w('archive/thematicmapissues01to16.html', '<title>Issues 01–16</title>')
    brand = ('Issues 1–%d were published as Marine Intelligence Weekly.' % brand_k)
    w('index.html', f'''<html><head>
<meta property="og:image" content="https://marineintelligenceweekly.com/assets/cover{cover}.webp">
<meta name="twitter:image" content="https://marineintelligenceweekly.com/assets/cover{cover}.webp">
<meta name="twitter:image:alt" content="MIW Issue {alt_issue} cover">
<script type="application/ld+json">{{"@type": "ItemList", "description": "list ({brand})", "numberOfItems": {jsonld_count}}}</script>
</head><body>
<div class="about-stat">Issues Published<strong>{home_count}</strong></div>
<a href="https://marineintelligenceweekly.com/index{home_latest}.html"><div>📰 Latest Issue</div><div>Issue {home_latest}</div></a>
<section id="latest" class="issues-section">
  <div class="issue-card-featured">
    <a href="https://marineintelligenceweekly.com/index{home_latest}.html" class="issue-card-featured-img"></a>
  </div>
  <!-- SPECIAL: Consolidated Brief. Unnumbered; not counted as an issue. -->
  <div>23 Jul → 30 Sep: what happened between Issue {prev} and Issue {home_latest}</div>
  <!-- YOUTUBE WALKTHROUGH SLOT — current MIW video -->
  <div>{"Issue walkthrough — Dropping Thursday" if placeholder else "Latest Short"}
    <a href="https://www.youtube.com/shorts/{home_short}">Watch</a></div>
</section>
<a href="https://marineintelligenceweekly.com/index{prev}.html" class="back-issue-card">
  <div class="back-issue-num">Issue {prev}</div></a>
<p>{brand}</p>
<div class="footer-links-label">Issues</div>
<a href="https://marineintelligenceweekly.com/index{footer_latest}.html">Issue {footer_latest} ← Latest</a>
<a href="https://marineintelligenceweekly.com/index{prev}.html">Issue {prev}</a>
</body></html>''')
    cards = ''.join(
        f'<a href="https://marineintelligenceweekly.com/index{n}.html" class="card">'
        + ('<span class="card-new">Latest in Archive</span>' if n == badge else '')
        + f'<div class="card-kicker">Issue {n}</div></a>\n'
        for n in sorted(numbered, reverse=True))
    w('archive/index.html', f'''<html><body>
<p class="hero-desc">Every MIW issue. {brand}</p>
<div class="stat">Issues published: <strong id="s-issues">{archive_count}</strong></div>
{cards}</body></html>''')
    hub_short = home_short if short_on_hub else 'zzzzzzzzzzz'
    w('youtube/index.html', f'<a href="https://www.youtube.com/shorts/{hub_short}">Short</a>')
    for rel, text in (extra or {}).items():
        w(rel, text)


def codes(d):
    return sorted({f.code for f in cps.check(d)})


def run_case(**kw):
    with tempfile.TemporaryDirectory() as d:
        make_site(d, **kw)
        return codes(d)


# ------------------------------------------------------------------- tests

def test_consistent_site_is_clean():
    assert run_case() == [], run_case()


def test_new_numbered_issue_updates_latest_correctly():
    # Issue 32 published and every surface moved: clean.
    assert run_case(latest=32) == []
    # Issue 32 page exists but the homepage still features 31: caught.
    got = run_case(latest=32, home_latest=31, footer_latest=31, badge=31,
                   alt_issue=31, cover=31)
    for c in ('HOME_FEATURED_NOT_LATEST', 'LATEST_LINK_STALE', 'ARCHIVE_BADGE_NOT_LATEST',
              'SOCIAL_COVER_NOT_LATEST', 'SOCIAL_ALT_NOT_LATEST'):
        assert c in got, (c, got)


def test_old_issue_remains_previous_issue():
    # Issue 30 as the back-issue card / plain footer link is never "latest".
    with tempfile.TemporaryDirectory() as d:
        make_site(d)
        inv = cps.inventory(d)
        assert inv['latest'] == 31 and inv['previous'] == 30, inv
        assert cps.check(d) == []


def test_special_brief_does_not_increment_numbered_issue():
    special = {'consolidated-jul-sep-2026.html':
               '<h1>What happened between Issue 30 and Issue 31</h1>'
               '<p>It is a special, not an issue.</p>'
               '<a href="/index30.html">← Issue 30</a>'}
    with tempfile.TemporaryDirectory() as d:
        make_site(d, extra=special)
        inv = cps.inventory(d)
        assert inv['latest'] == 31 and inv['count'] == 31, inv
        assert cps.check(d) == []


def test_standalone_article_does_not_change_latest_issue():
    art = {'articles/new-feature.html': '<h1>Feature</h1><a href="/index.html">Home</a>'}
    with tempfile.TemporaryDirectory() as d:
        make_site(d, extra=art)
        assert cps.inventory(d)['latest'] == 31
        assert cps.check(d) == []


def test_latest_video_does_not_change_latest_magazine_issue():
    with tempfile.TemporaryDirectory() as d:
        make_site(d, home_short='AbCdEfGhIjK')
        assert cps.inventory(d)['latest'] == 31
        assert cps.check(d) == []


def test_historical_issue_30_references_remain_intact():
    page = {'notes.html': '<p>Issue 30 covered MOL × IBM.</p>'
                          '<a href="/index30.html">Read Issue 30</a>'}
    assert run_case(extra=page) == []


def test_between_issue_30_and_31_is_not_flagged():
    page = {'brief.html': '<h1>What happened between Issue 30 and Issue 31</h1>'
                          '<a href="/index30.html">Issue 30</a>'}
    assert run_case(extra=page) == []


def test_brand_history_wording_is_not_falsely_flagged():
    # "Issues 1–30 were published as Marine Intelligence Weekly" is the brand
    # transition, not a count: it must survive Issue 31, 32, ...
    assert run_case(latest=32, brand_k=30) == []
    # A "helpful" bump to the running count is the actual error.
    assert 'BRAND_HISTORY_CHANGED' in run_case(brand_k=31)


def test_stale_homepage_current_link_is_caught():
    page = {'timeline.html': '<nav><a href="https://marineintelligenceweekly.com/index25.html">'
                             'Latest Issue</a></nav>'}
    assert 'LATEST_LINK_STALE' in run_case(extra=page)
    assert 'LATEST_LINK_STALE' in run_case(footer_latest=30)


def test_stale_latest_issues_list_label_is_caught():
    page = {'articles/index.html': '<div class="footer-links-label">Latest Issues</div>'
            '<a href="https://marineintelligenceweekly.com/index25.html">Issue 25</a>'
            '<a href="https://marineintelligenceweekly.com/index24.html">Issue 24</a>'}
    assert 'LATEST_LIST_STALE' in run_case(extra=page)
    ok = {'articles/index.html': '<div class="footer-links-label">Latest Issues</div>'
          '<a href="https://marineintelligenceweekly.com/index31.html">Issue 31</a>'
          '<a href="https://marineintelligenceweekly.com/index30.html">Issue 30</a>'}
    assert run_case(extra=ok) == []


def test_stale_issue_count_is_caught():
    assert 'COUNTER_MISMATCH' in run_case(home_count=30)
    assert 'COUNTER_MISMATCH' in run_case(archive_count=30)
    assert 'COUNTER_MISMATCH' in run_case(jsonld_count=30)


def test_count_uses_inventory_not_max_issue_number():
    # Numbering gap (no Issue 29): count is 30, latest is 31. Counters that
    # say 30 are right; the gap itself is surfaced for a human, not "fixed".
    nums = [n for n in range(17, 32) if n != 29]
    with tempfile.TemporaryDirectory() as d:
        make_site(d, numbered=nums)
        inv = cps.inventory(d)
        assert inv['count'] == 30 and inv['latest'] == 31, inv
        got = {f.code for f in cps.check(d)}
        assert 'COUNTER_MISMATCH' not in got, got
        assert 'NUMBERING_GAP' in got, got


def test_homepage_link_to_missing_issue_is_caught():
    assert 'MISSING_TARGET' in run_case(home_latest=32, footer_latest=32)


def test_archive_newer_than_homepage_is_caught():
    got = run_case(latest=32, home_latest=31, footer_latest=31, alt_issue=31, cover=31)
    assert 'HOME_FEATURED_NOT_LATEST' in got, got


def test_stale_placeholder_after_media_publication_is_caught():
    assert 'STALE_PLACEHOLDER' in run_case(placeholder=True)


def test_article_series_coming_soon_is_not_media_drift():
    # An unpublished article teaser outside the media slot is editorial, not media.
    with tempfile.TemporaryDirectory() as d:
        make_site(d)
        p = os.path.join(d, 'index.html')
        s = open(p, encoding='utf-8').read().replace(
            '</body>', '<div>Productivity Series · Part 2 · Coming Soon</div></body>')
        open(p, 'w', encoding='utf-8').write(s)
        assert cps.check(d) == [], cps.check(d)


def test_latest_short_must_exist_on_youtube_hub():
    assert 'SHORT_NOT_ON_HUB' in run_case(short_on_hub=False)


def test_real_repository_is_consistent():
    """The live tree must pass. This is the regression guard for the
    8 Oct 2026 drift fix; it reads the repository, not a fixture."""
    found = cps.check(ROOT)
    assert found == [], '\n'.join(str(f) for f in found)


if __name__ == '__main__':
    tests = [v for k, v in sorted(globals().items()) if k.startswith('test_')]
    failed = 0
    for fn in tests:
        try:
            fn(); print('PASS', fn.__name__)
        except AssertionError as e:
            failed += 1; print('FAIL', fn.__name__, '-', str(e)[:400])
    print('%d passed, %d failed' % (len(tests) - failed, failed))
    sys.exit(1 if failed else 0)
