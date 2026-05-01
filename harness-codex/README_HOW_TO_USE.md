# How To Use

## 1. Purpose

This file set makes Codex App read project rules and state files before working. The goal is to reduce irrelevant context, save tokens, avoid repeated mistakes, and require evidence for completion.

## 2. Step 1: Copy The Global Hard Rules

First, copy the following content into the custom instructions of Codex Desktop App.

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

## 3. Step 2: Copy Into Your Project Root

Copy all contents of this repository into the root of your target project. The result should look like this:

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
|   `-- ERROR_LEDGER.md
`-- your-project-files...
```

## 4. Step 3: Ask Codex To Read The Docs

In the target project, send this to Codex:

```text
Please read AGENTS.md, README_HOW_TO_USE.md, PROMPTS.md, and every document under harness/.
After reading them, start the project under these rules:
1. Check ERROR_LEDGER first.
2. Define acceptance criteria for the current task.
3. Read only the files needed for the current task.
4. Verify changes with real evidence.
5. Update TASK_STATUS and TASK_RESULT after completion.
6. Do not report completion without evidence.
```

## 5. Daily Use

- Use templates from `PROMPTS.md` for new tasks.
- Update `TASK_FOCUS_PACK.md` before complex tasks.
- Update `TASK_STATUS.md` at each meaningful checkpoint.
- Update `TASK_RESULT.md` when a task is done.
- Update `ERROR_LEDGER.md` after mistakes or rework.
- Do not commit chat history, accounts, keys, private paths, or other private data.

## 6. When Not To Use The Full Flow

For small tasks such as typo fixes, checking one known field, or changing one line of copy, use a lightweight flow: define the goal, make the smallest change, verify it, and report briefly.
