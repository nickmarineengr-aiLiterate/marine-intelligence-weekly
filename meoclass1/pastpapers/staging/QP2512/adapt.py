"""QP2512 staged-object assembler.

Scratch tooling for one paper. NOT promoted to tools/ -- see WORKFLOW_LESSONS.md
"The staged-object assembler should assert against INTAKE, not against the donor".

Two jobs, in this order:

1. `adapt()` clones a donor question object, applies an authored patch, and then
   RE-ASSERTS every printed-truth field from the QP2512 intake spec LAST. Anything a
   donor supplies for a printed-truth field is presumptively wrong, because the donor's
   printed truth belongs to a different paper. That is the rule the QP2511 Q9 defect
   established, where a staged object had inherited the donor's host_recurrence_hint.

2. `assemble()` merges the staged question objects back into the canonical spec, asserting
   identity, printed stem, marks and subparts against intake before it writes anything.
"""

import copy
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
SPECS = ROOT / "meoclass1" / "pastpapers" / "specs"
STAGING = pathlib.Path(__file__).resolve().parent

# Fields whose value is PRINTED TRUTH about QP2512 and must come from the intake spec,
# never from a donor and never from an authored patch.
PRINTED_TRUTH = (
    "q_no",
    "anchor",
    "text_verbatim",
    "subparts",
    "total_marks",
    "question_id",
    "host_recurrence_hint",
)

# Fields the intake spec owns for classification, which authoring may refine but which
# default to intake when the patch is silent.
INTAKE_DEFAULTS = (
    "short_title",
    "primary_category",
    "subject_tags",
    "intent_tags",
    "topic_tags",
    "command_verbs",
    "recurrence_class",
    "subpart_marks_note",
    "recurrence_adjudication",
)


def _intake(q_no):
    spec = json.loads((SPECS / "QP2512.json").read_text(encoding="utf-8"))
    for q in spec["questions"]:
        if q["q_no"] == q_no:
            return q
    raise KeyError(f"QP2512 intake has no {q_no}")


def _donor(donor_id):
    paper = donor_id.split("-")[0]
    spec = json.loads((SPECS / f"{paper}.json").read_text(encoding="utf-8"))
    for q in spec["questions"]:
        if q["question_id"] == donor_id:
            return copy.deepcopy(q)
    raise KeyError(donor_id)


def _renumber_cards(obj, q_no):
    """Retrieval card ids are identity, not content. Re-key them onto this paper."""
    for i, card in enumerate(obj.get("retrieval_cards") or [], start=1):
        card["id"] = f"QP2512-{q_no}-C{i}"
    return obj


def adapt(q_no, donor_id=None, patch=None, write=True):
    """Build one staged QP2512 question object."""
    base = _donor(donor_id) if donor_id else {}
    obj = copy.deepcopy(base)
    obj.update(copy.deepcopy(patch or {}))

    intake = _intake(q_no)

    # Intake defaults fill only where authoring stayed silent.
    for field in INTAKE_DEFAULTS:
        if field in intake and field not in (patch or {}):
            obj[field] = copy.deepcopy(intake[field])

    # Printed truth is re-asserted LAST and unconditionally.
    for field in PRINTED_TRUTH:
        if field in intake:
            obj[field] = copy.deepcopy(intake[field])
    obj["anchor"] = q_no.lower()

    _renumber_cards(obj, q_no)

    if write:
        out = STAGING / f"{q_no}.json"
        out.write_text(
            json.dumps(obj, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    return obj


def check(q_no):
    """Assert a staged object against intake. Returns a list of failures."""
    obj = json.loads((STAGING / f"{q_no}.json").read_text(encoding="utf-8"))
    intake = _intake(q_no)
    bad = []
    for field in PRINTED_TRUTH:
        if field in intake and obj.get(field) != intake[field]:
            bad.append(f"{q_no}.{field} does not match intake")
    if obj.get("anchor") != q_no.lower():
        bad.append(f"{q_no}.anchor wrong")
    if obj.get("answer_status") != "Built":
        bad.append(f"{q_no}.answer_status is not Built")
    for key in ("model_answer", "study_notes", "answer_route", "quick_revision",
                "retrieval_cards", "sources", "verification_file",
                "decomposition_gate", "decomposition"):
        if not obj.get(key):
            bad.append(f"{q_no}.{key} missing or empty")
    for i, card in enumerate(obj.get("retrieval_cards") or [], start=1):
        if card["id"] != f"QP2512-{q_no}-C{i}":
            bad.append(f"{q_no}.retrieval_cards[{i}] id wrong")
    tr = obj.get("temporal_review") or {}
    if tr.get("sitting") != "December 2025":
        bad.append(f"{q_no}.temporal_review.sitting is not December 2025")
    return bad


def assemble(write=True):
    """Merge every staged question into the canonical spec."""
    spec_path = SPECS / "QP2512.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    staged = {}
    failures = []
    for q in spec["questions"]:
        path = STAGING / f"{q['q_no']}.json"
        if not path.exists():
            failures.append(f"{q['q_no']} not staged")
            continue
        failures.extend(check(q["q_no"]))
        staged[q["q_no"]] = json.loads(path.read_text(encoding="utf-8"))
    if failures:
        for f in failures:
            print("FAIL", f)
        return False
    spec["questions"] = [staged[q["q_no"]] for q in spec["questions"]]
    spec["build_state"] = "Pilot Review Ready"
    spec["review_state"] = "Awaiting Founder Review - complete paper"
    spec["version"] = "1.0"
    spec["updated"] = "2026-08-12"
    if write:
        spec_path.write_text(
            json.dumps(spec, indent=1, ensure_ascii=False) + "\n", encoding="utf-8"
        )
    print(f"assembled {len(staged)} question(s) into specs/QP2512.json")
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "assemble":
        sys.exit(0 if assemble() else 1)
    if len(sys.argv) > 1 and sys.argv[1] == "check":
        allbad = []
        for n in range(1, 10):
            p = STAGING / f"Q{n}.json"
            if p.exists():
                allbad += check(f"Q{n}")
        for b in allbad:
            print("FAIL", b)
        print(f"{len(allbad)} failure(s)")
        sys.exit(1 if allbad else 0)
