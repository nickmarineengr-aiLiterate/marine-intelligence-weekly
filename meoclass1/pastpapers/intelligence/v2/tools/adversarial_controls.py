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
import io
import os
import re
import sys


def _make_stdout_printable():
    """Let this harness report on a stock Windows console.

    Control data carries the characters the examiner actually writes -
    `25 um` is also spelled `25 \u00b5m`, and the two must stay distinct in
    the corpus. A default Windows console is cp1252, which cannot encode
    either that or a degree sign, so printing the results table raised
    UnicodeEncodeError halfway down and the suite exited 1 without a
    verdict. It failed closed, so it could never manufacture a false
    green - but a control suite that is red on an unconfigured machine is
    not a portable control suite, and requiring PYTHONIOENCODING=utf-8 to
    be set by hand is exactly the environment dependence the rest of this
    model was cleaned of.

    This is display only. No test datum is altered: the strings compared
    by the classifier are the unmodified source strings, so the semantic
    result is identical whichever branch below is taken.
    """
    for name in ('stdout', 'stderr'):
        stream = getattr(sys, name, None)
        if stream is None:
            continue
        reconfigure = getattr(stream, 'reconfigure', None)
        if reconfigure is not None:          # CPython >= 3.7
            try:
                reconfigure(encoding='utf-8', errors='backslashreplace')
                continue
            except (ValueError, OSError):
                pass
        buf = getattr(stream, 'buffer', None)
        if buf is not None:
            setattr(sys, name, io.TextIOWrapper(
                buf, encoding='utf-8', errors='backslashreplace',
                line_buffering=True))


_make_stdout_printable()

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
    # -- Phase 3A.1: examiner demand, section 8 -----------------------------
    # The Laptop review found that a shared SECONDARY demand marker
    # (RESPONSIBILITY, PROCEDURAL_ACTION) floated demand_compatibility to 1.00
    # over an opposite PRIMARY command. Every control here pairs stems that
    # carry two demands, which is precisely what the original 21 never did.

    ('P31-D1', 'describe vs criticise, shared RESPONSIBILITY marker',
     'Describe the responsibilities of the Chief Engineer for planned '
     'maintenance of machinery on board a motor vessel.',
     'Criticise the responsibilities of the Chief Engineer for planned '
     'maintenance of machinery on board a motor vessel.',
     'TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'the governing command must survive a matching secondary task type'),

    ('P31-D2', 'explain vs list, shared RESPONSIBILITY marker',
     'Explain the responsibilities of the Company under the ISM Code for the '
     'safe operation of ships and pollution prevention.',
     'List the responsibilities of the Company under the ISM Code for the '
     'safe operation of ships and pollution prevention.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'an exposition is not an enumeration; adjudicated below exact/near'),

    ('P31-D3', 'describe vs critically evaluate a procedure',
     'Describe the procedure for carrying out a main engine crankcase '
     'inspection following an oil mist detector alarm.',
     'Critically evaluate the procedure for carrying out a main engine '
     'crankcase inspection following an oil mist detector alarm.',
     'TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'critical demand against expository demand is a different question'),

    ('P31-D4', 'state advantages vs discuss disadvantages',
     'State the advantages of a controllable pitch propeller for a twin screw '
     'vessel in coastal service.',
     'Discuss the disadvantages of a controllable pitch propeller for a twin '
     'screw vessel in coastal service.',
     'TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'strongly incompatible: opposite object and incompatible command'),

    ('P31-D5', 'identical outline of CE responsibilities',
     'Outline the responsibilities of the Chief Engineer during a bunkering '
     'operation alongside in port.',
     'Outline the responsibilities of the Chief Engineer during a bunkering '
     'operation alongside in port.',
     'EXACT_REPEAT|NEAR_VERBATIM',
     'command differences must not be fatal in general: this is a true repeat'),

    ('P31-D6', 'state of readiness is a condition, not the command STATE',
     'Describe how lifeboat launching appliances are maintained in a state of '
     'readiness on board a passenger ship.',
     'Criticise how lifeboat launching appliances are maintained in a state '
     'of readiness on board a passenger ship.',
     'TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'the regime mask must generalise beyond the enumerated phrases'),

    # -- Phase 3A.1: negation and requirement polarity, section 10 ----------

    ('P31-N1', 'required vs not required',
     'State the equipment required to be carried on board for oil pollution '
     'prevention under MARPOL Annex I.',
     'State the equipment not required to be carried on board for oil '
     'pollution prevention under MARPOL Annex I.',
     'TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'a candidate answering the affirmative of a negative stem fails outright'),

    ('P31-N2', 'permitted vs prohibited',
     'Explain the conditions under which discharge of oily bilge water is '
     'permitted in a special area under MARPOL Annex I.',
     'Explain the conditions under which discharge of oily bilge water is '
     'prohibited in a special area under MARPOL Annex I.',
     'TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'opposite poles of one permission'),

    ('P31-N3', 'with approval vs without approval',
     'Describe a modification to the fuel oil system carried out with the '
     'approval of the Administration during a voyage.',
     'Describe a modification to the fuel oil system carried out without the '
     'approval of the Administration during a voyage.',
     'TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'the legal condition is inverted, not merely qualified'),

    ('P31-N4', 'shall vs shall not',
     'State the circumstances in which the Master shall report a marine '
     'casualty to the Administration.',
     'State the circumstances in which the Master shall not report a marine '
     'casualty to the Administration.',
     'TOPIC_ONLY|NO_MEANINGFUL_MATCH',
     'modal negation follows the modal, so the anchor must look forward'),

    ('P31-N5', 'must vs may - legal force differs',
     'The Chief Engineer must record the bunker delivery note details in the '
     'oil record book on completion of bunkering.',
     'The Chief Engineer may record the bunker delivery note details in the '
     'oil record book on completion of bunkering.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'obligation against discretion: not exact, but not a contradiction'),

    ('P31-N6', 'an incidental not must NOT destroy a same-core relationship',
     'Describe the action to be taken by the duty engineer when the main '
     'engine will not start on air.',
     'Describe the action to be taken by the duty engineer when the main '
     'engine fails to start on air.',
     'EXACT_REPEAT|NEAR_VERBATIM',
     'negation anchored to `start` is not a rule polarity; nothing may fire'),

    # -- Phase 3A.1: technical magnitudes, section 13 -----------------------

    ('P31-M1', 'sulphur 0.50 percent vs 0.10 percent',
     'Explain the survey requirements for a vessel operating on fuel oil of '
     '0.50 percent sulphur content in an emission control area.',
     'Explain the survey requirements for a vessel operating on fuel oil of '
     '0.10 percent sulphur content in an emission control area.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'the decimal Phase 3A could not see at all'),

    ('P31-M2', 'detained two vs three consecutive years',
     'Describe the consequences for a ship detained for two consecutive '
     'years under the Paris MOU banning criteria.',
     'Describe the consequences for a ship detained for three consecutive '
     'years under the Paris MOU banning criteria.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'a time period is a magnitude, not a count of things to produce'),

    ('P31-M3', '440 V vs 1000 V switchboard',
     'Describe the maintenance and testing procedure for a 440 volt main '
     'switchboard on board a motor vessel.',
     'Describe the maintenance and testing procedure for a 1000 volt main '
     'switchboard on board a motor vessel.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'both magnitudes sat outside the Phase-3A 1-20 window'),

    ('P31-M4', '15 ppm vs 5 ppm oily water separator',
     'State the alarm and stopping arrangements provided for a 15 ppm oily '
     'water separator discharging overboard.',
     'State the alarm and stopping arrangements provided for a 5 ppm oily '
     'water separator discharging overboard.',
     'SAME_CORE_ASK|TOPIC_ONLY',
     'a statutory limit is load-bearing'),

    ('P31-M5', 'mark allocation is annotation, not a technical quantity',
     'Describe the procedure for testing the emergency generator on board a '
     'motor vessel under load conditions. (4)',
     'Describe the procedure for testing the emergency generator on board a '
     'motor vessel under load conditions. [6]',
     'EXACT_REPEAT|NEAR_VERBATIM',
     'the Phase-3A marks exclusion must NOT regress: the bank prints no marks'),

    # -- Phase 3A.2: marine technical magnitudes ----------------------------
    # The Laptop review of Phase 3A.1 found the numeric model had no FORCE,
    # VISCOSITY, TONNAGE, NAUTICAL-DISTANCE or MICRON dimension, so a stem
    # could change the quantity the answer turns on and still read as an exact
    # repeat. Each control below is a magnitude an MEO Class I answer is marked
    # on. Reaching SAME_CORE_ASK is the point: the ask survives, the claim of
    # verbatim recurrence does not.
    ('P32-F1', 'lifeboat release gear tested at 70 N vs 100 N',
     'Explain the procedure for testing the lifeboat on-load release gear and state the test value of %s that the manufacturer specifies.' % '70 N', 'Explain the procedure for testing the lifeboat on-load release gear and state the test value of %s that the manufacturer specifies.' % '100 N', 'SAME_CORE_ASK',
     'FORCE was absent from the model, so both sides extracted nothing'),
    ('P32-F2', 'release gear tested at 2.2 kN vs 4.4 kN',
     'Explain the procedure for testing the lifeboat on-load release gear and state the test value of %s that the manufacturer specifies.' % '2.2 kN', 'Explain the procedure for testing the lifeboat on-load release gear and state the test value of %s that the manufacturer specifies.' % '4.4 kN', 'SAME_CORE_ASK',
     'Phase 3A.1 caught this only because they are decimals, not because kN '
     'was understood'),
    ('P32-F3', '70 N vs 0.07 kN - equal, but not provably so',
     'Explain the procedure for testing the lifeboat on-load release gear and state the test value of %s that the manufacturer specifies.' % '70 N', 'Explain the procedure for testing the lifeboat on-load release gear and state the test value of %s that the manufacturer specifies.' % '0.07 kN', 'EXACT_REPEAT|NEAR_VERBATIM',
     'the layer does no unit conversion and will not guess one; newtons and '
     'kilonewtons share no dimension, so no conflict may be claimed. A '
     'DOCUMENTED LIMITATION, not a repair'),

    ('P32-P1', 'filter fineness 25 microns vs 10 microns',
     'State the arrangement of the lubricating oil filter of %s fitted to the main engine and explain how it is cleaned.' % '25 microns', 'State the arrangement of the lubricating oil filter of %s fitted to the main engine and explain how it is cleaned.' % '10 microns', 'SAME_CORE_ASK',
     'the 1-20 window in its purest form: 25 extracted nothing, 10 extracted '
     'a COUNT, and the conflict test needs both sides'),
    ('P32-P2', '25 microns vs 25 um - one magnitude, two spellings',
     'State the arrangement of the lubricating oil filter of %s fitted to the main engine and explain how it is cleaned.' % '25 microns', 'State the arrangement of the lubricating oil filter of %s fitted to the main engine and explain how it is cleaned.' % '25 um',
     'EXACT_REPEAT|NEAR_VERBATIM',
     'normalising a spelling is not converting a unit'),
    ('P32-P3', '10 \u03bcm vs 10 \u00b5m - Greek mu and micro sign',
     'State the arrangement of the lubricating oil filter of %s fitted to the main engine and explain how it is cleaned.' % '10 \u03bcm', 'State the arrangement of the lubricating oil filter of %s fitted to the main engine and explain how it is cleaned.' % '10 \u00b5m',
     'EXACT_REPEAT|NEAR_VERBATIM',
     'two distinct code points that name the same unit'),

    ('P32-V1', 'bunker viscosity 180 cSt vs 380 cSt',
     'Describe the treatment of heavy fuel oil of %s in the purifier before it is admitted to the main engine.' % '180 cSt', 'Describe the treatment of heavy fuel oil of %s in the purifier before it is admitted to the main engine.' % '380 cSt', 'SAME_CORE_ASK',
     'the number IS the fuel grade; 180 and 380 are different fuels and a '
     'different purifier answer'),
    ('P32-V2', 'bunker viscosity 15 cSt vs 15 cSt',
     'Describe the treatment of heavy fuel oil of %s in the purifier before it is admitted to the main engine.' % '15 cSt', 'Describe the treatment of heavy fuel oil of %s in the purifier before it is admitted to the main engine.' % '15 cSt', 'EXACT_REPEAT',
     'the same value must not be manufactured into a conflict'),

    ('P32-T1', 'cargo of 5000 tonnes vs 10000 tonnes',
     'Explain the stability calculation for a vessel carrying a cargo of %s and state the precautions the Chief Engineer takes.' % '5000 tonnes', 'Explain the stability calculation for a vessel carrying a cargo of %s and state the precautions the Chief Engineer takes.' % '10000 tonnes', 'SAME_CORE_ASK',
     'four and five digit magnitudes were beyond the parser entirely'),
    ('P32-T2', 'cargo of 50 kg vs 100 kg',
     'Explain the stability calculation for a vessel carrying a cargo of %s and state the precautions the Chief Engineer takes.' % '50 kg', 'Explain the stability calculation for a vessel carrying a cargo of %s and state the precautions the Chief Engineer takes.' % '100 kg', 'SAME_CORE_ASK',
     'MASS existed in Phase 3A.1 but nothing above 20 reached it unless a '
     'unit was recognised'),
    ('P32-T3', 'vessel of 50,000 dwt vs 70,000 dwt',
     'Explain the stability calculation for a vessel carrying a cargo of %s and state the precautions the Chief Engineer takes.' % '50,000 dwt', 'Explain the stability calculation for a vessel carrying a cargo of %s and state the precautions the Chief Engineer takes.' % '70,000 dwt', 'SAME_CORE_ASK',
     'grouped thousands are one number, and tonnage is a dimension'),

    ('P32-N1', 'discharge within 3 nautical miles vs 12 nautical miles',
     'State the discharge requirements that apply to a vessel operating within %s of the nearest land and explain the record entries.' % '3 nautical miles', 'State the discharge requirements that apply to a vessel operating within %s of the nearest land and explain the record entries.' % '12 nautical miles',
     'SAME_CORE_ASK',
     'the special-area boundary is the answer; 3 and 12 are different regimes'),
    ('P32-N2', 'discharge within 3 NM vs 12 NM',
     'State the discharge requirements that apply to a vessel operating within %s of the nearest land and explain the record entries.' % '3 NM', 'State the discharge requirements that apply to a vessel operating within %s of the nearest land and explain the record entries.' % '12 NM', 'SAME_CORE_ASK',
     'the abbreviated form must be read as the spelled form is'),

    ('P32-X1', 'minimum four pumps vs minimum six pumps',
     'Explain the bilge pumping arrangement of a motor vessel fitted with a minimum of %s pumps and state how each is tested.' % 'four', 'Explain the bilge pumping arrangement of a motor vessel fitted with a minimum of %s pumps and state how each is tested.' % 'six', 'SAME_CORE_ASK',
     'the mark-allocation exclusion strips PARENTHESISED digits only: a '
     'spelled technical quantity in the examiner\'s own words is semantic and '
     'must survive'),

    # -- Phase 3A.3: an ordinary word must not erase a technical magnitude ---
    # `_INSTRUMENT_NUM` suppresses the number after a reference token, and it
    # used to match those tokens as bare substrings: `no` inside "not" and
    # "nozzle", `reg` inside "regular", `ism` inside "mechanism". The number
    # was then dropped BEFORE its unit was read, and because `number_conflict`
    # compares only shared dimensions, an emptied set is silence rather than
    # disagreement - so two stems differing ONLY in a load-bearing quantity
    # came back EXACT_REPEAT.
    #
    # These run in pairs on purpose. The `-1` case proves the magnitude
    # survives preprocessing and still separates the two questions; the `-2`
    # case holds every word constant and repeats the value, proving the
    # separation came from the quantity and not from the sentence around it.
    # A one-sided test could be passed by a parser that had simply stopped
    # suppressing anything at all.
    ('P33-A1', 'NOT: filter not coarser than 25 vs 10 microns',
     'A lubricating oil filter is not coarser than 25 microns. Describe the maintenance the Chief Engineer carries out on it.',
     'A lubricating oil filter is not coarser than 10 microns. Describe the maintenance the Chief Engineer carries out on it.',
     'SAME_CORE_ASK',
     'the Laptop decisive case: "not" contains "no", and the fineness IS the '
     'answer'),
    ('P33-A2', 'NOT: filter not coarser than 25 vs 25 microns',
     'A lubricating oil filter is not coarser than 25 microns. Describe the maintenance the Chief Engineer carries out on it.',
     'A lubricating oil filter is not coarser than 25 microns. Describe the maintenance the Chief Engineer carries out on it.',
     'EXACT_REPEAT',
     'paired control: identical wording AND identical value must stay a repeat'),

    ('P33-B1', 'NOZZLE: injector opens at 250 vs 180 bar',
     'A fuel injector nozzle opens at 250 bar. Explain how it is tested and reconditioned on board.',
     'A fuel injector nozzle opens at 180 bar. Explain how it is tested and reconditioned on board.',
     'SAME_CORE_ASK',
     '"nozzle" contains "no"; the opening pressure is the setting being asked '
     'about'),
    ('P33-B2', 'NOZZLE: injector opens at 250 vs 250 bar',
     'A fuel injector nozzle opens at 250 bar. Explain how it is tested and reconditioned on board.',
     'A fuel injector nozzle opens at 250 bar. Explain how it is tested and reconditioned on board.',
     'EXACT_REPEAT',
     'paired control for the nozzle stem'),

    ('P33-C1', 'MECHANISM: release mechanism at 60 vs 100 N',
     'The locking mechanism of a lifeboat release gear withstands 60 N. State the tests and the records kept.',
     'The locking mechanism of a lifeboat release gear withstands 100 N. State the tests and the records kept.',
     'SAME_CORE_ASK',
     '"mechanism" contains "ism"; the test load is the quantity in issue'),
    ('P33-C2', 'MECHANISM: release mechanism at 60 vs 60 N',
     'The locking mechanism of a lifeboat release gear withstands 60 N. State the tests and the records kept.',
     'The locking mechanism of a lifeboat release gear withstands 60 N. State the tests and the records kept.',
     'EXACT_REPEAT',
     'paired control for the mechanism stem'),

    ('P33-D1', 'REGULAR: regular testing at 440 vs 690 V',
     'A main switchboard under regular testing at 440 V is to be maintained. Describe the insulation tests and the safety precautions.',
     'A main switchboard under regular testing at 690 V is to be maintained. Describe the insulation tests and the safety precautions.',
     'SAME_CORE_ASK',
     '"regular" contains "reg"; the voltage decides the precautions'),
    ('P33-D2', 'REGULAR: regular testing at 440 vs 440 V',
     'A main switchboard under regular testing at 440 V is to be maintained. Describe the insulation tests and the safety precautions.',
     'A main switchboard under regular testing at 440 V is to be maintained. Describe the insulation tests and the safety precautions.',
     'EXACT_REPEAT',
     'paired control for the regular-testing stem'),

    # -- four further realistic stems carrying the dangerous substrings ------
    ('P33-E1', 'NORMAL: normal running speed 750 vs 900 rpm',
     'The normal running speed of the main engine is 750 rpm. Explain the effect on the turbocharger and the fuel system.',
     'The normal running speed of the main engine is 900 rpm. Explain the effect on the turbocharger and the fuel system.',
     'SAME_CORE_ASK',
     '"normal" contains "no"'),
    ('P33-F1', 'REGULATING: regulating valve lifts at 7 vs 12 bar',
     'The regulating valve of the boiler lifts at 7 bar. Describe the setting procedure and the log entries required.',
     'The regulating valve of the boiler lifts at 12 bar. Describe the setting procedure and the log entries required.',
     'SAME_CORE_ASK',
     '"regulating" contains "reg"'),
    ('P33-G1', 'REGISTRATION: registration survey covers 12 vs 30 months',
     'The registration survey of the vessel covers 12 months of machinery records. State what the Chief Engineer prepares for it.',
     'The registration survey of the vessel covers 30 months of machinery records. State what the Chief Engineer prepares for it.',
     'SAME_CORE_ASK',
     '"registration" contains "reg"'),
    ('P33-H1', 'ISOLATING MECHANISM: trips at 30 vs 60 A',
     'The isolating mechanism of the emergency switchboard trips at 30 A. Explain the discrimination arrangement and its testing.',
     'The isolating mechanism of the emergency switchboard trips at 60 A. Explain the discrimination arrangement and its testing.',
     'SAME_CORE_ASK',
     '"isolating" and "mechanism" both carry the substrings'),

    # -- the bare negation, which anchoring alone would not have saved -------
    # `\bno\b` would still match the "no" of "no more than". The designator is
    # always written "No. 4", so `no` is required to carry its period.
    ('P33-I1', 'NO MORE THAN: 15 vs 5 ppm oil content',
     'The oily water separator discharges no more than 15 ppm. Describe the alarm arrangement and the record entries.',
     'The oily water separator discharges no more than 5 ppm. Describe the alarm arrangement and the record entries.',
     'SAME_CORE_ASK',
     'a leading word boundary alone leaves "no more than" suppressing the '
     'limit; the period on "no." is what separates the negation from the '
     'designator'),
    ('P33-I2', 'NO MORE THAN: 15 vs 15 ppm oil content',
     'The oily water separator discharges no more than 15 ppm. Describe the alarm arrangement and the record entries.',
     'The oily water separator discharges no more than 15 ppm. Describe the alarm arrangement and the record entries.',
     'EXACT_REPEAT',
     'paired control for the bare-negation stem'),
]


# Each mutation switches one guard off. `expect_fail` names controls that must
# stop holding — if they all still pass, the guard is not load-bearing.
MUTATIONS = [
    ('examiner demand removed from the classifier',
     dict(use_demand=False),
     ['AD-1', 'AD-3', 'AD-13', 'AD-14', 'P31-D1', 'P31-D3', 'P31-D4']),
    ('actor mismatch ignored',
     dict(use_actor=False), ['AD-2', 'AD-5']),
    ('short-stem floor removed',
     dict(use_short_stem=False), ['NC-5', 'AD-9']),
    ('critical numbers ignored',
     dict(use_numbers=False),
     ['AD-6', 'P31-M1', 'P31-M2', 'P31-M3', 'P31-M4']),
    ('opposite conditions ignored',
     dict(use_polarity=False), ['NC-6', 'AD-4', 'AD-12']),

    # -- Phase 3A.1: the repairs must be load-bearing, not merely present ----
    # Each of these restores the exact defect the Laptop review measured. If a
    # mutation escapes, the repair is decoration.
    ('P3A-1 restored: demand aggregated with max() again',
     dict(demand_aggregate_max=True), ['P31-D1']),
    ('P3A-2 restored: regime masking removed',
     dict(use_regime_mask=False), ['P31-D6']),
    ('P3A-3 restored: requirement polarity / negation removed',
     dict(use_negation=False),
     ['P31-N1', 'P31-N2', 'P31-N3', 'P31-N4', 'P31-N5']),
    ('P3A-4 restored: numbers narrowed back to integers 1-20',
     dict(numbers_small_int_only=True),
     ['P31-M1', 'P31-M3', 'P32-F1', 'P32-P1', 'P32-V1', 'P32-T1', 'P32-T2',
      'P32-T3']),

    # -- Phase 3A.2: each dimension must be load-bearing, not merely listed --
    # A unit table is easy to extend and easy to extend uselessly. These delete
    # one family of units at a time and require a control to stop holding.
    ('P32-1 restored: force units unknown',
     dict(numbers_drop=qs.NUMERIC_MUTATION_SETS['force']),
     ['P32-F1', 'P32-F2']),
    ('P32-2 restored: micron / particle size unknown',
     dict(numbers_drop=qs.NUMERIC_MUTATION_SETS['micron']), ['P32-P1']),
    ('P32-3 restored: viscosity unknown',
     dict(numbers_drop=qs.NUMERIC_MUTATION_SETS['viscosity']), ['P32-V1']),
    ('P32-4 restored: tonnage and mass unknown',
     dict(numbers_drop=qs.NUMERIC_MUTATION_SETS['tonnage']),
     ['P32-T1', 'P32-T2', 'P32-T3']),
    ('P32-5 restored: nautical distance unknown',
     dict(numbers_drop=qs.NUMERIC_MUTATION_SETS['nautical']),
     ['P32-N1', 'P32-N2']),
    ('P32-6 restored: decimals ignored',
     dict(numbers_ignore_decimals=True), ['P32-F2', 'P31-M1']),
]


# The mutations above switch off a classifier option. The boundary in
# `_INSTRUMENT_NUM` is not an option - it is the expression itself - so it is
# mutated by substitution instead. Each entry restores a WEAKER form of the
# reference-suppression rule and must break at least one control or parser
# case; if a weaker expression passes everything, the boundary is decoration
# and the Phase 3A.2 defect could return unnoticed.
REGEX_MUTATIONS = [
    ('P33-1 restored: reference tokens unanchored (the 3A.2 defect)',
     r'(solas|marpol|stcw|colreg|load\s*line|tonnage|ilo|mlc|isps|ism|annex|'
     r'chapter|regulation|reg|convention|protocol|amendment|no\.?)'
     r'\s*[^.;]{0,24}$'),
    ('P33-2 leading boundary only: "regular" and "registration" still match',
     r'\b(solas|marpol|stcw|colreg|load\s*line|tonnage|ilo|mlc|isps|ism|annex|'
     r'chapter|regulation|reg|convention|protocol|amendment|no\.)'
     r'\s*[^.;]{0,24}$'),
    ('P33-3 period dropped from "no.": the bare negation suppresses again',
     r'(?:\b(?:solas|marpol|stcw|colreg|load\s*line|tonnage|ilo|mlc|isps|ism|'
     r'annex|chapter|regulation|reg|convention|protocol|amendment|no)\b\.?)'
     r'\s*[^.;]{0,24}$'),
]




# Magnitude parsing, asserted directly rather than through a classification.
# The class-level controls above cannot isolate a parser defect whose two stems
# differ lexically anyway, and two of the defects below are of that kind: they
# are OVER-claims, where Phase 3A.1 read two different quantities as one
# magnitude because a dimension key lumped several scales together. Nothing in
# the Laptop review reached them, because every case it raised was an
# under-claim.
NUMERIC_PARSER_CASES = [
    # (text, dimension, value, note) - value None means "no such dimension"
    ('a test load of 70 N', 'FORCE_N', '70',
     'the headline R-2 gap: force did not exist'),
    ('a test load of 100 N', 'FORCE_N', '100', 'and not only below 20'),
    ('a fineness of 25 microns', 'MICRON', '25',
     'the 1-20 window, reproduced with a different unit'),
    ('a fineness of 25 \u00b5m', 'MICRON', '25', 'micro sign normalises'),
    ('a fineness of 25 \u03bcm', 'MICRON', '25', 'Greek mu normalises'),
    ('a fineness of 25um', 'MICRON', '25', 'unspaced form is the same value'),
    ('a grade of 380 cSt', 'VISCOSITY_CST', '380', 'viscosity did not exist'),
    ('a vessel of 50,000 dwt', 'TONNAGE_DWT', '50000',
     'grouped thousands are one number'),
    ('within 12 NM of land', 'NAUTICAL_MILE', '12',
     'the abbreviation, resolved by its casing'),
    ('within 12 nautical miles of land', 'NAUTICAL_MILE', '12',
     'and the spelled phrase, read from its first word'),

    # -- conservative refusals: silence beats a guess ----------------------
    ('a wavelength of 12 nm', 'NAUTICAL_MILE', None,
     'lowercase nm is nanometres or nautical miles and casing cannot settle '
     'it, so no distance is claimed'),
    ('a load of 2.2 KN', 'FORCE_KN', None,
     'shouted KN is kN or kn; it is dropped rather than guessed'),
    ('a temperature of 40 C', 'TEMPERATURE_C', None,
     'bare C is Celsius or a category letter; only \u00b0C and the spelled '
     'forms are read as temperature'),
    ('a temperature of 40 \u00b0C', 'TEMPERATURE_C', '40',
     'the degree sign settles it'),

    # -- OVER-claims found in this pass, not raised by the review ----------
    ('rated at 440 kV', 'VOLT_V', None,
     'Phase 3A.1 held one VOLT key, so 440 V and 440 kV read as the same '
     'magnitude. A scale is part of the dimension'),
    ('running at 100 knots', 'SPEED_RPM', None,
     'Phase 3A.1 held one SPEED key covering knots AND rpm, so 100 rpm and '
     '100 knots read as the same magnitude'),
    ('running at 100 knots', 'SPEED_KNOT', '100', 'and knots are still read'),

    # -- exclusions that must not regress ----------------------------------
    ('the emergency generator test (4)', 'COUNT', None,
     'a parenthesised digit is MIW mark annotation, which the bank never '
     'prints'),
    ('under SOLAS 74 as amended', 'COUNT', None,
     'an instrument number names a document, not a quantity'),
    ('a minimum of four pumps is fitted', 'COUNT', '4',
     'but a spelled quantity in the examiner\'s own words is semantic'),
    ('operate within 30 seconds', 'TIME_SECOND', '30',
     'and so is an unparenthesised one'),

    # -- Phase 3A.3: the reference tokens are whole words, both ends --------
    # Asserted at the parser because that is where the magnitude was lost. The
    # classifier controls above prove the product consequence; these prove the
    # cause, one substring at a time.
    ('a filter not coarser than 25 microns', 'MICRON', '25',
     '"not" is not "no."'),
    ('the nozzle opens at 250 bar', 'PRESSURE_BAR', '250',
     '"nozzle" is not "no."'),
    ('the locking mechanism withstands 60 N', 'FORCE_N', '60',
     '"mechanism" is not "ism"'),
    ('under regular testing at 440 V', 'VOLT_V', '440',
     '"regular" is not "reg"'),
    ('normal running speed is 750 rpm', 'SPEED_RPM', '750',
     '"normal" is not "no."'),
    ('the regulating valve lifts at 7 bar', 'PRESSURE_BAR', '7',
     '"regulating" is not "reg"'),
    ('the registration survey covers 12 months', 'TIME_MONTH', '12',
     '"registration" is not "reg"'),
    ('the isolating mechanism trips at 30 A', 'CURRENT_A', '30',
     '"isolating mechanism" carries both substrings'),
    ('numbered equipment tested at 180 cSt', 'VISCOSITY_CST', '180',
     '"numbered" is not "no."'),
    ('an isometric sketch drawn to 5 mm', 'LENGTH_MM', '5',
     '"isometric" is not "ism"'),
    ('sulphur content not above 0.50 percent mass', 'PERCENT', '0.5',
     'the decimal limit survives the negation'),
    ('not less than 4 pumps are fitted', 'COUNT', '4',
     'and so does a bare count'),
    ('discharging no more than 25 microns', 'MICRON', '25',
     'the bare negation is not a designator'),

    # -- and the genuine references are still suppressed --------------------
    ('under regulation 13 of Annex I', 'COUNT', None,
     'a spelled regulation reference names a document'),
    ('under Reg. 14 of the Annex', 'COUNT', None,
     'and so does the abbreviated form, which the old expression MISSED '
     'because [^.;] could not cross the period'),
    ('under reg 14 of the Annex', 'COUNT', None,
     'with or without the period'),
    ('as required by No. 4 of the code', 'COUNT', None,
     'the designator carries its period'),
    ('the ISM 9 requirement applies', 'COUNT', None,
     'a bare instrument acronym is still a reference'),
    ('see chapter 9 of the code', 'COUNT', None, 'chapter references too'),
    ('MARPOL Annex VI regulation 14 applies', 'COUNT', None,
     'the full citation form the corpus actually uses'),
]


def run_numeric_parser(verbose=True):
    """Return the set of parser cases that FAILED."""
    failed = set()
    if verbose:
        print('%-40s %-16s %-10s %s'
              % ('TEXT', 'DIMENSION', 'EXPECT', 'RESULT'))
        print('-' * 108)
    for text, dim, want, note in NUMERIC_PARSER_CASES:
        got = dict(qs.numbers(text)).get(dim)
        ok = (got == want)
        if not ok:
            failed.add(text)
        if verbose:
            print('%-40s %-16s %-10s %s'
                  % (text[:40], dim, want if want else '(absent)',
                     'pass' if ok else 'FAIL (got %r)' % got))
    return failed


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

    print()
    print('magnitude parsing - asserted directly, not through a class')
    print()
    num_failed = run_numeric_parser()
    print()
    print('parser cases: %d   failures: %d'
          % (len(NUMERIC_PARSER_CASES), len(num_failed)))
    if num_failed:
        print('failing: %s' % sorted(num_failed))
    failed = failed | num_failed

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

    print()
    print('reference-suppression boundary - each weaker expression must break '
          'something')
    print('%-62s %s' % ('MUTATION', 'RESULT'))
    print('-' * 108)
    intact = qs._INSTRUMENT_NUM
    rx_escapes = 0
    try:
        for name, pattern in REGEX_MUTATIONS:
            qs._INSTRUMENT_NUM = re.compile(pattern, re.I)
            broke = ((run(qs.DEFAULT, verbose=False) - failed)
                     | (run_numeric_parser(verbose=False) - failed))
            ok = bool(broke)
            rx_escapes += 0 if ok else 1
            print('%-62s %s' % (
                name[:62],
                'load-bearing (broke %d: %s)'
                % (len(broke), ', '.join(sorted(broke)[:3])) if ok
                else 'ESCAPED - the boundary is decoration'))
    finally:
        qs._INSTRUMENT_NUM = intact
    print('-' * 108)
    print('regex mutations: %d   escaped: %d'
          % (len(REGEX_MUTATIONS), rx_escapes))
    escapes += rx_escapes

    return 1 if (failed or escapes) else 0


if __name__ == '__main__':
    sys.exit(main())
