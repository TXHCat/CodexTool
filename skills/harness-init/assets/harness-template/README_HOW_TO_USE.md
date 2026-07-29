# How To Use

## 1. Purpose

This Harness reduces irrelevant context, separates authority from derived records, prevents repeated mistakes, and requires evidence for completion.

## 2. Rule Entry

The root `AGENTS.md` contains a bounded Harness integration block. It requires Codex to read and follow `.harness/AGENTS.md` before project work. Do not remove or partially edit either marker.

## 3. Project Map

Populate [HCA_PROJECT_MAP.md](HCA_PROJECT_MAP.md) only from real files and confirmed information:

- Resolve workspace and repository boundaries.
- Identify normative, implementation, verification, historical, and derived documents with their lifecycle and ownership.
- Index current module responsibility boundaries, direct dependencies, entry points, deeper documentation, and verification owners.
- Record dependency direction and verification routing.
- Mark unknown information explicitly.

The Project Map is a derived, non-normative locator. Do not store task status, completion history, incidents, commands, versions, hashes, or test evidence in it. Update it in the same change when documents move or module/ownership topology changes.

## 4. Start A Task

Use this compact recovery route:

```text
Read AGENTS.md, .harness/HCA_PROJECT_MAP.md, the current TASK_FOCUS_PACK and TASK_STATUS, and .harness/ERROR_LEDGER.md.
Search active Error Ledger patterns and the catalog, then open only matching canonical entries. Do not preload every shard or unrelated project document.
Define acceptance criteria, delegate only the smallest necessary in-scope implementation with no unrelated refactors or authority expansion, verify it with real evidence, and send it to an independent read-only review.
Fix valid findings, rerun affected checks, and repeat review until zero unresolved findings remain before updating the completed task records or advancing.
```

## 5. Task Execution And Review Gate

The main Agent runs tasks in order. For each task:

1. Delegate implementation to a bounded implementation subagent that makes only the smallest necessary in-scope change, with no unrelated refactors or authority expansion, using the required evidence, acceptance checks, and one writer per file. That subagent must not delegate again unless explicitly authorized.
2. Run and inspect the owning verification route.
3. Assign a different subagent to review the actual diff, artifacts, scope, authority and ownership, tests and evidence, and relevant Error Ledger patterns. Review is read-only.
4. Validate the findings, fix every valid issue, rerun affected checks, and request another independent review.
5. Repeat until the latest review has zero unresolved findings. Only then may the main Agent continue to the next task or report completion.

If implementation or review subagents are unavailable, report the task blocked; do not silently skip the gate. The main Agent owns integration, and reviewers never edit implementation or evidence.

## 6. Error Ledger Workflow

1. Search `.harness/error-ledger/PATTERNS.md` by failure class.
2. Search `.harness/error-ledger/CATALOG.md` by tool, path, module, symptom, or keyword.
3. Open only the linked canonical entry under `.harness/error-ledger/entries/`.
4. For an exact repeat, update the matching pattern and current task records without creating a new incident.
5. For a distinct reusable failure, allocate `max(ERR) + 1`, append it to the correct fixed 25-ID shard, and add its catalog record.
6. Preserve removed IDs as permanent gaps. Never renumber or reuse them.

## 7. Daily Use

- Use [PROMPTS.md](PROMPTS.md) for new tasks, continuation, mistake handling, and review.
- Use [TASK_FOCUS_PACK.md](TASK_FOCUS_PACK.md) for complex, multi-file, architectural, high-risk, or delegated work.
- Keep [TASK_STATUS.md](TASK_STATUS.md) short and recoverable; update [TASK_RESULT.md](TASK_RESULT.md) when evidence is reusable.
- Use module-owned verification routes and inspect the actual output artifact.
- Keep Harness records concise and free of secrets, private data, chat history, and transient debug noise.

## 8. Lightweight Tasks

For a typo, one known field, or another narrow change, keep planning and records lightweight and make only the smallest necessary in-scope change, with no unrelated refactors or authority expansion, while retaining Error Ledger lookup, the implementation-subagent gate, owning verification, and independent review.
