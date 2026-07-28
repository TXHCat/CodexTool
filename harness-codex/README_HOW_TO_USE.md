# How To Use

## 1. Purpose

This file set makes Codex read project rules and compact recovery records before working. It reduces irrelevant context, separates authority from derived records, prevents repeated mistakes, and requires evidence for completion.

## 2. Copy The Global Hard Rules

Copy the following content into the custom instructions of Codex Desktop App when project-wide instructions are not already available:

```text
# Codex Global Hard Rules

1. Do not fabricate, guess, fake completion, fake verification, or report unverified results.
2. Do not claim completion without real execution, inspection, tests, logs, screenshots, diffs, or other evidence.
3. Clarify unclear goals, scope, constraints, and acceptance criteria before acting.
4. Break problems down from first principles, then choose the simplest stable path that can be verified.
5. Fix root causes first; do not only patch symptoms.
6. Avoid pointless trial and error. If two attempts add no new information, stop and reframe the problem.
7. Keep code clear, stable, and maintainable. Avoid unnecessary complexity, temporary glue, and fragile structure.
8. Unless explicitly allowed, do not install, download, cache, build, or create project files on the C drive.
9. Process mistakes through the Error Ledger: create an incident only for distinct reusable information; exact repeats update the matching pattern and current task records.
10. Keep user-visible text concise, direct, actionable, and free of internal mechanics or private information.

Default working principles:
- Use project files rather than long chat memory.
- Read only the context required for the current task.
- Use the shortest verified path for narrow tasks and the full recovery flow for complex work.
- Define acceptance criteria, execute, verify, and record.
- Do not report completion without evidence.
```

## 3. Copy Into The Project Root

The installed structure should look like this:

```text
your-project/
|-- AGENTS.md
|-- PROMPTS.md
|-- README_HOW_TO_USE.md
|-- harness/
|   |-- HCA_PROJECT_MAP.md
|   |-- TASK_FOCUS_PACK.md
|   |-- TASK_STATUS.md
|   |-- TASK_RESULT.md
|   |-- ERROR_LEDGER.md
|   `-- error-ledger/
|       |-- PATTERNS.md
|       |-- CATALOG.md
|       `-- entries/
|           `-- ERR-0001-0025.md
`-- your-project-files...
```

Merge with existing project instructions instead of overwriting confirmed project-specific authority, ownership, or verification rules.

## 4. Initialize The Project Map

Populate `harness/HCA_PROJECT_MAP.md` only from real files and confirmed information:

- Resolve workspace and repository boundaries.
- Identify normative, implementation, verification, historical, and derived documents with their lifecycle and ownership.
- Index current module responsibility boundaries, direct dependencies, entry points, deeper documentation, and verification owners.
- Record dependency direction and verification routing.
- Mark unknown information explicitly.

The Project Map is a derived, non-normative locator. Do not store task status, completion history, incidents, commands, versions, hashes, or test evidence in it. Update it in the same change when documents are added, removed, or relocated, or when module/ownership topology changes.

## 5. Start A Task

Ask Codex to use the compact recovery route:

```text
Read AGENTS.md, harness/HCA_PROJECT_MAP.md, the current TASK_FOCUS_PACK and TASK_STATUS, and harness/ERROR_LEDGER.md.
Search the active Error Ledger patterns and catalog for this task, then open only matching canonical entries. Do not preload every shard or unrelated project document.
Define acceptance criteria, make the smallest in-scope change, verify it with real evidence, and update the required task records.
```

## 6. Error Ledger Workflow

1. Search `harness/error-ledger/PATTERNS.md` by failure class.
2. Search `harness/error-ledger/CATALOG.md` by tool, path, module, symptom, or keyword.
3. Open only the linked canonical entry under `harness/error-ledger/entries/`.
4. For an exact repeat, update the matching pattern and current task records without creating a new incident.
5. For a distinct reusable failure, allocate `max(ERR) + 1`, append it to the correct fixed 25-ID shard, and add its catalog record.
6. Preserve removed IDs as permanent gaps. Never renumber or reuse them.

## 7. Daily Use

- Use `PROMPTS.md` for new tasks, continuation, mistake handling, and review.
- Use `TASK_FOCUS_PACK.md` for complex, multi-file, architectural, high-risk, or delegated work.
- Keep `TASK_STATUS.md` short and recoverable; update `TASK_RESULT.md` when evidence is reusable.
- Use module-owned verification routes and inspect the actual output artifact.
- Keep Harness records concise and free of secrets, private data, chat history, and transient debug noise.

## 8. Lightweight Tasks

For a typo, one known field, or another narrow change, define the goal, make the smallest change, verify it, update `TASK_STATUS.md`, and report briefly. Do not weaken verification or Error Ledger lookup merely because the task is small.
