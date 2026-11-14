---
name: harness-init
description: Initialize or adopt a project Harness limited to a derived Project Map and a paged Error Ledger, safely integrate a root AGENTS.md bootstrap, and populate navigation from confirmed repository files. Use when Codex needs to add .harness to a new or existing project or install Project Map and reusable failure-prevention conventions.
---

# Harness Init

Create project navigation and reusable failure prevention without overwriting existing project rules or inventing project facts. Harness maintains only the Project Map and Error Ledger; execution and Review policy belongs to the project's root `AGENTS.md`.

## Execution And Review

- Default to the main Agent performing investigation, implementation, and verification directly. Use an independent Reviewer only when explicitly requested or concrete risk makes independent Review necessary; other Subagents require an explicit user request for delegation.
- Reviewers remain read-only by default. For a suspected P0 finding, they may add, modify, and run narrowly scoped tests and isolated fixtures to reproduce or verify it. Follow single-writer ownership and the project's owning verification workflow; return production fixes to the main Agent.

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
9. Verify the installed structure, root bootstrap, Project Map evidence boundaries, relative links, Error Ledger invariants, Git scope, and diff hygiene before reporting completion.

## Project Map Rules

- Treat the Project Map as a derived, non-normative locator, never as product authority.
- Record repository boundaries; authority and lifecycle; real module responsibility boundaries; direct dependency direction; entry points; deeper documentation; and verification owners.
- Confirm living claims against owning files. Mark missing facts as `Unknown` instead of guessing.
- Keep transient execution state, completion history, incidents, commands, versions, hashes, and test evidence out of the Project Map.
- Update the map in the same change when documents move or module/ownership topology changes.

## Safety And Idempotency

- Use the bundled initializer; do not reproduce its copy or merge logic with ad hoc shell commands.
- Never redirect initialization to a convenience path. The requested project root is part of the mutation boundary.
- Never pass a force or overwrite option; none is supported.
- Preserve an existing root `AGENTS.md`. The initializer may only create or append the bounded block from `assets/root-agents-bootstrap.md`.
- Treat a valid managed `.harness` plus an exact bootstrap block as already initialized. Re-running must not reset a populated Project Map or Error Ledger.
- Treat `.harness` without the managed marker, missing required files, symlinks, partial markers, or edited bootstrap content as conflicts.
- Keep temporary tests outside live project roots and remove only the exact temporary directory created for the test.

## Verification

- Require the initializer's apply result and a second no-op preflight to succeed.
- Confirm the managed structure and `.harness/.harness-init` schema version 1 marker.
- Confirm the root bootstrap points to `.harness/AGENTS.md` and existing root instructions remain byte-for-byte unchanged outside the bounded block.
- For a newly created Harness, confirm `CATALOG.md` reports zero retained records and the first shard contains no canonical `### ERR-NNNN` entry. For an existing Harness, confirm its Project Map and retained Error Ledger content are preserved.
- Validate Markdown links from their installed document directories and run the repository's diff-hygiene check.
- Report failures and remaining conflicts plainly; an incomplete integration is not a successful initialization.

## Resources

- `scripts/init_harness.py`: fail-closed, idempotent `.harness` initializer and root AGENTS bootstrap integrator.
- `assets/harness-template/`: Project Map and Error Ledger files copied into the target project's `.harness` directory.
- `assets/root-agents-bootstrap.md`: exact bounded block created or appended at the project root.
