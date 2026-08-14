# MIW Production Agents — Claude Code Kickoff Brief (v1)

**Run this in Claude Code, opened directly at `F:\marine-intelligence-weekly`. Not claude.ai chat.**

This file is the single source of truth for the agent-build project. Save it in the repo (suggested: `docs/agent-build/BRIEF_v1.md`) and reference it from a root or subfolder `CLAUDE.md` so any future Claude Code session — yours or a resumed one — loads this context automatically instead of depending on chat memory.

---

## ADAPTATION NOTES — read before the original spec below

These four corrections sit on top of the original spec (Part A–N, unchanged below). They exist because the original was written slightly ambiguous about *which* Claude product runs it, and because one design assumption needs fixing before implementation starts.

### 1. Subagents are the judgement layer, not the savings layer
Claude Code's native mechanism for "QB Production Agent" and "MIW Notes Production Agent" is its **subagent** feature: filesystem-defined workers in `.claude/agents/*.md`, each with its own context window, a scoped `tools:` allowlist, and a `description:` field Claude Code uses to auto-route work to them. This is the correct implementation vehicle for Part F's "agent separation" requirement.

But subagents are not automatically cheaper — isolating context has its own overhead, and subagent-heavy workflows can run *more* expensive than single-thread work, not less. **The token reduction in this whole design comes from Level 1 (deterministic Python doing extraction, numbering, formatting, validation with zero AI calls).** Build and prove Level 1 first. Subagents are the bounded-judgement layer (Level 2/3) that Python *escalates to* — not the main execution engine, and not the thing to point at when reporting token savings in Part J deliverable #23.

### 2. Two concrete subagent definitions to create
- `.claude/agents/qb-production-agent.md` — tools restricted to Read/Grep/Edit/Bash scoped to `meoclass1/` and `SQ/`. Invoked only for the Level 2 judgement calls listed in Part C (near-duplicate classification, examiner-variant detection, answer drafting from verified source).
- `.claude/agents/miw-notes-production-agent.md` — tools restricted to the Uday notes source/staging directories and the MIW Notes template location. Invoked only for the Level 2 tasks in Part D (interpreting unclear handwriting, resolving ambiguous wording, bounded technical expansion).

Each definition needs a precise `description:` field — that's Claude Code's routing signal, and a vague description causes silent mis-routing more often than a bad system prompt does.

### 3. Persistent context via CLAUDE.md, not chat memory
Point a `CLAUDE.md` (repo root or an `agent-build/` subfolder) at:
- this brief,
- `miw-qb-production_SKILL_v3.md`,
- `miw-notes-mgmt_SKILL.md`,
- `miw-correction-workflow_SKILL.md`,
- the current state/queue files once Part G's schemas exist.

This is the actual mechanism that satisfies Part G's resumability requirement ("a new Claude session should be able to determine what's active, what's done, what failed"). Don't rely on Claude Code "remembering" — make the state legible on disk.

### 4. Use hooks to gate validation, not instruction alone
Add a hook (PostToolUse or Stop) that runs the deterministic validators automatically after each Level 1 Python step, before any subagent or Claude review can mark a batch `VALIDATED`. This turns Part H/Level 4's gate into something mechanically enforced rather than something Claude has to remember to check.

### 5. One thing to verify before starting
Check whether the existing Claude.ai project skills (`miw-qb-production`, `miw-notes-mgmt`, `miw-correction-workflow`, etc.) are also installed for Claude Code, or whether the underlying `.md` files need to be copied/symlinked into `.claude/skills/`. The two products don't share a skill directory automatically — confirm this in the Part N inspection pass below, don't assume it.

---

## ORIGINAL SPEC (Part A–N) — unchanged, run as written with the above corrections applied

*(Original brief pasted in full below this line — see the version already in the MIW project conversation for the complete Part A through Part N text: repository inspection requirements, Level 1–4 execution hierarchy, QB Production Agent functions, MIW Notes Production Agent functions, chapter standard preservation, agent separation rules, state machine, token-efficiency requirements, human/AI control boundaries, deliverables, pilot requirements, premortem, and implementation discipline.)*

**Immediate first task (Part N) — do this and stop:**

1. Current-state assessment of the repo — Python programs, skills, templates, schemas, validators, directory structure, state/queue files, existing agent definitions.
2. Confirm skill-porting status (Adaptation Note 5 above).
3. Existing components reusable unchanged.
4. Token-heavy steps in the present QB workflow.
5. Token-heavy steps in the present MIW Notes workflow.
6. Proposed QB Production Agent architecture (Python execution engine + `qb-production-agent` subagent scope).
7. Proposed MIW Notes Production Agent architecture (Python execution engine + `miw-notes-production-agent` subagent scope).
8. Shared utilities architecture.
9. AI-versus-Python responsibility matrix.
10. State and queue design (files, not chat memory).
11. Implementation package sequence.
12. Premortem (all items from the original Part L, plus: subagent misrouting from a vague `description:` field; hook failing silently).
13. Recommended pilot.
14. Expected token-reduction mechanism — and confirm it's attributed to Level 1 Python, not subagent isolation.
15. Genuine blockers.

**Do not regenerate any Uday Notes chapters. Do not process the QB backlog. Do not create `.claude/agents/*.md` files yet — report the proposed scope and tool allowlists first, implement only after this assessment is reviewed.**
