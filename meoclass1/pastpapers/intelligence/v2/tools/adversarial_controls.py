# -*- coding: utf-8 -*-
"""Adversarial controls for the QI-v2 similarity classifier.

Supersedes tools/negative_controls.py, which held its own private copy of the
classifier. Everything here calls tools/qi_similarity.py, so a control failing
means the shipped model failed.

    python .../adversarial_controls.py            run the controls
    python .../adversarial_controls.py --mutate   switch each guard off and
                                                  prove a control depends on it

The mutation pass is the point. A guard that no control depends on is
decoration: if the suite still passes with examiner demand removed, then
demand is not load-bearing, whatever the prose says.
"""
from __future__ import unicode_literals

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import qi_similarity as qs                                        # noqa: E402


# Each control: (id, modern stem, candidate ancestor, allowed classes, note)
CONTROLS = [

    # -- Phase-2 negative controls, retained verbatim ------------------------
    ('NC-1', 'motivation family, true positive',
     'As Chief Engineer on board stress the issues you will address for lack '
     'of motivation, differences in attitude and to increase sense of '
     'competitiveness for better management and effective control?',
     'As chief engineer onboard, stress the issues you will address for lack '
     'of motivation, differences in attitude and to increase sense of '
     'competitiveness for better management and effective control?',
     'EXACT_REPEAT|NEAR_VERBATIM',
     'the one true positive: the guards must not destroy it'),

    ('NC-2', 'cargo abandonment vs abandonment of ship',
     'In what circumstances is cargo considered abandoned, and who carries '
     'liability for such cargo?',
     'When is a ship treated as a wreck and what constitutes abandonment of '
     'the ship by her owners?',
     'NO_MEANINGFUL_MATCH|TOPIC_ONLY',
     'the standing semantic false positive the Laptop required be kept'),

    ('NC-3', 'motivation-as-topic vs the motivation family',
     'As Chief Engineer on board stress the issues you will address for lack '
     'of motivation, differences in attitude and to increase sense of '
     'competitiveness for better management and effective control?',
     'With respect to engine room man management enlist the key issues you '
     'will address with proper justification in the following areas '
     '(a) Training programmes (b) Long term personnel development concept '
     '(c) Attitude and motivation development (d) Emergency response '
     '(e) Copying with stress',
     'NO_MEANINGFUL_MATCH|TOPIC_ONLY',
     'BANK-061 is a near-neighbour of the motivation family, not the family'),

    ('NC-4', 'dry dock coordination vs dry dock project planning',
     'Your vessel where you are posted as Chief Engineer is about to enter a '
     'dry dock. State the coordination and exchange of information necessary '
     'with the Master of the vessel for entering the dock. Also, list the '
     'necessary preparations required along with the delegation of '
     'responsibilities to the engineers of the vessel. Enlist the inspections '
     'and co-operations you will make with the dry dock authorities for '
     'undocking of the vessel.',
     'Why is dry-docking referred to as a major event in the maintenance of a '
     'ship? As a Chief Engineer explain different steps that need '
     'consideration while planning a dry-docking project of a ship due for '
     'its first special survey.',
     'NO_MEANINGFUL_MATCH|TOPIC_ONLY',
     'BANK-164 is about dry-docking but is not the coordination question'),

    ('NC-5', 'one-word "Warranties" vs the differentiate form',
     'Warranties',
     'Differentiate between express and implied warranties and give an '
     'example in each case with reference to a hull and machinery policy of '
     'insurance.',
     'UNSCOREABLE_SHORT_STEM',
     'Phase 2 allowed four classes here; Phase 3A requires exactly one'),

    ('NC-6', 'lay-up reactivation vs lay-up preservation (inverse ask)',
     'A ship on which you have joined as Chief Engineer is scheduled to be '
     'put in active service after major lay-up and necessary repairs. State '
     'the preparation and trials you would conduct prior offering the ship to '
     'the surveying authorities for survey and inspection.',
     'Describe the preservation of machinery you would carry out as Chief '
     'Engineer when taking a vessel into a prolonged lay-up.',
     'NO_MEANINGFUL_MATCH|TOPIC_ONLY',
     'opposite pole of the same condition'),

    # -- the two cases the Laptop demonstrated --------------------------------
    ('AD-1', 'describe vs criticise, same nouns',
     'Describe the actions a Chief Engineer should take on receiving a Port '
     'State Control deficiency notice concerning the oily water separator.',
     'Criticise the actions a Chief Engineer took on receiving a Port State '
     'Control deficiency notice concerning the oily water separator.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'the governing case: DESCRIBE must never read as CRITICISE'),

    ('AD-2', 'inverted responsibility, Chief Engineer vs PSC officer',
     'State the actions the Chief Engineer should take during a Port State '
     'Control inspection of the engine room and its pollution prevention '
     'equipment.',
     'State the actions the Port State Control officer should take during an '
     'inspection of the engine room and its pollution prevention equipment.',
     'TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'who acts on whom is the question, not a detail'),

    # -- ten more, one per failure mode the Founder listed ---------------------
    ('AD-3', 'same nouns, different command (list vs discuss)',
     'List the statutory certificates required on board a bulk carrier.',
     'Discuss the statutory certificates required on board a bulk carrier and '
     'their relative importance to the operation of the vessel.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'DISCUSS is not LIST merely because the objects coincide'),

    ('AD-4', 'same regulation, opposite scenario',
     'State the preparations required before entering a dry dock under the '
     'Load Line conditions of assignment.',
     'State the inspections required after undocking under the Load Line '
     'conditions of assignment.',
     'TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'entering and undocking are opposite poles'),

    ('AD-5', 'same equipment, different responsibility holder',
     'Explain the responsibilities of the Chief Engineer for the maintenance '
     'of the oily water separator and its recording.',
     'Explain the responsibilities of the classification society surveyor for '
     'the survey of the oily water separator and its recording.',
     'TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'same equipment, inverted duty'),

    ('AD-6', 'same words, changed critical number',
     'State FIVE main problems associated with burning residual fuel oil in '
     'medium speed engines and explain how each may be minimised.',
     'State THREE main problems associated with burning residual fuel oil in '
     'medium speed engines and explain how each may be minimised.',
     'SAME_CORE_ASK',
     'the count is part of the task; near-verbatim would overstate it'),

    ('AD-7', 'same words, changed legal qualifier',
     'State the responsibilities and liabilities of the shipper under the '
     'Hague-Visby Rules.',
     'State the responsibilities and liabilities of the shipper under the '
     'Hamburg Rules.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'the instrument decides the answer'),

    ('AD-8', 'old question absorbed inside a larger new question',
     'Underline the general procedures followed for flow of information among '
     'ships personnel. As a Chief Engineer on a ship having multinational '
     'crew, state how the process of effective information to the team can be '
     'approached by you and also how a certain instruction received by you '
     'from shore office for engine management can be best utilized? Following '
     'a Port State Control failure, explain at the initial meeting with your '
     'engineers what examples you would give.',
     'Underline the general procedures followed for flow of information among '
     'ships personnel. As a Chief Engineer on a ship having multinational '
     'crew, state how the process of effective information to the team can be '
     'approached by you and also how a certain instruction received by you '
     'from shore office for engine management can be best utilized?',
     'SAME_CORE_ASK',
     'bidirectional containment must find it, and must not call it exact'),

    ('AD-9', 'short generic stem against a real question',
     'Deviation',
     'As per the Marine Insurance Act, write short notes on the following: '
     '(a) Deviation (b) Warranties (c) War Risk Clause (d) Charterers '
     'Contribution Clause.',
     'UNSCOREABLE_SHORT_STEM',
     'a noun label is not a question, however well it matches'),

    ('AD-10', 'different actor, otherwise identical (bank items 64 and 182)',
     'Differentiate the salient features during survey of a ship under '
     '(i) Bare boat charter (ii) Voyage charter (iii) Time charter. As a '
     'Chief Engineer on board explain with reasons which of the three surveys '
     'is most demanding and exhaustive and why?',
     'Differentiate the salient consideration taken during survey of a ship '
     'under (a) Bare boat charter (b) Voyage charter (c) Time charter. As a '
     'Second Engineer on board explain with reasons which of the three '
     'surveys is most demanding and exhaustive and why?',
     'NEAR_VERBATIM|SAME_CORE_ASK',
     'a real pair inside the bank: adjacent rank weakens exactness only'),

    ('AD-11', 'question versus statement on the same subject',
     'What are the essential features of the ISPS Code and what are the '
     'duties of a Chief Engineer with respect to the Code?',
     'The essential features of the ISPS Code place duties on the Chief '
     'Engineer with respect to the Code.',
     'SAME_CORE_ASK|TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'a statement sets no task'),

    ('AD-12', 'procedural sequence reversed',
     'Describe the procedure for the setting of safety valves of exhaust gas '
     'auxiliary boilers before the inspection of the boiler.',
     'Describe the procedure for the inspection of exhaust gas auxiliary '
     'boilers after the setting of the safety valves.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'before and after are opposite poles of one condition'),

    ('AD-13', 'calculate versus explain on the same quantity',
     'Calculate the maximum pressure to which a corroded starting air '
     'receiver should be subjected.',
     'Explain the maximum pressure to which a corroded starting air receiver '
     'should be subjected.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'a computation is not an exposition'),

    ('AD-14', 'sketch versus state on the same system',
     'Draw a neat sketch of the fuel oil transfer system of a motor vessel.',
     'State the components of the fuel oil transfer system of a motor vessel.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'a drawing is not a list'),

    ('AD-15', 'state and list stay compatible',
     'State the items examined by a surveyor during an annual survey.',
     'List the items examined by a surveyor during an annual survey.',
     'EXACT_REPEAT|NEAR_VERBATIM',
     'the compatibility rules must not over-penalise: STATE and LIST are close'),
]


# Each mutation switches one guard off. `expect_fail` names controls that must
# stop holding — if they all still pass, the guard is not load-bearing.
MUTATIONS = [
    ('examiner demand removed from the classifier',
     dict(use_demand=False), ['AD-1', 'AD-3', 'AD-13', 'AD-14']),
    ('actor mismatch ignored',
     dict(use_actor=False), ['AD-2', 'AD-5']),
    ('short-stem floor removed',
     dict(use_short_stem=False), ['NC-5', 'AD-9']),
    ('critical numbers ignored',
     dict(use_numbers=False), ['AD-6']),
    ('opposite conditions ignored',
     dict(use_polarity=False), ['NC-6', 'AD-4', 'AD-12']),
]


def run(opts, verbose=True):
    """Return the set of control ids that FAILED under these options."""
    failed = set()
    if verbose:
        print('%-7s %-52s %5s %5s %-6s %-9s %-24s %s'
              % ('ID', 'CONTROL', 'FWD', 'REV', 'DMD', 'ACTOR',
                 'CLASSIFIED', 'RESULT'))
        print('-' * 132)
    for cid, name, a, b, allowed, note in CONTROLS:
        r = qs.classify(a, b, opts)
        ok = r.cls in allowed.split('|')
        if not ok:
            failed.add(cid)
        if verbose:
            print('%-7s %-52s %5.2f %5.2f %6.2f %-9s %-24s %s'
                  % (cid, name[:52], r.fwd, r.rev, r.demand_compat,
                     r.actor_rel, r.cls,
                     'pass' if ok else 'FAIL (want %s)' % allowed))
    return failed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mutate', action='store_true')
    ap.add_argument('--why', metavar='ID', help='print the reasons for one control')
    args = ap.parse_args()

    if args.why:
        for cid, name, a, b, allowed, note in CONTROLS:
            if cid == args.why:
                r = qs.classify(a, b)
                print('%s %s' % (cid, name))
                print('  note      : %s' % note)
                print('  modern    : %r' % r.a)
                print('  ancestor  : %r' % r.b)
                print('  lexical   : fwd=%.2f rev=%.2f -> %s'
                      % (r.fwd, r.rev, r.containment_class))
                print('  class     : %s (allowed %s)' % (r.cls, allowed))
                for x in r.reasons:
                    print('  reason    : %s' % x)
                return 0
        print('no such control: %s' % args.why)
        return 2

    print('QI-v2 adversarial controls  (classifier: tools/qi_similarity.py)')
    print()
    failed = run(qs.DEFAULT)
    print()
    print('controls: %d   failures: %d' % (len(CONTROLS), len(failed)))
    if failed:
        print('failing: %s' % sorted(failed))

    if not args.mutate:
        return 1 if failed else 0

    print()
    print('mutation pass - each guard is switched off and must break a control')
    print('%-48s %-28s %s' % ('MUTATION', 'MUST BREAK', 'RESULT'))
    print('-' * 108)
    escapes = 0
    for name, kw, expect in MUTATIONS:
        broke = run(qs.Options(**kw), verbose=False) - failed
        got = sorted(broke & set(expect))
        ok = bool(got)
        escapes += 0 if ok else 1
        print('%-48s %-28s %s' % (
            name[:48], ','.join(expect)[:28],
            'load-bearing (broke %s)' % ','.join(got) if ok
            else 'ESCAPED - guard is decoration'))
    print('-' * 108)
    print('mutations: %d   escaped: %d' % (len(MUTATIONS), escapes))
    return 1 if (failed or escapes) else 0


if __name__ == '__main__':
    sys.exit(main())
