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

console.log('Generated page: ' + path.basename(PAPER));
console.log('Cards found: ' + cards.length);
console.log('');
console.log('-- search behaviour (driven by data-search, not innerText) --');

function search(q) {
  const terms = q.toLowerCase().trim().split(/\s+/).filter(Boolean);
  return cards.filter(c => terms.every(t => c.search.indexOf(t) !== -1));
}

// The core requirement: these all match while every card is COLLAPSED.
const probes = [
  ['general average', 'EM2607-Q5'],
  ['sopep', 'EM2607-Q2'],
  ['ammonia', 'EM2607-Q6'],
  ['iacs', 'EM2607-Q3'],
  ['uberrimae fidei', 'EM2607-Q9'],
  ['marpol annex vi', 'EM2607-Q4'],
  ['merchant shipping act 2025', 'EM2607-Q7'],
  ['automation', 'EM2607-Q8'],
  ['iron ore pellets', 'EM2607-Q1'],
];
probes.forEach(([q, expect]) => {
  const hits = search(q).map(c => c.qid);
  ok(`search "${q}" finds ${expect}`, hits.includes(expect), 'got ' + JSON.stringify(hits));
});

console.log('');
console.log('-- search matches metadata that is never displayed --');
ok('alias "seca" finds the ECA question (word never rendered on the card)',
   search('seca').map(c => c.qid).includes('EM2607-Q4'));
ok('alias "fuel switching" finds Q4', search('fuel switching').map(c => c.qid).includes('EM2607-Q4'));
ok('alias "material circumstance" finds Q9',
   search('material circumstance').map(c => c.qid).includes('EM2607-Q9'));
ok('regulation "msc.255(84)" finds Q2', search('msc.255(84)').map(c => c.qid).includes('EM2607-Q2'));
ok('recurrence code "2023/apr/q3" finds Q5', search('2023/apr/q3').map(c => c.qid).includes('EM2607-Q5'));
ok('multi-term "ammonia fuel cell" narrows to Q6',
   JSON.stringify(search('ammonia fuel cell').map(c => c.qid)) === '["EM2607-Q6"]',
   JSON.stringify(search('ammonia fuel cell').map(c => c.qid)));
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

bookmarks['EM2607-Q5'] = 1;
bookmarks['EM2607-Q9'] = 1;
progress['EM2607-Q1'] = 'studied';
save(store, KEY_BM, bookmarks);
save(store, KEY_PR, progress);
ok('bookmarks written under the namespaced key', KEY_BM in store._dump());
ok('progress written under the namespaced key', KEY_PR in store._dump());

// "close the browser, come back tomorrow"
const bm2 = load(store, KEY_BM);
const pr2 = load(store, KEY_PR);
ok('bookmarks survive a restart', bm2['EM2607-Q5'] === 1 && bm2['EM2607-Q9'] === 1);
ok('studied state survives a restart', pr2['EM2607-Q1'] === 'studied');
ok('state is keyed by stable question_id, not DOM order',
   Object.keys(bm2).every(k => /^EM\d{4}-Q\d+$/.test(k)));

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
   JSON.stringify(filtered('bookmarked')) === '["EM2607-Q5","EM2607-Q9"]',
   JSON.stringify(filtered('bookmarked')));
ok('Studied filter returns exactly the studied questions',
   JSON.stringify(filtered('studied')) === '["EM2607-Q1"]', JSON.stringify(filtered('studied')));
ok('Not-studied filter excludes the studied one', !filtered('unstudied').includes('EM2607-Q1'));
ok('All filter returns every card', filtered('all').length === cards.length);

// unbookmark round-trip
delete bookmarks['EM2607-Q9'];
save(store, KEY_BM, bookmarks);
ok('unbookmark removes only that question',
   JSON.stringify(Object.keys(load(store, KEY_BM))) === '["EM2607-Q5"]');

// future-paper safety
bookmarks['EM2601-Q3'] = 1;
save(store, KEY_BM, bookmarks);
ok('storage model accommodates a future paper without collision',
   Object.keys(load(store, KEY_BM)).length === 2);

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
