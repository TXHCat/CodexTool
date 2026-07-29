# AGENTS.md / Project Harness Rules

## 0. Goal

Use this evidence-first Harness to preserve only the context needed for current work, keep durable project navigation separate from task history, prevent repeated mistakes, and require verification before completion is reported.

## 1. Global Hard Rules

1. Do not fabricate, guess, fake completion, fake verification, or report unverified results.
2. Do not claim completion without real execution, inspection, tests, logs, screenshots, diffs, or other evidence.
3. Clarify unclear goals, scope, constraints, and acceptance criteria before acting.
4. Break problems down from first principles, then choose the simplest stable path that can be verified.
5. Fix root causes first; do not only patch symptoms.
6. Avoid pointless trial and error. If two attempts add no new information, stop and reframe the problem.
7. Keep code clear, stable, and maintainable. Avoid unnecessary complexity, temporary glue, and fragile structure.
8. Unless explicitly allowed, do not install, download, cache, build, or create project files on the C drive.
9. Process mistakes through `.harness/ERROR_LEDGER.md`: create an incident only for distinct reusable information; exact repeats update the matching pattern and current task records.
10. Keep user-visible text concise, direct, actionable, and free of private data or internal mechanics.

## 2. Authority And Project Map

- Identify normative authorities, implementation owners, verification owners, and historical documents before relying on them.
- `.harness/HCA_PROJECT_MAP.md` and all Harness records are derived and non-normative. They locate authoritative or owning sources but never replace them.
- Confirm living claims against the authoritative document, owning module documentation, code, configuration, asset, or fresh verification evidence.
- Keep task status, completion history, incidents, commands, versions, hashes, and test evidence out of the Project Map.
- Mark unknown or unconfirmed information explicitly. Never fill the Project Map from assumptions.

## 3. Module Ownership And Documentation

- Add or identify an owning README whenever a first-party module or responsibility boundary is created.
- Update owning documentation in the same change when responsibility, direct dependencies, entry points, lifecycle, generated-asset ownership, or verification routing changes.
- Update `.harness/HCA_PROJECT_MAP.md` in the same change when documents are added, removed, or relocated, or when module or ownership topology changes.
- Keep detailed technical material near its owner and use the Project Map as a compact locator rather than duplicating those details.
- Keep project documentation outside vendor implementation directories and distinguish project integration responsibility from vendor ownership.

## 4. Harness File Roles

- `.harness/AGENTS.md`: detailed project Harness operating rules.
- `.harness/README_HOW_TO_USE.md`: human-facing usage guide.
- `.harness/PROMPTS.md`: ready-to-copy task prompt templates.
- `.harness/HCA_PROJECT_MAP.md`: compact derived index of authority, repository boundaries, ownership, dependencies, entry points, and verification routes.
- `.harness/TASK_FOCUS_PACK.md`: current complex-task context, constraints, and acceptance focus.
- `.harness/TASK_STATUS.md`: short progress state and next recovery gate.
- `.harness/TASK_RESULT.md`: verified outcomes, evidence pointers, and known gaps.
- `.harness/ERROR_LEDGER.md`: compact Error Ledger retrieval and write contract.
- `.harness/error-ledger/PATTERNS.md`: consolidated active prevention rules.
- `.harness/error-ledger/CATALOG.md`: complete retained incident lookup.
- `.harness/error-ledger/entries/`: canonical fixed 25-ID incident shards.

## 5. Default Execution Order

1. Read `.harness/ERROR_LEDGER.md`, search the active patterns and incident catalog, and open only canonical entries relevant to the task.
2. Define the goal, deliverables, acceptance criteria, allowed scope, risks, and verification method.
3. Classify the task before editing. A narrow, low-risk, reversible task with straightforward verification may use the lightweight flow and short recovery records; complex, cross-boundary, architectural, high-risk, destructive, publication, or explicitly delegated/reviewed work uses the full Focus/Status/Result flow.
4. Read only the relevant authorities, owning module documentation, Project Map locators, and current task records.
5. For lightweight work, the main Agent may make only the smallest necessary in-scope change, with no unrelated refactors or authority expansion, directly or through delegation. For full-flow work, delegate the same bounded change to an implementation subagent with explicit evidence inputs, acceptance checks, and single-writer ownership.
6. Verify through the owning module's route and inspect the actual output, not only the command invocation.
7. Use an independent read-only Review subagent when the full flow applies, the risk justifies it, or the user requests it. Lightweight work may omit this gate.
8. When Review is required, use at most two independent rounds by default. Round 1 inspects the complete declared scope. After the main Agent validates findings and fixes blocking findings, round 2 inspects only that fix delta, affected verification, and the direct regression boundary. A pass requires zero unresolved blocking findings; non-blocking suggestions do not trigger fixes or another Review.
9. Update the required Harness recovery records with concise current state and reusable evidence.
10. If a mistake or missed verification occurs, follow `.harness/ERROR_LEDGER.md` before proceeding.

Do not preload every Error Ledger shard or every project document.

Do not advance to the next task or report completion while a required Review is pending, a blocking finding remains unresolved, or required evidence is missing.

## 6. Task Classification, Subagent Execution, And Review Gates

- The main Agent owns the ordered task sequence, integration decisions, finding validation, and final reporting.
- Lightweight work is narrow, low-risk, reversible, easy to verify, and does not change runtime behavior, architecture, normative product semantics, authority hierarchy, ownership topology, public contracts, security, persistent data, destructive state, releases, or external publication. Mechanically synchronized copies alone do not make a task full-flow.
- For lightweight work, implementation delegation and independent Review are optional and may be omitted independently. Record the lightweight classification and rationale, keep one writer, make only the smallest necessary in-scope change with no unrelated refactors or authority expansion, and run proportionate verification.
- If scope expands, verification becomes ambiguous, a mistake causes non-trivial rework, or new risk crosses a lightweight boundary, reclassify the task and apply the full Subagent/Review flow before continuing.
- When the full flow applies, delegate only the smallest necessary in-scope implementation, with no unrelated refactors or authority expansion, to a bounded subagent with explicit inputs, outputs, constraints, evidence, acceptance checks, and single-writer ownership. The implementation subagent must not recursively delegate unless the main Agent explicitly authorizes it.
- When Review is required, after implementation and owning-route verification assign a different independent review subagent for round 1 to inspect the actual diff, artifacts, acceptance criteria, scope, authority and ownership boundaries, tests and evidence, and relevant Error Ledger patterns. The reviewer is read-only and never edits implementation or evidence.
- A blocking finding is an acceptance failure, correctness defect, out-of-scope change, authority or ownership conflict, security/data/destructive risk, missing required verification, or any issue that would make the completion claim false. Style preferences, optional refactors, future hardening, and suggestions not required for current acceptance are non-blocking; record them once in `.harness/TASK_RESULT.md`, then finish without fixing or re-reviewing them.
- Every Review return must state the round, checked scope, blocking findings, non-blocking suggestions, evidence, conclusion, and remaining risk. The main Agent validates findings and rejects duplicate, unsupported, out-of-scope, or re-litigation findings with a recorded rationale.
- The default Review budget is two independent rounds. Round 1 covers the full declared scope. If blocking findings are fixed, round 2 covers only the blocker-fix delta, affected verification, and direct regression boundary; it must not reopen unchanged scope or accepted decisions. A pass requires zero unresolved blocking findings.
- Do not start an automatic third Review. After round 2, the main Agent may make one scope-preserving small fix only when objective deterministic checks can prove it, then close without another Review. If the remaining fix changes behavior, architecture, scope, or authority judgment, or requires subjective validation, record Review-budget exhaustion and request user direction.
- Pure recovery-record synchronization, evidence-link maintenance, and other administrative updates after Review do not trigger another Review when they do not change the reviewed implementation or acceptance evidence.
- Do not begin the next task or report completion while a required Review is pending, a blocking finding remains unresolved within the available budget, or required evidence is missing. If a required Subagent or Reviewer is unavailable, report the task blocked; this does not block a correctly classified lightweight task whose optional gates were omitted.
- An explicit user request for Subagent execution or Review overrides the lightweight exemption, but the two-round cap still applies unless the user explicitly authorizes more rounds.
- Delegation never expands authority, scope, filesystem permission, or permission to modify user-owned work.

## 7. Error Ledger Rules

- Search for the same or similar failure class before work.
- Create a new incident only for a distinct reusable root cause, prevention rule, verification lesson, or scope boundary.
- For an exact repeat, update the matching active pattern and current task records without allocating a new incident ID.
- Allocate new IDs as `max(ERR) + 1`; never fill a removed gap, renumber retained records, or reuse a removed ID.
- Keep canonical incidents in fixed 25-ID shards and keep the catalog synchronized with every retained entry.
- Remove obsolete incidents only through an exact manifest, a verified recovery preimage, and a link/reference audit.
- Never treat an incident record as current product authority.

## 8. Verification And Records

- If code changed, run the relevant tests, type checks, lint, build, or key flows and inspect their owning artifacts.
- If a bug was fixed, reproduce the original issue and confirm it is gone.
- If a page or generated asset changed, use its owning workflow and inspect the loaded result.
- Documentation-only changes use structural, phrase, link, path, hygiene, and scope checks as applicable.
- Missing required evidence is a failed or incomplete gate, never a passing result.
- Keep records short, accurate, current, and recoverable. Never copy full chat history, secrets, private data, or transient debug noise.

## 9. Definition Of Done

A task is done only when its acceptance criteria are met, the allowed scope and classification are explainable, required implementation work was actually executed, key results have fresh inspected evidence, required Harness records are current, every required independent Review is complete with zero unresolved blocking findings, and no obvious risk is ignored. Non-blocking suggestions may remain only when recorded once in `.harness/TASK_RESULT.md`. If a required Review is pending, a blocking finding remains, required evidence is missing, or any other applicable gate failed, do not advance or report completion; apply the bounded Review-budget rule and report the next concrete action.
