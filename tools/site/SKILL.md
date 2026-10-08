---
name: miw-site-publication
version: 1.1
updated: 2026-10-08
description: >
  Cross-surface website maintenance for marineintelligenceweekly.com whenever MIW publishes a
  numbered magazine issue, a Special Brief, a standalone feature article, a reference-series update,
  or a video/Short. It decides what "latest", "previous" and every counter mean, and it lists every
  surface that has to move together. It ships with a checker (tools/site/check_publication_state.py)
  that fails on drift. Load it before touching index.html, archive/index.html, youtube/index.html,
  articles/index.html or any page carrying a "Latest Issue" control, and after every publication.
---

# MIW Site Publication — Update Skill v1.1

## 0. TL;DR

```
python tools/site/check_publication_state.py          # must print "0 finding(s)"; exit 1 = drift
python tools/site/test_check_publication_state.py     # checker self-tests (synthetic fixtures)
node --test tools/security/*.test.mjs                 # site, archive, navigation, link, security suite
# factory repo (MIW-Magazine-Production), before any numbered release:
python tools/store_patch_publication_state_test.py --store <STORE checkout> --rev origin/main   # synthetic next issue, end to end
```

Run the checker **before** you edit, to get the baseline, and **after** you edit, to prove the result.
A numbered issue is not done until the checker is clean on the candidate **and** on the live site
after deployment (§8).

Why this skill exists: on 8 Oct 2026, one day after Issue 31 went live, seven current-facing surfaces
were still stale. The homepage counter said 30 and the Twitter-card alt text named Issue 30. Three
"Latest Issue" links pointed at Issues 25 and 22, and the articles hub's "Latest Issues" footer
started at Issue 25. The release patch updated only the paths it knew about. The rest of this
skill lists every surface involved and makes the checker enforce them.

**v1.1 (closure sprint, 8 Oct 2026):** the factory `store_patch.py` now owns all seven of those
surfaces (rows marked **SP** in §3) and, after `--apply`, runs this checker on the patched STORE
tree and exits 1 on any finding. A replay of the real Issue 31 release through the fixed patch
reproduces the hand-fixed state (STORE `db5a123`) byte-for-byte. The nav surfaces had drifted
since Issue 25. The fixed patch **refuses** to stack a release on such pre-existing drift, so
fix the drift (or re-run this checker) before patching, and never edit around a refusal.

This skill is about the **state** of the publication across the site. Other skills cover how a
page is written and built:

| Need | Use |
|---|---|
| Write or build the issue page itself (indexN.html) | factory repo `MIW-Magazine-Production` (`build_issue.py`, `store_patch.py`, release gate) |
| Archive card markup, filter tags | user skill `miw-archive` (card HTML, `card-new` badge steps) |
| Notes / QB / Oral / Written lanes | `tools/notes/SKILL.md`, `tools/oral/SKILL.md` and their own skills (never touched by this skill) |

## 1. Vocabulary — keep these separate

| Term | Meaning | Changes when |
|---|---|---|
| **Content publication** | The page exists and is reachable (indexN.html, an article page, a brief page). | Any publication |
| **Homepage promotion** | A slot on `/` features the item (featured issue card, Special panel, Feature slot, media slot). | Editorial choice |
| **Archive insertion** | The item gets a card/entry in `/archive/` (numbered issues; specials only if chosen). | Numbered issue (always), others optional |
| **Latest** | The highest-numbered **published numbered issue**. Nothing else is ever "Latest Issue". | Numbered issue only |
| **Previous** | The numbered issue immediately before Latest (the first back-issue card). | Numbered issue only |
| **Counter** | "Issues Published", archive `#s-issues`, JSON-LD `numberOfItems` = the **count** of published numbered issues. | Numbered issue only |
| **Brand history** | "Issues 1–30 were published as Marine Intelligence Weekly". This is a fixed fact, not a count. | Founder brand decision only |
| **Media latest** | The newest video/Short in the homepage media slot and on `/youtube/`. Unrelated to the magazine's Latest. | Video/Short publication |

### Never increment a number blindly

Before changing any number on the site, decide which kind of number it is:

1. **Lifetime published count** ("Issues Published", `#s-issues`, `numberOfItems`). Set it to `len(inventory)`.
2. **Current-brand count.** None is displayed today. Issues under "MIW — Marine Intelligence" start at 31.
3. **Archived-series count/range** ("Issues 01–16" thematic map; homepage footer "Archive (Issues 01–26)").
   This is a range. It changes only when the series it names changes.
4. **Previous-issue number** ("Previous Issue: Issue 30", "← Issue 30"). It stays with the page it was published on.
5. **Brand-transition boundary** ("Issues 1–30 …"). It never follows new issues (§6).

Count is **not** max. If numbering ever has a gap, or an unnumbered item is mistaken for an issue,
`count ≠ latest`. The checker reports `NUMBERING_GAP` so a person decides; nothing is "fixed" automatically.

## 2. Source of truth (highest first)

1. **Published content page / release manifest.** `indexN.html` exists at the root (and the factory release
   record for that issue). Issues 1–16 come from the title range of `archive/thematicmapissues01to16.html`.
2. **Issue / article metadata.** The page's own title, date and canonical URL.
3. **Archive / index registry.** `archive/index.html` cards, the `Latest in Archive` badge and `#s-issues`.
4. **Homepage promotion surfaces.** Featured card, back-issue grid, footer list, stats strip, JSON-LD.

Lower levels follow higher ones. Never derive "latest" from prose ("our most recent issue …"). The
checker derives `latest`, `previous` and `count` from level 1 only.

## 3. A — New numbered magazine issue N

The factory `store_patch.py` writes the rows marked **SP** below with exact-once anchored edits,
then runs this checker on the candidate tree. Rows without **SP** are hand-maintained or N/A and
**must still be audited**. If a new current-facing surface is added to the site, either add it to
`store_patch.PAGE_PATCHES` (with a refusal on unexpected state) or the post-apply checker will
refuse the next release. That refusal is intended.

| # | Surface | Where (search anchor) | Action for issue N |
|---|---|---|---|
| 1 | Issue page **SP** | `indexN.html` | Built by the factory; canonical URL = root page |
| 2 | Archive copy **SP** | `archive/issueN.html` | Verbatim twin of root (archive_continuity tests) |
| 3 | Archive card **SP** | `archive/index.html` `<!-- ISSUE N -->` | Insert above N−1 (miw-archive skill) |
| 4 | Homepage Latest block **SP** | `index.html` `<!-- LATEST ISSUE -->` → `.issue-card-featured` | Link, cover, alt, kicker date, title, desc, topics, Read button → N |
| 5 | Previous issues list **SP** | `index.html` `.back-issue-card` grid | N−1 becomes the first back-issue card |
| 6 | Issue counter (home) **SP** | `index.html` `Issues Published<strong>` | = published count |
| 7 | Latest badge/label (home) **SP** | "📰 Latest Issue" start-here card; footer `← Latest` | → N; exactly one `← Latest` |
| 8 | Canonical URL | `indexN.html` `<link rel="canonical">` | Root URL, also on the archive twin |
| 9 | Nav links **SP** | every `Latest Issue` nav/footer link site-wide (`timeline.html`, `articles/timeline-article.html`, `GHGDecarb/timeline.html`, `articles/index.html` "Latest Issues") | → N (checker: `LATEST_LINK_STALE`, `LATEST_LIST_STALE`) |
| 10 | Issue date | Featured kicker, archive kicker, footer label | The publication date in the release record |
| 11 | OG/Twitter metadata **SP** | `index.html` `og:image`, `twitter:image` and both `:alt` | `coverN.webp`; an alt that names "Issue N−1" → N (refused if it names any other issue); a brand-level alt that names no issue is left alone |
| 12 | Structured data **SP** | `index.html` ItemList (`numberOfItems`, positions), BreadcrumbList | N at position 1; `numberOfItems` = count |
| 13 | Sitemap | none today (`/sitemap.xml` 404) | N/A. See §9 FUTURE_ARCHITECTURE_RECOMMENDATION |
| 14 | RSS/feed | none today (`/feed.xml` 404) | N/A |
| 15 | Archive "latest" marker **SP** | `archive/index.html` `card-new` "Latest in Archive" | Move from N−1 to N; exactly one |
| 16 | Prev/next navigation | `indexN.html` must link ← N−1 | **No forward link on N−1.** House convention, asserted by `issue_navigation.test.mjs` |
| 17 | Issue cover asset **SP** | `assets/coverN.webp` | Present; used by featured card and social card |
| 18 | Mobile cover variant **SP** | `assets/*_N_mobile.webp` (in-issue visuals) | Present for every desktop visual |
| 19 | Homepage share image **SP** | `og:image`/`twitter:image` (the same file as #11 today) | coverN |
| 20 | Article/feature hub **SP** | `articles/index.html` footer "Latest Issues" | N, N−1, N−2 |
| 21 | YouTube companion | `index.html` `<!-- YOUTUBE WALKTHROUGH` slot | Change only if a companion video exists (§7); keep the comment prefix |
| 22 | "Issues 1–N" copy | none should exist except the brand line | Do not invent one |
| 23 | Brand-history copy | 4 places (§6) | **Do not change** |
| 24 | Search/index manifests | none for magazine issues (`notes_content_index.json` is Notes-only) | N/A |
| 25 | Tests | `archive_continuity` + `issue_navigation` issue lists; `regulatory_facts` current-issue dateline; checker | Add N / update the dateline; run everything |
| 26 | Production verification | §8 | Live checker = 0 findings |

Leave these alone when N is published: Issue N−1's own page (including its "Next Issue" teaser box,
which is published text and not a link), archive entries for older issues, and editorial references
to earlier issues inside issue N.

## 4. B — Special Brief (unnumbered)

A Special Brief is **not** a numbered issue. Publishing one must **never**:
- increment any counter (§1);
- change Latest or Previous;
- move or renumber archive cards;
- relabel or move "Latest Issue" anywhere.

It **may**:
- add a homepage Special panel inside `#latest`, below the featured card, marked
  `<!-- SPECIAL: … Unnumbered; not counted as an issue. -->`. The factory `store_patch.py` must preserve it
  byte-for-byte;
- add an archive or special entry (only without the `card-new` Latest badge);
- update a feature or reference hub;
- add a video companion (§7);
- set its own page metadata.

A published brief is approval-bound and dated. Text such as "Next · Issue 31 · planned 7 October"
was true on its date. Any later change goes through the factory **SPECIAL_REISSUE** gate with Founder
approval. It is never edited in place to "keep it current".

## 5. C/D — Standalone feature article and reference-series update

Required for an article:
1. Canonical article page under `articles/`.
2. A card in the `articles/index.html` hub.
3. Optionally the homepage Feature slot.
4. Metadata and OG image on the article page.
5. Internal links from related pages.

For a reference series (e.g. `timeline.html`, `GHGDecarb/timeline.html`, `ecosystem.html`), add a reference card where applicable.

**No** numbered-issue counter change. **No** change to Latest. If the article page carries a
"Latest Issue" nav link (the timeline pages do), it must point at the current Latest. The checker
enforces this.

## 6. Brand history — fixed, not a count

"Issues 1–30 were published as Marine Intelligence Weekly." appears in:
- `index.html` JSON-LD ItemList `description`;
- `index.html` Organization `description`;
- `index.html` About section;
- the `archive/index.html` hero.

Founder decision (2 Oct 2026): Issue 31 is the first issue published as
**MIW — Marine Intelligence**. So "1–30" is the brand boundary, and it stays at 30 for Issue 32, 33,
and later issues. The checker constant `LAST_LEGACY_BRAND_ISSUE = 30` fails any "helpful" bump
(`BRAND_HISTORY_CHANGED`). The constant and these four lines change only on a new Founder brand
decision.

## 7. E — Video / Short

When a new MIW video or Short is published, audit:
- the homepage media slot (`<!-- YOUTUBE WALKTHROUGH` …; exactly one such comment, because the factory anchors on it);
- `/youtube/` (the new item first);
- no stale "coming soon" or "Dropping Thursday" text in either media surface;
- thumbnail (`img.youtube.com/vi/<ID>/…`), title and YouTube ID (11 chars);
- channel link `@MarineIntelligenceWeekly`;
- the deep link to the related issue or brief;
- no obsolete placeholder, no duplicate embed, no broken link.

Every video ID on the homepage must also appear on `/youtube/` (checker: `SHORT_NOT_ON_HUB`).

A newer video does **not** replace magazine content and does **not** change Latest Issue. Editorial
"Coming Soon" teasers outside the media slot (e.g. Productivity Series Parts 2–3) are editorial
decisions, not media drift. The checker deliberately ignores them.

## 8. Release discipline (website)

1. Branch or worktree from current `origin/main`. Never work in a recovery clone. No direct `main` mutation.
2. Baseline: run the checker and the node suite on the untouched branch, and record the counts.
3. Make the minimal edits. Each one is an exact string match; preserve line endings.
4. Re-run everything. Any per-test outcome that differs from baseline blocks landing.
5. Compare live and candidate. Fetch every changed page from production, then diff it against the candidate. Only the
   intended lines may differ, and every untouched surface must be byte-identical to live.
6. Founder landing approval → Founder (or Lane A) pushes. Claude does not push `main` or deploy.
7. After the deployment is READY, fetch the live pages again and run the checker on a fresh clone of the
   deployed SHA. It must report 0 findings.
8. Social/LinkedIn handoff is a separate, Founder-authorised step. Website state never triggers a post.

## 9. FUTURE_ARCHITECTURE_RECOMMENDATION (not implemented; needs a decision)

- **Publication registry.** Add a small `publications.json` (id, type issue|special|article|video,
  number, date, url, cover), written by the factory at release time. The homepage, archive and
  checker would read it instead of inferring state from pages. This is not introduced now: it would
  change the factory contract.
- ~~**Factory `store_patch.py` coverage.**~~ DONE in v1.1 (closure sprint, 8 Oct 2026): stats strip,
  share-image alt, timeline "Latest Issue" links, articles-hub list, and the post-apply checker gate.
  The Special Brief path (`consolidated_store_patch.py`) now also refuses a change to the visible
  "Issues Published" counter.
- **Sitemap.** No `sitemap.xml` exists. Adding one (public pages only; `meoclass1/` and `solvedQP/`
  are noindex) would need its own small spec and test.
- **User-level skills** (`miw-production`, `marine-intelligence-weekly`) still say "update stats on
  homepage if needed". Point them at this file.
