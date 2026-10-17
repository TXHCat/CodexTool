# Project Harness

This `.harness` directory provides durable project navigation and reusable failure prevention. A task recovery record is created only when interruption, handoff, or cross-session recovery requires one.

## Core Files

- [AGENTS.md](AGENTS.md): detailed operating rules loaded through the root `AGENTS.md` bootstrap.
- [HCA_PROJECT_MAP.md](HCA_PROJECT_MAP.md): derived, non-normative locator of authority, boundaries, ownership, dependencies, entry points, and verification routes.
- [ERROR_LEDGER.md](ERROR_LEDGER.md): compact entry point into active prevention patterns, the searchable catalog, and canonical fixed 25-ID incident shards.
- [PROMPTS.md](PROMPTS.md): task, continuation, mistake-handling, and review prompts.

## Core Contracts

- Confirm facts from authoritative or owning sources; the Project Map only locates them.
- Update the Project Map when document locations or module/ownership topology change.
- Search Error Ledger patterns and the catalog first, then open only relevant canonical entries.
- Create a new incident only when it adds distinct reusable prevention information; repeated failures and temporary execution problems need no new record.
- Do not report completion without fresh inspected evidence.

See [README_HOW_TO_USE.md](README_HOW_TO_USE.md) for daily operation.
