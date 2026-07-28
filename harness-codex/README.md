# Harness Codex

Harness Codex is a lightweight, evidence-first project collaboration file set. It separates durable project navigation, current task recovery, verified results, and reusable failure prevention so Codex can work without depending on long chat history or loading unrelated context.

## What's Included

- `AGENTS.md`: project operating rules.
- `README_HOW_TO_USE.md`: adoption and daily-use guide.
- `PROMPTS.md`: ready-to-copy task prompts.
- `harness/HCA_PROJECT_MAP.md`: derived, non-normative project locator.
- `harness/TASK_*.md`: current task focus, status, and result templates.
- `harness/ERROR_LEDGER.md`: compact Error Ledger entry point.
- `harness/error-ledger/`: active prevention patterns, searchable incident catalog, and fixed 25-ID canonical entry shards.

## Core Contracts

- Confirm facts from authoritative or owning sources; the Project Map only locates them.
- Keep task status, completion history, incidents, commands, versions, hashes, and test evidence out of the Project Map.
- Update the Project Map when document locations or module/ownership topology change.
- Search Error Ledger patterns and the catalog first, then open only relevant canonical entries.
- Create a new incident only when it adds distinct reusable information. Consolidate exact repeats into the matching pattern and current task records.
- Do not report completion without fresh inspected evidence.

## How To Use

1. Copy this directory's contents into the root of the target project.
2. Adapt the authority, repository-boundary, module, dependency, and verification locators in `harness/HCA_PROJECT_MAP.md` from real project files. Mark unknowns instead of guessing.
3. Ask Codex to read `AGENTS.md`, the compact Project Map, current task records, and `harness/ERROR_LEDGER.md`. It should search only relevant Error Ledger indexes and entries rather than preloading every shard.
4. Use the prompts in `PROMPTS.md` for initialization, implementation, recovery, and review.

See `README_HOW_TO_USE.md` for the complete workflow.

## Recommendations

- Do not commit chat history, accounts, keys, private paths, or other private information.
- Use the full Focus/Status/Result flow for complex or high-risk tasks and a lightweight status flow for narrow changes.
- Preserve deleted Error Ledger IDs as permanent gaps; never renumber or reuse them.
