---
name: harness-init
description: Initialize or adopt an evidence-first project Harness under `.harness`, safely integrate a root AGENTS.md bootstrap, and populate HCA_PROJECT_MAP.md from confirmed repository files. Use when Codex needs to set up Harness in a new or existing project, add a `.harness` directory, standardize task recovery records, or install Project Map and paged Error Ledger conventions.
---

# Harness Init

Create a recoverable project Harness without overwriting existing project rules or inventing project facts.

## Workflow

1. Treat the project root named by the user as an immutable target. Resolve that exact path, applicable `AGENTS.md` files, repository root, and current Git state; never substitute the current directory, home directory, or a different temporary path. Preserve unrelated changes.
2. Inspect only the root README, dependency/build/test configuration, obvious entry points, and existing documentation needed to identify authority, module ownership, and verification routes.
3. Resolve this skill's directory from the loaded `SKILL.md`; do not assume the current working directory.
4. Run the initializer without `--apply` and inspect its complete preflight result:

   ```powershell
   python <skill-root>/scripts/init_harness.py --project-root <absolute-project-root>
   ```

5. Compare the initializer's printed `project_root` with the exact requested target before applying. If they differ, stop. If that exact target is on the C drive, stop unless the current user request explicitly names and authorizes that project root; global Skill installation permission does not authorize C-drive project output. Pass `--allow-c-drive` only for that exact authorization.
6. If preflight reports an unmanaged, incomplete, or conflicting `.harness` or bootstrap block, stop and request direction. Do not overwrite, repair, or bypass the conflict.
7. Apply the exact preflighted initialization:

   ```powershell
   python <skill-root>/scripts/init_harness.py --project-root <absolute-project-root> --apply
   ```

8. Populate `.harness/HCA_PROJECT_MAP.md` from the confirmed project facts gathered in step 2. Keep unknown values as `Unknown`; do not claim planned modules exist.
9. Leave `.harness/TASK_FOCUS_PACK.md`, `.harness/TASK_STATUS.md`, and `.harness/TASK_RESULT.md` as blank templates unless the user separately asks to initialize task records.
10. Verify the installed structure, root bootstrap, Project Map evidence boundaries, relative links, zero-record Error Ledger, Git scope, and diff hygiene before reporting completion.

## Project Map Rules

- Treat the Project Map as a derived, non-normative locator, never as product authority.
- Record repository boundaries; authority and lifecycle; real module responsibility boundaries; direct dependency direction; entry points; deeper documentation; and verification owners.
- Confirm living claims against owning files. Mark missing facts as `Unknown` instead of guessing.
- Keep task status, completion history, incidents, commands, versions, hashes, and test evidence out of the Project Map.
- Update the map in the same change when documents move or module/ownership topology changes.

## Safety And Idempotency

- Use the bundled initializer; do not reproduce its copy or merge logic with ad hoc shell commands.
- Never redirect initialization to a convenience path. The requested project root is part of the mutation boundary.
- Never pass a force or overwrite option; none is supported.
- Preserve an existing root `AGENTS.md`. The initializer may only create or append the bounded block from `assets/root-agents-bootstrap.md`.
- Treat a valid managed `.harness` plus an exact bootstrap block as already initialized. Re-running must not reset a populated Project Map or task records.
- Treat `.harness` without the managed marker, missing required files, symlinks, partial markers, or edited bootstrap content as conflicts.
- Keep temporary tests outside live project roots and remove only the exact temporary directory created for the test.

## Verification

- Require the initializer's apply result and a second no-op preflight to succeed.
- Confirm every template file exists and `.harness/.harness-init` identifies schema version 1.
- Confirm the root bootstrap points to `.harness/AGENTS.md` and existing root instructions remain byte-for-byte unchanged outside the bounded block.
- Confirm `CATALOG.md` reports zero retained records and the first shard contains no canonical `### ERR-NNNN` entry.
- Validate Markdown links from their actual document directories and run the repository's diff-hygiene check.
- Report failures and remaining conflicts plainly; an incomplete integration is not a successful initialization.

## Resources

- `scripts/init_harness.py`: fail-closed, idempotent `.harness` initializer and root AGENTS bootstrap integrator.
- `assets/harness-template/`: files copied into the target project's `.harness` directory.
- `assets/root-agents-bootstrap.md`: exact bounded block created or appended at the project root.
