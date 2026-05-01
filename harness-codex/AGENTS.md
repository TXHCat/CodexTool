# AGENTS.md / Codex Harness Rules

## 0. Goal

This project provides a lightweight Codex Harness file set. It records rules, status, results, and errors inside the project so Codex App relies less on long chat history, uses fewer tokens, and verifies work more consistently.

## 1. Global Hard Rules

1. Do not fabricate, guess, fake completion, fake verification, or report unverified results.
2. Do not claim completion without real execution, inspection, tests, logs, screenshots, diffs, or other evidence.
3. Clarify unclear goals, scope, constraints, and acceptance criteria before acting.
4. Break problems down from first principles, then choose the simplest stable path that can be verified.
5. Fix root causes first; do not only patch symptoms.
6. Avoid pointless trial and error. If two attempts add no new information, stop and reframe the problem.
7. Keep code clear, stable, and maintainable. Avoid unnecessary complexity, temporary glue, and fragile structure.
8. Unless explicitly allowed, do not install, download, cache, build, or create project files on the C drive.
9. Record mistakes in the error ledger and check them before later tasks to avoid repeats.
10. User-visible text must be concise, direct, and actionable. Do not expose internals, debug details, model errors, JSON, field names, parameter names, prompts, or system mechanics.

## 2. Default Working Principles

- Do not depend on long chat memory; use project files to preserve state.
- Do not maximize context; read only what the current task actually needs.
- Use the shortest path for simple tasks; reserve full planning for complex tasks.
- For every task, define acceptance criteria, execute, verify, then record.
- Do not report completion without evidence.

## 3. File Roles

- `AGENTS.md`: project-level working rules.
- `README_HOW_TO_USE.md`: human-facing usage guide.
- `PROMPTS.md`: ready-to-copy task prompt templates for Codex.
- `harness/HCA_PROJECT_MAP.md`: compact project map for stable long-term information.
- `harness/TASK_FOCUS_PACK.md`: current task focus pack containing only task-relevant context.
- `harness/TASK_STATUS.md`: short task status for progress recovery.
- `harness/TASK_RESULT.md`: task result evidence pack.
- `harness/ERROR_LEDGER.md`: error ledger used to prevent repeated mistakes.

## 4. Default Execution Order

1. Check `harness/ERROR_LEDGER.md` for related past mistakes.
2. Define the goal, deliverables, acceptance criteria, constraints, risks, and verification method.
3. Update `harness/TASK_FOCUS_PACK.md` with only necessary task context.
4. Read only the files the current task actually needs.
5. Make the smallest necessary change without unrelated refactors.
6. Verify with real evidence such as commands, output, screenshots, diffs, or logs.
7. Update `harness/TASK_STATUS.md` and `harness/TASK_RESULT.md`.
8. If a mistake occurs, update `harness/ERROR_LEDGER.md`.

## 5. Verification Rules

- If a script was written, run it and inspect the output.
- If code changed, run relevant tests, type checks, lint, or key flows.
- If a bug was fixed, reproduce the original issue and confirm it is gone.
- If a page changed, open it and test the key path.
- If copy changed, check that user-visible text is concise, direct, and free of internals.
- If verification fails, do not report completion.

## 6. Recording Rules

Records must be short, accurate, and recoverable. Do not copy full chat history, do not put temporary process details into long-term files, and do not record secrets or private information.

## 7. User-Facing Text Rules

User-facing text should only state what happened, what the user should do next, and information directly related to the task. Do not expose model details, providers, system mechanics, prompts, JSON, field names, parameter names, internal state, or debug data.

## 8. Definition of Done

A task is done only when acceptance criteria are met, work was actually executed, key results were verified, the change scope is explainable, required records are updated, and no obvious risk is ignored.
