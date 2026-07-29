# Common Prompts

## 1. New Project Initialization

```text
Initialize this project using the root AGENTS.md and .harness files.

Requirements:
1. Resolve workspace and repository roots and check whether project outputs would be created on the C drive.
2. Read only the root structure, README, dependency configuration, and build/test entry points needed to populate .harness/HCA_PROJECT_MAP.md.
3. Do not change business code or scan unrelated files.
4. Treat HCA_PROJECT_MAP as a derived, non-normative locator of authority, boundaries, ownership, dependencies, entry points, and verification routes.
5. Fill it only from real files and confirmed information. Mark unknowns explicitly and do not guess.
6. Keep task status, completion history, incidents, commands, versions, hashes, and test evidence out of the Project Map.
7. Report inspected files, confirmed modules, missing information, and current progress.
```

## 2. Every New Task

```text
Follow AGENTS.md and .harness rules for this task:

Task:
[describe the task]

Requirements:
1. Read the compact ERROR_LEDGER entry point, search active PATTERNS and CATALOG, and open only matching canonical entries.
2. Define acceptance criteria, related files, out-of-scope areas, risks, and verification method; use TASK_FOCUS_PACK for complex work.
3. Read only authoritative or owning files relevant to this task.
4. As the main Agent, delegate implementation to a bounded implementation subagent with explicit evidence, acceptance checks, and single-writer ownership. Do not permit recursive delegation unless explicitly authorized.
5. Keep the change scope minimal, avoid unrelated refactors, and update HCA_PROJECT_MAP in the same change if documents or module/ownership topology change.
6. Verify the result through the owning route with fresh inspected evidence.
7. Assign a different independent subagent to review the actual diff, artifacts, acceptance, scope, authority and ownership, tests and evidence, and relevant Error Ledger patterns read-only.
8. Validate findings. Fix every valid finding, rerun affected checks, and repeat independent review until zero unresolved findings remain.
9. Update the required TASK_STATUS and TASK_RESULT records.
10. Do not advance or report completion while review is pending, a finding remains, or required evidence is missing. If subagents are unavailable, report the task blocked.
```

## 3. Lightweight Task

```text
Use a lightweight AGENTS.md flow for this task:

Task:
[describe the task]

Requirements:
1. Search the compact Error Ledger indexes for relevant mistakes.
2. Define the goal and allowed scope.
3. Delegate the smallest necessary change to a bounded implementation subagent with single-writer ownership.
4. Verify it with the owning route, then have a different independent subagent review the actual change and evidence read-only.
5. Fix valid findings, rerun affected checks, and repeat review until no unresolved finding remains.
6. Update TASK_STATUS and report briefly only after all gates pass; otherwise report blocked or incomplete.
```

## 4. Continue An In-Progress Task

```text
Continue the current task according to AGENTS.md and .harness rules.

Requirements:
1. Read HCA_PROJECT_MAP, TASK_FOCUS_PACK, TASK_STATUS, and the compact ERROR_LEDGER entry point; search only relevant patterns and catalog entries.
2. Do not depend on chat history or preload every Error Ledger shard.
3. If TASK_STATUS conflicts with actual files, stop and report the mismatch.
4. Confirm the goal, completed work, remaining work, next gate, and verification method.
5. Continue through the required implementation-subagent, owning verification, and independent review loop.
6. Fix valid findings, rerun affected checks, and repeat independent review until no unresolved finding remains.
7. Do not advance or report completion while review is pending, evidence is missing, or a finding remains; report blocked if subagents are unavailable.
8. Update TASK_STATUS and TASK_RESULT when the evidence is complete.
```

## 5. Process A Mistake

```text
A mistake occurred. Follow .harness/ERROR_LEDGER.md and AGENTS.md.

Mistake:
[describe the mistake]

Requirements:
1. Stop the failing execution path.
2. Search PATTERNS and CATALOG to decide whether the failure adds distinct reusable information.
3. For an exact repeat, update the matching pattern and current task records without allocating a new ERR ID.
4. For a distinct failure, allocate max(ERR) + 1 immediately before writing, append the full record to the correct fixed 25-ID shard, and add the catalog entry.
5. Record the symptom, location, root cause, fix, prevention rule, next check, and verification evidence without private data.
6. Update TASK_FOCUS_PACK with the prevention constraint and define the smallest repair plan.
7. Do not continue until the required incident or pattern/task update is complete.
```

## 6. Review A Task

```text
Review this task according to AGENTS.md and .harness rules.

Review scope:
[describe task or change scope]

Requirements:
1. Read TASK_FOCUS_PACK and TASK_RESULT, then search ERROR_LEDGER's active patterns and catalog for the review scope.
2. Inspect the actual diff and fresh verification evidence; do not rely on verbal claims.
3. Be independent from the implementation subagent and remain read-only; do not edit implementation or evidence.
4. Check acceptance criteria, scope and unrelated changes, authority and ownership boundaries, tests and verification evidence, and relevant Error Ledger patterns.
5. Check whether document or module topology changes required a same-change HCA_PROJECT_MAP update.
6. Output pass/fail, evidence, required rework, unresolved findings, remaining risk, and current progress. A pass requires zero unresolved findings.
```
