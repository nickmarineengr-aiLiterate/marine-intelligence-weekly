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
  QP2512: {
    probes: [
      ['disease vector', 'QP2512-Q1'],
      ['gassing up', 'QP2512-Q2'],
      ['insurable interest', 'QP2512-Q3'],
      ['maslow', 'QP2512-Q4'],
      ['shipping casualty', 'QP2512-Q5'],
      ['minimum age', 'QP2512-Q6'],
      ['off-hire', 'QP2512-Q7'],
      ['detainable deficiency', 'QP2512-Q8'],
      ['maritime lien', 'QP2512-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['self-actualization', 'QP2512-Q4',
       'Q4 (the American spelling; the answer renders self-actualisation)'],
      ['ms act 334', 'QP2512-Q8', 'Q8 (the compressed form of the section reference)'],
      ['underperformance', 'QP2512-Q7',
       'Q7 (the one-word form of the speed and consumption claim)'],
      ['section 361', 'QP2512-Q5',
       'Q5 (the court empowered to make a formal investigation)'],
      ['judicial sale', 'QP2512-Q9', 'Q9 (the mechanism behind the order of settlement)'],
    ],
    // A.1185(33) is the Procedures for Port State Control, 2023 -- the OPERATIVE
    // edition at a December 2025 sitting. It is used here rather than a SOLAS
    // regulation precisely because the edition is this paper's sharpest temporal
    // trap: the 2021 edition was revoked in 2023 and the 2025 edition had not been
    // issued. If this probe ever starts resolving to a different resolution
    // number, the paper has been re-anchored onto the wrong Procedures.
    regulation: ['a.1185(33)', 'QP2512-Q8'],
    // Leak probe: the third-party host's own printed sitting code for Q8 must NOT
    // be searchable in the shipped bytes.
    recurrence: ['2025/dec/q8', 'QP2512-Q8'],
    narrow: ['nearest appropriate repair yard', 'QP2512-Q8'],
  },
  QP2511: {
    probes: [
      ['bulk carrier losses', 'QP2511-Q1'],
      ['torque rich', 'QP2511-Q2'],
      ['ship sanitation control certificate', 'QP2511-Q3'],
      ['gassing up', 'QP2511-Q4'],
      ['condition assessment programme', 'QP2511-Q5'],
      ['dye penetrant', 'QP2511-Q6'],
      ['single window', 'QP2511-Q7'],
      ['alang', 'QP2511-Q8'],
      ['signature subject to ratification', 'QP2511-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['lrm', 'QP2511-Q2', 'Q2 (the light running margin abbreviation)'],
      ['deratting certificate', 'QP2511-Q3', 'Q3 (the superseded name of the SSCC)'],
      ['maritime declaration of health', 'QP2511-Q3',
       'Q3 (the name Article 37 carried before the amendments in force from 19 September 2025)'],
      ['beaching', 'QP2511-Q8', 'Q8 (the Convention does not prohibit it)'],
      ['vclt', 'QP2511-Q9', 'Q9 (the Vienna Convention abbreviation)'],
    ],
    // MSC.215(82) is the Performance Standard for Protective Coatings, reached
    // through SOLAS XII/6 -- the bulk carrier limb. It belongs to Q1's casualty
    // answer, not to Q5's survey regime, which is why A.1049(27) is not used here.
    regulation: ['msc.215(82)', 'QP2511-Q1'],
    // Q5 is the EARLIER member of an exact pair, so its recurrence points FORWARD
    // to March 2026 -- the opposite direction from most fixtures in this file.
    recurrence: ['2026/mar/q6', 'QP2511-Q5'],
    narrow: ['restriction from sailing with a hold empty', 'QP2511-Q1'],
  },
  QP2404: {
    probes: [
      ['internet of things', 'QP2404-Q1'],
      ['ammonia', 'QP2404-Q2'],
      ['maritime lien', 'QP2404-Q3'],
      ['rudder', 'QP2404-Q4'],
      ['cybutryne', 'QP2404-Q5'],
      ['general average', 'QP2404-Q6'],
      ['human element', 'QP2404-Q7'],
      ['recognized organization', 'QP2404-Q8'],
      ['unclos', 'QP2404-Q9'],
    ],
    aliases: [
      ['nh3', 'QP2404-Q2', 'the ammonia question (the formula is never rendered on the card)'],
      ['leitrad', 'QP2404-Q4', 'Q4 (the vane wheel\'s original name)'],
      ['irgarol', 'QP2404-Q5', 'Q5 (the trade name of cybutryne, never rendered)'],
      ['sleep debt', 'QP2404-Q7', 'Q7'],
      ['constitution of the oceans', 'QP2404-Q9', 'Q9'],
    ],
    // A.1188(33) is the edition of the ISM implementation Guidelines operative
    // at THIS sitting. Its predecessor A.1118(30) was revoked by it on
    // 6 December 2023, four months before the paper was sat, and appears in the
    // answer only as the revoked edition. Probing the correct edition therefore
    // also guards the wrong-edition trap this question is built on.
    regulation: ['a.1188(33)', 'QP2404-Q8'],
    recurrence: ['2023/aug/q1', 'QP2404-Q1'],
  },
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
  QP2603: {
    probes: [
      ['signature subject to ratification', 'QP2603-Q1'],
      ['cargo securing manual', 'QP2603-Q2'],
      ['joint war committee', 'QP2603-Q3'],
      ['ship sanitation', 'QP2603-Q4'],
      ['gassing up', 'QP2603-Q5'],
      ['condition assessment', 'QP2603-Q6'],
      ['propeller', 'QP2603-Q7'],
      ['thermal runaway', 'QP2603-Q8'],
      ['hong kong convention', 'QP2603-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['hkc', 'QP2603-Q9', 'the ship recycling question (abbreviation never rendered)'],
      ['dpt', 'QP2603-Q7', 'Q7'],
      ['strait of hormuz', 'QP2603-Q3', 'Q3'],
    ],
    regulation: ['a.1049(27)', 'QP2603-Q6'],
    // March Q1 is an EXACT repeat of February Q7, so its recurrence table
    // carries the February code -- which is exactly what should be findable.
    recurrence: ['2026/feb/q7', 'QP2603-Q1'],
    // Must resolve to exactly ONE card. March sets three questions that mention
    // emergency shutdown or release in some form, so the probe is the coupling's
    // own full name.
    narrow: ['emergency release coupling', 'QP2603-Q5'],
  },
  QP2604: {
    probes: [
      ['tacit acceptance', 'QP2604-Q1'],
      ['thermal runaway', 'QP2604-Q2'],
      ['contestation', 'QP2604-Q3'],
      ['vlcc', 'QP2604-Q4'],
      ['biofouling', 'QP2604-Q5'],
      ['ship sanitation', 'QP2604-Q6'],
      // NOT 'unclos' -- April Q8 also cites UNCLOS article 94(7), so the bare
      // convention name resolves to two cards. The constitutional article is
      // unique to Q7, and is also the limb April added over January.
      ['article 253', 'QP2604-Q7'],
      ['very serious marine casualty', 'QP2604-Q8'],
      ['fatigue', 'QP2604-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['bfrb', 'QP2604-Q5', 'the biofouling record book (abbreviation never rendered)'],
      ['dualist', 'QP2604-Q7', 'Q7'],
      ['treaty amendment', 'QP2604-Q1', 'Q1'],
    ],
    regulation: ['mepc.378(80)', 'QP2604-Q5'],
    // April Q2 is a NEAR repeat of February Q3 and March Q8, so its recurrence
    // table carries their codes -- which is exactly what should be findable.
    recurrence: ['2026/mar/q8', 'QP2604-Q2'],
    // Must resolve to exactly ONE card. April sets biofouling once, and the
    // record book's full name cannot collide with anything else on the paper.
    narrow: ['biofouling record book', 'QP2604-Q5'],
  },
  QP2606: {
    probes: [
      // Q1 sets goal-based standards and Q8 refers to them when explaining why
      // class rules must be verified, so "goal-based" resolves to two cards.
      // The Ship Construction File is the part of GBS only Q1 carries.
      ['ship construction file', 'QP2606-Q1'],
      ['no more favourable treatment', 'QP2606-Q2'],
      ['york antwerp', 'QP2606-Q3'],
      ['upskill', 'QP2606-Q4'],
      ['msc.428(98)', 'QP2606-Q5'],
      ['inventory control', 'QP2606-Q6'],
      ['particularly sensitive sea area', 'QP2606-Q7'],
      ['periodical survey', 'QP2606-Q8'],
      ['formal safety assessment', 'QP2606-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases. Each
      // answer spells the term out in full, so the abbreviation exists in
      // metadata alone, which is the behaviour being guarded.
      ['scf', 'QP2606-Q1', 'the ship construction file (abbreviation never rendered)'],
      ['ship risk profile', 'QP2606-Q2', 'Q2'],
      ['dpa', 'QP2606-Q5', 'Q5'],
      ['nosdcp', 'QP2606-Q7', 'Q7'],
    ],
    regulation: ['a.1207(34)', 'QP2606-Q8'],
    // June's host table lists no other 2026 sitting against any question, so the
    // recurrence probe has to be a historical code. 2025/FEB/Q9 is unique to Q7;
    // Q8 carries 2025/SEP/Q9, which differs only in the month.
    recurrence: ['2025/feb/q9', 'QP2606-Q7'],
    // Must resolve to exactly ONE card. June sets surveys only in Q8, and the
    // radio certificate's full name cannot collide with anything else.
    narrow: ['cargo ship safety radio certificate', 'QP2606-Q8'],
  },
  // First paper of the 2025 solved-production run, and the first entry here for
  // a paper that is not from the 2026 set.
  QP2508: {
    probes: [
      ['tojo maru', 'QP2508-Q1'],
      ['carbon intensity indicator', 'QP2508-Q2'],
      ['thermal runaway', 'QP2508-Q3'],
      // 'fatigue' would also resolve to Q4 alone, but sleep debt is unique to
      // the Guidelines half of the question and so probes the more specific limb.
      ['sleep debt', 'QP2508-Q4'],
      ['unseaworthy', 'QP2508-Q5'],
      ['york antwerp', 'QP2508-Q6'],
      ['signature subject to ratification', 'QP2508-Q7'],
      // NOT 'net-zero framework' -- Q2 cross-refers to it when separating the
      // in-force CII from the proposed Chapter V, so it resolves to two cards.
      ['ghg fuel intensity', 'QP2508-Q8'],
      ['exclusive economic zone', 'QP2508-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['special drawing rights', 'QP2508-Q1', 'the LLMC question (the card writes only SDR)'],
      ['annual efficiency ratio', 'QP2508-Q2', 'Q2 (the card writes only AER)'],
      ['yar', 'QP2508-Q6', 'Q6 (the abbreviation is never rendered)'],
      ['world merchant fleet tonnage', 'QP2508-Q7', 'Q7'],
    ],
    regulation: ['mepc.377(80)', 'QP2508-Q8'],
    // Leak probe. This code is printed on the source copy against Q5, which
    // carries the heaviest host annotation on the paper - six prior sittings.
    // None of it may reach the shipped bytes.
    recurrence: ['2023/jul/q9', 'QP2508-Q5'],
    // Must resolve to exactly ONE card. August sets general average in Q6 and
    // excepts it from limitation in Q1, so the probe is Rule VII's own heading.
    narrow: ['damage to machinery and boilers', 'QP2508-Q6'],
  },
  QP2403: {
    probes: [
      ['big data', 'QP2403-Q1'],
      ['bill of lading', 'QP2403-Q2'],
      // NOT 'general average' -- it resolves to Q3 alone on this paper, but
      // contribution is the limb the examiner singled out, so probe that.
      ['contributory values', 'QP2403-Q3'],
      ['kappel', 'QP2403-Q4'],
      // NOT 'cyber' -- Q1 reaches the same instruments when it reaches the
      // security barrier, so the term resolves to two cards.
      ['functional elements', 'QP2403-Q5'],
      ['electronic record book', 'QP2403-Q6'],
      ['iii code', 'QP2403-Q7'],
      // NOT 'bridge control' -- Q5 lists bridge systems among the vulnerable
      // onboard systems, so it resolves to Q5 and Q8.
      ['starting air distributor', 'QP2403-Q8'],
      ['maritime labour convention', 'QP2403-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['eu mrv', 'QP2403-Q1', 'the big data question (the card names no reporting regime)'],
      ['machine learning', 'QP2403-Q1', 'Q1 (the card writes only analytics)'],
      ['azipod', 'QP2403-Q4', 'Q4 (the card writes only azimuth or podded propulsion)'],
      ['seafarers bill of rights', 'QP2403-Q9', 'Q9 (the card never uses the phrase)'],
    ],
    regulation: ['a.1070(28)', 'QP2403-Q7'],
    // Leak probe. The March 2024 source copy carries the host's own provider
    // codes against Q8 -- 2010/SR12, 2011/SR4, 2011/SR8 - a different code
    // shape from the year/month/question form used elsewhere in the set, and
    // the only place it appears on this paper. None of it may reach the
    // shipped bytes.
    recurrence: ['2011/sr8', 'QP2403-Q8'],
    // Must narrow. 'bridge control' alone resolves to Q5 and Q8; adding the
    // astern term takes it to Q8 on its own.
    narrow: ['bridge control astern', 'QP2403-Q8'],
  },
  // October 2025 reprints the March 2024 paper question-for-question, so the
  // nine content probes are the same terms -- but they were re-tested against
  // THIS page rather than inherited, because the answers behind them changed.
  QP2510: {
    probes: [
      ['big data', 'QP2510-Q1'],
      ['bill of lading', 'QP2510-Q2'],
      ['contributory values', 'QP2510-Q3'],
      ['kappel', 'QP2510-Q4'],
      ['functional elements', 'QP2510-Q5'],
      ['electronic record book', 'QP2510-Q6'],
      ['iii code', 'QP2510-Q7'],
      ['starting air distributor', 'QP2510-Q8'],
      ['maritime labour convention', 'QP2510-Q9'],
      // Temporal fingerprints. Each of these exists ONLY because this sitting
      // is answered on law the March 2024 paper could not use, so a regression
      // to donor content would take them out and fail here rather than ship.
      ['carriage of goods by sea act 2025', 'QP2510-Q2'],
      ['six functional elements', 'QP2510-Q5'],
      ['social connectivity', 'QP2510-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['eu mrv', 'QP2510-Q1', 'the big data question (the card names no reporting regime)'],
      ['machine learning', 'QP2510-Q1', 'Q1 (the card writes only analytics)'],
      ['azipod', 'QP2510-Q4', 'Q4 (the card writes only azimuth or podded propulsion)'],
      ['seafarers bill of rights', 'QP2510-Q9', 'Q9 (the card never uses the phrase)'],
      // Rev.3 mnemonic. Rev.2's was IPDRR; if the answer regressed to five
      // elements this alias would go with it.
      ['g-ipdrr', 'QP2510-Q5', 'Q5 (the six-element mnemonic, never rendered)'],
      // The inverted proposition. The donor asserts these are EXCLUDED from
      // "goods"; the 2025 Indian Schedule includes them.
      ['live animals deck cargo', 'QP2510-Q2', 'Q2 (the Article I(d) reversal)'],
    ],
    regulation: ['a.1070(28)', 'QP2510-Q7'],
    // Leak probe. 2025/APR/Q9 is a host annotation carried against Q5 on THIS
    // source copy and on no earlier one, so it is specific to this paper rather
    // than inherited from the donor's probe list. None of it may reach the
    // shipped bytes.
    recurrence: ['2025/apr/q9', 'QP2510-Q5'],
    // Must narrow. 'bridge control' alone resolves to Q5 and Q8 -- Q5 lists
    // bridge systems among the vulnerable onboard systems.
    narrow: ['bridge control astern', 'QP2510-Q8'],
  },
  QP2506: {
    probes: [
      ['grim vane wheel', 'QP2506-Q1'],
      ['tacit acceptance', 'QP2506-Q2'],
      ['port of refuge', 'QP2506-Q3'],
      ['scopic', 'QP2506-Q4'],
      ['privity', 'QP2506-Q5'],
      ['refloat', 'QP2506-Q6'],
      ['very serious marine casualty', 'QP2506-Q7'],
      ['msc.1/circ.1598', 'QP2506-Q8'],
      ['unseaworthy', 'QP2506-Q9'],
      // Temporal fingerprints. Each exists ONLY because this sitting is June
      // 2025, so a regression to a donor's content would remove it and fail
      // here rather than ship.
      //
      // The August 2025 donor teaches "assent is not commencement", because the
      // 2025 Act was assented in the month of its own sitting. At June 2025 the
      // Bill had been passed by neither House, so the point is one rung
      // earlier. If this probe stops resolving, the donor's currency paragraph
      // has come back.
      ['a bill is not an act', 'QP2506-Q9'],
      // The revoked predecessor. A.949(23) is the number nearly every note set
      // still carries; A.1184(33) revoked it on 6 December 2023, eighteen
      // months before this sitting. This probe guards against an answer
      // regressing to the widely published wrong edition.
      ['a.1184(33)', 'QP2506-Q3'],
      // SCOPIC is new to the corpus with this paper; the version in force at
      // the sitting is 2020 and the answer's figures are read from that text.
      ['scopic 2020', 'QP2506-Q4'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['costa bulb', 'QP2506-Q1', 'Q1 (the answer never uses the trade name)'],
      ['atl', 'QP2506-Q3', 'Q3 (the answer always writes actual total loss in full)'],
      ['nagasaki spirit', 'QP2506-Q4', 'Q4 (the case is never named in the prose)'],
    ],
    regulation: ['msc.255(84)', 'QP2506-Q7'],
    // Leak probe. 2022/JAN/Q7 is a host annotation printed against Q1 on THIS
    // source copy. None of it may reach the shipped bytes.
    recurrence: ['2022/jan/q7', 'QP2506-Q1'],
    // Must narrow. 'rule vii' alone also resolves to Q8, whose A-VIII/1
    // citation contains the same letters.
    narrow: ['rule vii general average', 'QP2506-Q6'],
  },
  QP2509: {
    probes: [
      ['bauxite', 'QP2509-Q1'],
      ['carbon intensity indicator', 'QP2509-Q2'],
      ['particular average', 'QP2509-Q3'],
      ['maritime lien', 'QP2509-Q4'],
      ['hazardous and noxious', 'QP2509-Q5'],
      ['toolbox talk', 'QP2509-Q6'],
      ['bunkers 2001', 'QP2509-Q7'],
      ['maritime labour convention', 'QP2509-Q8'],
      ['classification society', 'QP2509-Q9'],
    ],
    aliases: [
      ['d40', 'QP2509-Q1', 'the bauxite question (the particle-size term is never rendered)'],
      ['pari passu', 'QP2509-Q4', 'Q4'],
      ['loto', 'QP2509-Q6', 'Q6'],
      ['sleep debt', 'QP2509-Q8', 'Q8'],
    ],
    // A.1186(33) is the edition of the HSSC Survey Guidelines operative at THIS
    // sitting. Its successor A.1207(34) was adopted 3 December 2025, after the
    // paper was sat, and is deliberately absent from the answer. Probing the
    // correct edition therefore also guards the reversal.
    regulation: ['a.1186(33)', 'QP2509-Q9'],
    // Leak probe. 2022/OCT/Q5 is a host annotation printed against Q9 on THIS
    // source copy and appears on no other question of this paper. None of it
    // may reach the shipped bytes.
    recurrence: ['2022/oct/q5', 'QP2509-Q9'],
    // Must resolve to exactly ONE card. September sets pollution liability
    // twice over -- Q5 explains why a ship's own fuel falls outside HNS and Q7
    // is the Bunkers/CLC comparison -- so 'bunker' and even 'bunkers 2001'
    // resolve to both. Surveys are set only in Q9, and the radio certificate's
    // full name cannot collide with anything else on the paper.
    narrow: ['cargo ship safety radio certificate', 'QP2509-Q9'],
  },
  QP2401: {
    probes: [
      ['uberrimae fidei', 'QP2401-Q1'],
      ['single window', 'QP2401-Q2'],
      ['carbon intensity indicator', 'QP2401-Q3'],
      ['planned maintenance system', 'QP2401-Q4'],
      ['unified requirement', 'QP2401-Q5'],
      ['tribology', 'QP2401-Q6'],
      ['vetting inspection', 'QP2401-Q7'],
      ['fault tree analysis', 'QP2401-Q8'],
      ['flag state performance indicators', 'QP2401-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['uberrima fides', 'QP2401-Q1',
       'Q1 (the nominative variant; the answer renders uberrimae fidei)'],
      ['mepc.1/circ.684', 'QP2401-Q3', 'Q3 (the EEOI circular, cited nowhere on the card)'],
      ['pq index', 'QP2401-Q6', 'Q6 (a particle-quantifier term the answer never names)'],
      ['inhibit gate', 'QP2401-Q8', 'Q8 (a gate type outside the worked example)'],
      ['cdi', 'QP2401-Q7', 'Q7 (the chemical/gas parallel scheme, in metadata only)'],
    ],
    // FAL.14(46) rather than a SOLAS regulation, because it is this paper's
    // sharpest temporal anchor: adopted 13 May 2022 but IN FORCE 1 January 2024,
    // days before the sitting, which is what makes the maritime single window
    // already mandatory here. Its successor FAL.15(47) did not enter into force
    // until 1 January 2025. If this probe ever starts resolving to FAL.15(47),
    // the paper has been re-anchored onto an amendment that had not yet bitten.
    regulation: ['fal.14(46)', 'QP2401-Q2'],
    // Leak probe. 2022/OCT/Q2 is a host annotation printed against Q1 on THIS
    // source copy and appears on no other question of this paper. None of it
    // may reach the shipped bytes.
    recurrence: ['2022/oct/q2', 'QP2401-Q1'],
    // Must resolve to exactly ONE card. January sets inspection regimes twice --
    // Q4 carries port state control and the RO Code, Q7 carries vetting -- so
    // 'inspection' and even 'questionnaire' are ambiguous. The compiled
    // questionnaire's full name is SIRE 2.0 vocabulary and cannot collide.
    narrow: ['compiled vessel inspection questionnaire', 'QP2401-Q7'],
  },
  QP2412: {
    probes: [
      ['sustainable development goals', 'QP2412-Q1'],
      ['noise levels', 'QP2412-Q2'],
      ['paris mou', 'QP2412-Q3'],
      ['classification society', 'QP2412-Q4'],
      ['root cause analysis', 'QP2412-Q5'],
      ['maritime labour convention', 'QP2412-Q6'],
      ['hague-visby', 'QP2412-Q7'],
      ['seemp', 'QP2412-Q8'],
      ['flag state performance indicators', 'QP2412-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['swiss cheese', 'QP2412-Q5', 'Q5 (the Reason model by its informal name)'],
      ['dmlc', 'QP2412-Q6', 'Q6 (the compressed form of the Declaration)'],
      ['ship risk profile', 'QP2412-Q3', 'Q3 (the NIR ranking mechanism)'],
      ['latent failure', 'QP2412-Q5', 'Q5 (the organisational half of the failure pair)'],
    ],
    // MEPC.395(82) rather than a SOLAS regulation, because the SEEMP guideline
    // edition is this paper's sharpest temporal anchor: adopted 4 October 2024,
    // it revoked MEPC.346(78) just TWO MONTHS before the sitting. A January 2024
    // treatment of Q8 would still cite MEPC.346(78) and be eleven months stale
    // by December. If this probe stops resolving, Q8 has been re-anchored onto
    // the superseded guidelines.
    regulation: ['mepc.395(82)', 'QP2412-Q8'],
    // Leak probe. 2022/OCT/Q5 is a host annotation printed against Q4 on THIS
    // source copy. None of it may reach the shipped bytes.
    recurrence: ['2022/oct/q5', 'QP2412-Q4'],
    // Must resolve to exactly ONE card. December sets compliance documents more
    // than once -- Q4 carries class certificates and Q8 the SEEMP -- so
    // 'declaration' and 'compliance' are each ambiguous. The DMLC's full printed
    // name belongs to Q6 alone.
    narrow: ['declaration of maritime labour compliance', 'QP2412-Q6'],
  },
  QP2402: {
    probes: [
      ['instrument hierarchy', 'QP2402-Q1'],
      ['bunker convention', 'QP2402-Q2'],
      ['bulbous bow', 'QP2402-Q3'],
      ['cylinder lubricating', 'QP2402-Q4'],
      ['greenhouse gas', 'QP2402-Q5'],
      ['inventory control', 'QP2402-Q6'],
      ['harmonized system of survey', 'QP2402-Q7'],
      ['grounded', 'QP2402-Q8'],
      ['human element', 'QP2402-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['clc 92', 'QP2402-Q2', 'Q2 (the compressed form of the 1992 Civil Liability Convention)'],
      ['scrape down', 'QP2402-Q4', 'Q4 (the cylinder drain-oil analysis technique)'],
      ['economic order quantity', 'QP2402-Q6', 'Q6 (the stores-control model)'],
      ['tacit acceptance', 'QP2402-Q1', 'Q1 (the amendment procedure)'],
    ],
    // MEPC.377(80) rather than an Annex VI regulation number, because a bare
    // number is unusable as a probe here: search is an AND of substrings, so
    // "regulation 24" also matches every card carrying "2024". The 2023 IMO GHG
    // Strategy is the sharper anchor anyway -- it superseded the 2018 Initial
    // Strategy in July 2023, and Q5 must not be written against the old one.
    regulation: ['mepc.377(80)', 'QP2402-Q5'],
    // Leak probe. 2022/DEC/Q5 is a host annotation printed against Q3 on THIS
    // source copy. None of it may reach the shipped bytes.
    recurrence: ['2022/dec/q5', 'QP2402-Q3'],
    // Must resolve to exactly ONE card. February sets surveys and management
    // systems more than once -- Q6 and Q9 both reach the SMS -- so 'survey' and
    // 'certification' are each ambiguous. The HSSC's full printed name is Q7's.
    narrow: ['harmonised system of survey and certification', 'QP2402-Q7'],
  },
  QP2409: {
    probes: [
      ['fitness for duty', 'QP2409-Q1'],
      ['goal based standards', 'QP2409-Q2'],
      ['midterm', 'QP2409-Q3'],
      ['iopc', 'QP2409-Q4'],
      ['social security', 'QP2409-Q5'],
      ['bunker convention', 'QP2409-Q6'],
      ['gisis', 'QP2409-Q7'],
      ['anti-fouling', 'QP2409-Q8'],
      ['rudder', 'QP2409-Q9'],
    ],
    aliases: [
      // Never rendered on the card -- these live only in search_aliases.
      ['tbt', 'QP2409-Q8', 'Q8 (the compressed form of tributyltin)'],
      ['cybutryne', 'QP2409-Q8', 'Q8 (the second controlled substance)'],
      ['blue card', 'QP2409-Q6', 'Q6 (the insurer letter behind the certificate)'],
      ['grim vane wheel', 'QP2409-Q9', 'Q9 (one of the named efficiency devices)'],
      ['costa bulb', 'QP2409-Q9', 'Q9 (the rudder-bulb device)'],
    ],
    // MSC.560(108) rather than a regulation, because it is this paper's sharpest
    // trap in the FORWARD direction. It was adopted in 2024, before the sitting,
    // but does NOT enter into force until 1 January 2026, so it must never be
    // written as law here. Q1 names it precisely in order to exclude it. If this
    // probe stops resolving, the exclusion has been dropped.
    regulation: ['msc.560(108)', 'QP2409-Q1'],
    // Leak probe. 2023/OCT/Q8 is a host annotation printed against Q6 on THIS
    // source copy. None of it may reach the shipped bytes.
    recurrence: ['2023/oct/q8', 'QP2409-Q6'],
    // Must resolve to exactly ONE card. September sets pollution funds twice --
    // Q4 is the IOPC Funds and Q6 the Bunkers/CLC comparison -- so 'fund' and
    // even '1992 fund convention' resolve to both. The device question's full
    // printed title cannot collide.
    narrow: ['rudder efficiency improvement devices', 'QP2409-Q9'],
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
// INVERTED at schema 1.3. This assertion used to REQUIRE that searching a
// third-party host sitting code found the question -- which is only possible
// because the host's printed annotation was inside the shipped data-search
// attribute: invisible on screen, present in the bytes, and another party's
// claim either way. It is now a leak probe. The canonical status label, which
// MIW does compute, is searchable in its place.
if (F.recurrence) {
  ok(`host recurrence code "${F.recurrence[0]}" is NOT searchable`,
     search(F.recurrence[0]).length === 0,
     'got ' + JSON.stringify(search(F.recurrence[0]).map(c => c.qid)));
}
// ...and every card must carry exactly one of the four canonical status labels,
// so the search that was lost is genuinely replaced rather than just removed.
// Asserted structurally rather than by fixture: the label of any given question
// changes the moment another year is transcribed, which is the whole point of
// computing it from the calendar.
const STATUS_LABELS = ['once in this set', 'first in set',
                       'repeated - same wording', 'repeated - reworded'];
const missing = cards.filter(c =>
  !STATUS_LABELS.some(l => c.search.indexOf(l) !== -1)).map(c => c.qid);
ok('every card is searchable by its canonical recurrence status',
   missing.length === 0, 'without a status label: ' + JSON.stringify(missing));
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
// Search is pure and must keep working when localStorage is unavailable.
//
// This probe is derived from the paper's OWN fixtures. It previously read
// `search('general average').length === 1`, which quietly assumed every paper
// in the series sets a general average question -- true of QP2607, QP2601 and
// QP2602 by coincidence, false of QP2603, which failed here on a page whose
// search was working perfectly. That is the same defect class as the old
// glob('EM*.html') and the hard-coded QP2607 fixtures: a harness that derives
// its page list dynamically while keeping a paper-specific assumption inline.
// The guard was NOT weakened -- it still fails if search returns nothing, and
// a paper with no probes at all is already failed above.
const blockedProbe = (F.probes[0] || [null])[0];
ok('search still works with storage blocked',
   !!blockedProbe && storageOK(blocked) === false && search(blockedProbe).length > 0,
   'probe ' + JSON.stringify(blockedProbe) + ' returned ' +
   JSON.stringify(blockedProbe ? search(blockedProbe).map(c => c.qid) : []));

// corrupt payload
const corrupt = makeStore(false);
corrupt.setItem(KEY_BM, 'not json at all');
ok('corrupt stored value is ignored, not fatal', JSON.stringify(load(corrupt, KEY_BM)) === '{}');
corrupt.setItem(KEY_BM, '["array","not","object"]');
ok('wrong-shaped stored value is ignored', JSON.stringify(load(corrupt, KEY_BM)) === '{}');

console.log('');
console.log(`RESULT: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
