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
3. Choose the record flow: a narrow task may use short recovery records; complex, multi-file, architectural, high-risk, or delegated work uses the full Focus/Status/Result flow.
4. Read only the relevant authorities, owning module documentation, Project Map locators, and current task records.
5. The main Agent orchestrates tasks in order and delegates the current implementation to a bounded implementation subagent that makes only the smallest necessary in-scope change, with no unrelated refactors or authority expansion, using explicit evidence inputs, acceptance checks, and single-writer ownership.
6. Verify through the owning module's route and inspect the actual output, not only the command invocation.
7. Assign a different independent subagent to review the actual diff, artifacts, and verification evidence read-only against acceptance, scope, authority and ownership, tests, and relevant Error Ledger patterns.
8. Validate every finding. Fix each valid finding, rerun affected checks, and send the modified task through another independent review. Repeat until no finding remains unresolved.
9. Update the required Harness recovery records with concise current state and reusable evidence.
10. If a mistake or missed verification occurs, follow `.harness/ERROR_LEDGER.md` before proceeding.

Do not preload every Error Ledger shard or every project document.

Do not advance to the next task or report completion while a finding remains, review is pending, or required evidence is missing.

## 6. Subagent Execution And Review Gates

- The main Agent owns the ordered task sequence, integration decisions, finding validation, and final reporting.
- Delegate every implementation to a bounded implementation subagent that makes only the smallest necessary in-scope change, with no unrelated refactors or authority expansion, using explicit inputs, outputs, constraints, evidence, acceptance checks, and single-writer ownership. The implementation subagent must not recursively delegate unless the main Agent explicitly authorizes it.
- After implementation and owning-route verification, assign a different independent review subagent to inspect the actual diff, artifacts, acceptance criteria, scope, authority and ownership boundaries, tests and evidence, and relevant Error Ledger patterns.
- The reviewer is read-only and never edits implementation or evidence.
- The main Agent validates review findings. Every valid finding must be fixed, affected checks rerun, and the modified task independently reviewed again until zero unresolved findings remain.
- Do not begin the next task or report completion while review is pending, a finding remains unresolved, or required evidence is missing. If subagents are unavailable, report the task blocked instead of skipping implementation or review.
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

A task is done only when its acceptance criteria are met, the allowed scope is explainable, delegated implementation was actually executed, key results have fresh inspected evidence, required Harness records are current, the latest independent review is complete with zero unresolved findings, and no obvious risk is ignored. If review is pending, a valid finding remains, required evidence is missing, or any other gate failed, do not advance or report completion; report the task as incomplete or blocked with the next concrete action.
