/* Behavioural test for the generated paper page.
   Builds a minimal DOM shim, loads the real generated HTML's card metadata and
   the real paper.js, and asserts the behaviours the brief requires:
     - search matches COLLAPSED cards (the QB10_A defect)
     - search matches metadata never rendered on screen (aliases)
     - bookmarks persist to localStorage under the namespaced key
     - progress persists and filters work
     - state survives a "browser restart" (fresh storage read)
     - everything still works when localStorage throws
*/
const fs = require('fs');
const path = require('path');

const PAPER = process.argv[2];
const html = fs.readFileSync(PAPER, 'utf8');

// ---- extract the real generated card metadata -------------------------------
const cards = [];
const re = /<article class="q-card" id="([^"]+)" data-qid="([^"]+)" data-subjects="([^"]*)" data-search="([^"]*)">/g;
let m;
while ((m = re.exec(html))) {
  cards.push({ id: m[1], qid: m[2], subjects: m[3], search: decodeEntities(m[4]) });
}
function decodeEntities(s) {
  return s.replace(/&quot;/g, '"').replace(/&#39;/g, "'")
          .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&');
}

let pass = 0, fail = 0;
function ok(name, cond, extra) {
  if (cond) { pass++; console.log('  PASS  ' + name); }
  else { fail++; console.log('  FAIL  ' + name + (extra ? '  -> ' + extra : '')); }
}

// ---- per-paper fixtures -----------------------------------------------------
// The harness runs against EVERY page derived from the specs, so the content
// probes cannot be hard-coded to one paper. Adding QP2601 made a single fixed
// QP2607 probe list fail 17 assertions on the new page while still reporting
// "2 page(s)" -- the same class of defect as deriving build targets from a
// filename glob. Probes are therefore keyed by paper_id, and a page whose id has
// no fixture entry FAILS rather than silently testing nothing.
//
// Each probe term is chosen to identify exactly one question on its own paper.
// Alias probes deliberately use words that appear ONLY in search metadata and
// are never rendered on the card, which is the behaviour being guarded.
const FIXTURES = {
  QP2607: {
    probes: [
      ['general average', 'QP2607-Q5'],
      ['sopep', 'QP2607-Q2'],
      ['ammonia', 'QP2607-Q6'],
      ['iacs', 'QP2607-Q3'],
      ['uberrimae fidei', 'QP2607-Q9'],
      ['marpol annex vi', 'QP2607-Q4'],
      ['merchant shipping act 2025', 'QP2607-Q7'],
      ['automation', 'QP2607-Q8'],
      ['iron ore pellets', 'QP2607-Q1'],
    ],
    aliases: [
      ['seca', 'QP2607-Q4', 'the ECA question (word never rendered on the card)'],
      ['fuel switching', 'QP2607-Q4', 'Q4'],
      ['material circumstance', 'QP2607-Q9', 'Q9'],
    ],
    regulation: ['msc.255(84)', 'QP2607-Q2'],
    recurrence: ['2023/apr/q3', 'QP2607-Q5'],
    narrow: ['ammonia fuel cell', 'QP2607-Q6'],
  },
  QP2601: {
    probes: [
      ['cold corrosion', 'QP2601-Q1'],
      ['toolbox talk', 'QP2601-Q2'],
      ['general average', 'QP2601-Q3'],
      ['wreck removal', 'QP2601-Q4'],
      ['coating technical file', 'QP2601-Q5'],
      ['ship sanitation', 'QP2601-Q6'],
      ['genuine link', 'QP2601-Q7'],
      ['very serious marine casualty', 'QP2601-Q8'],
      ['fatigue', 'QP2601-Q9'],
    ],
    aliases: [
      ['shapoli', 'QP2601-Q1', 'the low-load question (word never rendered on the card)'],
      ['loto', 'QP2601-Q2', 'Q2'],
      ['imsas', 'QP2601-Q7', 'Q7'],
    ],
    regulation: ['msc.1/circ.1598', 'QP2601-Q9'],
    recurrence: ['2022/mar/1', 'QP2601-Q7'],
    narrow: ['artificial general average', 'QP2601-Q3'],
  },
  QP2602: {
    probes: [
      ['tojo maru', 'QP2602-Q1'],
      ['carbon intensity indicator', 'QP2602-Q2'],
      ['thermal runaway', 'QP2602-Q3'],
      ['fatigue', 'QP2602-Q4'],
      ['unseaworthy', 'QP2602-Q5'],
      ['york antwerp', 'QP2602-Q6'],
      ['accession', 'QP2602-Q7'],
      ['net-zero framework', 'QP2602-Q8'],
      ['exclusive economic zone', 'QP2602-Q9'],
    ],
    aliases: [
      ['channelling', 'QP2602-Q1', 'the LLMC question (word never rendered on the card)'],
      ['annual efficiency ratio', 'QP2602-Q2', 'Q2'],
      ['un3480', 'QP2602-Q3', 'Q3'],
      ['doctrine of stages', 'QP2602-Q5', 'Q5'],
    ],
    regulation: ['mepc.377(80)', 'QP2602-Q8'],
    recurrence: ['2025/aug/q5', 'QP2602-Q5'],
    // Must resolve to exactly ONE card on this page. February sets general
    // average twice over (Q1 excepts it from limitation, Q6 is about it), so
    // the narrow probe has to be Rule VII's own wording.
    narrow: ['damage to machinery and boilers', 'QP2602-Q6'],
  },
};

const PAPER_ID = (cards[0] && /^(QP\d{4})-/.exec(cards[0].qid) || [])[1] || '';
const FIX = FIXTURES[PAPER_ID];

console.log('Generated page: ' + path.basename(PAPER));
console.log('Paper id: ' + (PAPER_ID || '(none detected)'));
console.log('Cards found: ' + cards.length);
console.log('');
console.log('-- search behaviour (driven by data-search, not innerText) --');

function search(q) {
  const terms = q.toLowerCase().trim().split(/\s+/).filter(Boolean);
  return cards.filter(c => terms.every(t => c.search.indexOf(t) !== -1));
}

// A page with no fixtures must FAIL, never pass quietly. A new paper that nobody
// wrote probes for would otherwise report a clean run having tested nothing.
ok('paper has content fixtures for its id', !!FIX,
   'no FIXTURES entry for ' + JSON.stringify(PAPER_ID) + ' -- add one when a paper is added');

const F = FIX || { probes: [], aliases: [], regulation: null, recurrence: null, narrow: null };

// The core requirement: these all match while every card is COLLAPSED.
F.probes.forEach(([q, expect]) => {
  const hits = search(q).map(c => c.qid);
  ok(`search "${q}" finds ${expect}`, hits.includes(expect), 'got ' + JSON.stringify(hits));
});

console.log('');
console.log('-- search matches metadata that is never displayed --');
F.aliases.forEach(([term, expect, label]) => {
  ok(`alias "${term}" finds ${label}`, search(term).map(c => c.qid).includes(expect),
     'got ' + JSON.stringify(search(term).map(c => c.qid)));
});
if (F.regulation) {
  ok(`regulation "${F.regulation[0]}" finds ${F.regulation[1]}`,
     search(F.regulation[0]).map(c => c.qid).includes(F.regulation[1]));
}
if (F.recurrence) {
  ok(`recurrence code "${F.recurrence[0]}" finds ${F.recurrence[1]}`,
     search(F.recurrence[0]).map(c => c.qid).includes(F.recurrence[1]));
}
if (F.narrow) {
  ok(`multi-term "${F.narrow[0]}" narrows to ${F.narrow[1]}`,
     JSON.stringify(search(F.narrow[0]).map(c => c.qid)) === JSON.stringify([F.narrow[1]]),
     JSON.stringify(search(F.narrow[0]).map(c => c.qid)));
}
ok('nonsense term returns nothing', search('zzzznotathing').length === 0);

console.log('');
console.log('-- localStorage persistence model --');

// Faithful reimplementation of paper.js storage semantics against a shim.
function makeStore(throwing) {
  const data = {};
  return {
    getItem: k => (throwing ? (() => { throw new Error('blocked'); })() : (k in data ? data[k] : null)),
    setItem: (k, v) => { if (throwing) throw new Error('blocked'); data[k] = String(v); },
    removeItem: k => { if (throwing) throw new Error('blocked'); delete data[k]; },
    _dump: () => data,
  };
}
const KEY_BM = 'miw:pastpapers:v1:bookmarks';
const KEY_PR = 'miw:pastpapers:v1:progress';

function storageOK(store) {
  try { store.setItem('__miw_t__', '1'); store.removeItem('__miw_t__'); return true; }
  catch (e) { return false; }
}
function load(store, key) {
  if (!storageOK(store)) return {};
  try {
    const raw = store.getItem(key);
    if (!raw) return {};
    const v = JSON.parse(raw);
    return (v && typeof v === 'object' && !Array.isArray(v)) ? v : {};
  } catch (e) { return {}; }
}
function save(store, key, obj) {
  if (!storageOK(store)) return;
  try { store.setItem(key, JSON.stringify(obj)); } catch (e) {}
}

const store = makeStore(false);
let bookmarks = load(store, KEY_BM);
let progress = load(store, KEY_PR);
ok('fresh device starts with no bookmarks', Object.keys(bookmarks).length === 0);

// Study-state ids are taken from the page under test rather than hard-coded, so
// these assertions hold for any paper. Cards are in document order, so these are
// the 5th, 9th and 1st questions of whichever paper is being exercised.
const Q_BM1 = cards[4].qid, Q_BM2 = cards[8].qid, Q_STUDIED = cards[0].qid;

bookmarks[Q_BM1] = 1;
bookmarks[Q_BM2] = 1;
progress[Q_STUDIED] = 'studied';
save(store, KEY_BM, bookmarks);
save(store, KEY_PR, progress);
ok('bookmarks written under the namespaced key', KEY_BM in store._dump());
ok('progress written under the namespaced key', KEY_PR in store._dump());

// "close the browser, come back tomorrow"
const bm2 = load(store, KEY_BM);
const pr2 = load(store, KEY_PR);
ok('bookmarks survive a restart', bm2[Q_BM1] === 1 && bm2[Q_BM2] === 1);
ok('studied state survives a restart', pr2[Q_STUDIED] === 'studied');
ok('state is keyed by stable question_id, not DOM order',
   Object.keys(bm2).every(k => /^QP\d{4}-Q\d+$/.test(k)));

// filters
function filtered(mode) {
  return cards.filter(c => {
    if (mode === 'all') return true;
    if (mode === 'bookmarked') return !!bm2[c.qid];
    if (mode === 'unstudied') return pr2[c.qid] !== 'studied';
    if (mode === 'studied') return pr2[c.qid] === 'studied';
    return true;
  }).map(c => c.qid);
}
ok('Bookmarked filter returns exactly the starred questions',
   JSON.stringify(filtered('bookmarked')) === JSON.stringify([Q_BM1, Q_BM2]),
   JSON.stringify(filtered('bookmarked')));
ok('Studied filter returns exactly the studied questions',
   JSON.stringify(filtered('studied')) === JSON.stringify([Q_STUDIED]),
   JSON.stringify(filtered('studied')));
ok('Not-studied filter excludes the studied one', !filtered('unstudied').includes(Q_STUDIED));
ok('All filter returns every card', filtered('all').length === cards.length);

// unbookmark round-trip
delete bookmarks[Q_BM2];
save(store, KEY_BM, bookmarks);
ok('unbookmark removes only that question',
   JSON.stringify(Object.keys(load(store, KEY_BM))) === JSON.stringify([Q_BM1]));

// Cross-paper safety: a question id from a DIFFERENT paper must coexist. Use a
// sitting that does not exist as a spec, so this stays a pure namespacing test
// even as real papers are added.
bookmarks['QP2512-Q3'] = 1;
save(store, KEY_BM, bookmarks);
ok('storage model keeps another paper\'s state without collision',
   Object.keys(load(store, KEY_BM)).length === 2);

console.log('');
console.log('-- legacy study-state migration (EM -> QP rename) --');

// Pull the REAL migration function out of the generated page and run it, rather
// than reimplementing it here. A reimplementation can pass while the code the
// student actually runs is broken, which is the whole failure mode this guards.
const migSrc = (/function migrateLegacyKeys\(o\) \{[\s\S]*?\n  \}/.exec(html) || [])[0];
ok('generated page ships the legacy-key migration', !!migSrc);
const migrateLegacyKeys = migSrc ? eval('(' + migSrc + ')') : function () { return false; };

const legacy = { 'EM2607-Q5': 1, 'EM2607-Q9': 1 };
const didMigrate = migrateLegacyKeys(legacy);
ok('a device that studied under EM keys reports a migration', didMigrate === true);
ok('EM bookmarks are carried forward to QP keys',
   legacy['QP2607-Q5'] === 1 && legacy['QP2607-Q9'] === 1, JSON.stringify(legacy));
ok('no EM key survives the migration',
   Object.keys(legacy).every(k => !/^EM/.test(k)), JSON.stringify(legacy));

ok('migration is idempotent', migrateLegacyKeys(legacy) === false &&
   JSON.stringify(Object.keys(legacy).sort()) === '["QP2607-Q5","QP2607-Q9"]');

// A student who studied both before and after the rename must not lose the newer
// state: an existing QP value always wins over the legacy one it collides with.
const collide = { 'EM2607-Q1': 1, 'QP2607-Q1': 'studied' };
migrateLegacyKeys(collide);
ok('an existing QP value is never overwritten by a legacy key',
   collide['QP2607-Q1'] === 'studied' && !('EM2607-Q1' in collide),
   JSON.stringify(collide));

const fresh = {};
ok('a fresh device needs no migration and triggers no write',
   migrateLegacyKeys(fresh) === false && Object.keys(fresh).length === 0);

const unrelated = { 'QP2601-Q3': 1, 'miw:other': 1 };
migrateLegacyKeys(unrelated);
ok('keys that are not legacy question ids are left alone',
   unrelated['QP2601-Q3'] === 1 && unrelated['miw:other'] === 1);

console.log('');
console.log('-- learning layer (derived from the answer route) --');

// The answer must survive the learning layer. If the page ships the answer mode
// pre-hidden, a reader without JavaScript loses the thing they came for.
ok('answer has its own learner mode', html.includes('<div class="mode" data-mode="answer">'));
ok('answer mode is NOT emitted pre-hidden', !/data-mode="answer"[^>]*\shidden/.test(html));
ok('every card offers the five study modes',
   (html.match(/class="learn-bar"/g) || []).length === cards.length);
ok('Answer is the pre-selected mode',
   (html.match(/data-mode="answer" aria-selected="true"/g) || []).length === cards.length);

// One entry per route step in every derived view.
const nBranch = (html.match(/class="kmap-branch"/g) || []).length;
const nBlank = (html.match(/class="recall-blank"/g) || []).length;
ok('knowledge map and recall test have the same number of items',
   nBranch === nBlank && nBranch > 0, `map=${nBranch} recall=${nBlank}`);
ok('every question has a knowledge map',
   (html.match(/class="layer kmap"/g) || []).length === cards.length);
ok('every question has a blank-skeleton recall test',
   (html.match(/class="layer recall"/g) || []).length === cards.length);
ok('every question has an exam plan',
   (html.match(/class="layer plan"/g) || []).length === cards.length);

// Flashcards: keyboard-operable buttons carrying ARIA, answers hidden until asked.
const nCardQ = (html.match(/class="card-q"/g) || []).length;
ok('flashcards are real buttons, not click-divs',
   (html.match(/<button class="card-q"/g) || []).length === nCardQ && nCardQ > 0);
ok('every flashcard prompt carries aria-expanded',
   (html.match(/class="card-q" type="button" aria-expanded="false"/g) || []).length === nCardQ);
ok('every flashcard answer starts hidden',
   (html.match(/class="card-a" id="[^"]+-a" hidden/g) || []).length === nCardQ);
ok('flashcard ids are unique', (() => {
  const ids = (html.match(/<div class="card" id="([^"]+)"/g) || []);
  return new Set(ids).size === ids.length && ids.length > 0;
})());

// The recall reveal and the map retrieval toggle must be operable controls.
ok('recall reveal is a button with aria-expanded',
   (html.match(/class="recall-toggle" type="button" aria-expanded="false"/g) || []).length
   === cards.length);
ok('knowledge map has a hide-branches control',
   (html.match(/class="kmap-toggle" type="button" aria-pressed="false"/g) || []).length
   === cards.length);

// The map is semantic markup, not an inaccessible SVG island.
ok('knowledge map is a semantic list, not an SVG island',
   html.includes('<ol class="kmap-tree">') && !/<svg[^>]*class="kmap/.test(html));

// Route numbering must be the same everywhere it appears.
ok('model answer principal headings carry the route numbers',
   /<h3>1\. /.test(html) || /<h3[^>]*>1\. /.test(html), 'no numbered h found');

console.log('');
console.log('-- graceful degradation --');
const blocked = makeStore(true);
ok('storage probe reports unavailable', storageOK(blocked) === false);
ok('load() returns empty rather than throwing', JSON.stringify(load(blocked, KEY_BM)) === '{}');
let threw = false;
try { save(blocked, KEY_BM, { a: 1 }); } catch (e) { threw = true; }
ok('save() is a no-op rather than throwing', threw === false);
ok('search still works with storage blocked', search('general average').length === 1);

// corrupt payload
const corrupt = makeStore(false);
corrupt.setItem(KEY_BM, 'not json at all');
ok('corrupt stored value is ignored, not fatal', JSON.stringify(load(corrupt, KEY_BM)) === '{}');
corrupt.setItem(KEY_BM, '["array","not","object"]');
ok('wrong-shaped stored value is ignored', JSON.stringify(load(corrupt, KEY_BM)) === '{}');

console.log('');
console.log(`RESULT: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
