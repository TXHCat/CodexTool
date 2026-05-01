# Harness Codex

This is a lightweight project collaboration file set for Codex. It stores project rules, current task context, verification results, and error records in the project root so Codex relies less on long chat history, reads less irrelevant context, and works with more consistent verification.

## What's Included

- `AGENTS.md`: project working rules.
- `README_HOW_TO_USE.md`: detailed usage guide.
- `PROMPTS.md`: ready-to-copy prompt templates.
- `harness/`: templates for project map, task focus, task status, task result, and error ledger.

## How To Use

1. Copy these global hard rules into the custom instructions of Codex Desktop App:

```text
# Codex Global Hard Rules

You must always follow these rules:

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

Default working principles:

- Do not depend on long chat memory; use project files to preserve state.
- Do not maximize context; read only what the current task actually needs.
- Use the shortest path for simple tasks; reserve full planning for complex tasks.
- For every task, define acceptance criteria, execute, verify, then record.
- Do not report completion without evidence.
```

2. Copy all contents of this repository into the root directory of your target project.
3. Ask Codex to read every document before starting:

```text
Please read AGENTS.md, README_HOW_TO_USE.md, PROMPTS.md, and every document under harness/. Then start the project under these rules.
```

## Recommendations

- Do not commit chat history, accounts, keys, private paths, or other private information.
- For complex tasks, update `harness/TASK_FOCUS_PACK.md` first.
- Do not mark a task complete without real verification evidence.
- After a mistake, write it into `harness/ERROR_LEDGER.md` to avoid repeating it.
