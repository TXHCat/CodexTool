# HCA_PROJECT_MAP

## Purpose

This is a derived, non-normative long-term index. Use it to locate authority, repository boundaries, module ownership, dependency direction, entry points, and verification routes; confirm living claims against the authoritative or owning source.

Do not store task status, completion history, incident records, commands, versions, hashes, or test evidence here. Populate this map only from real files and confirmed information. Mark unknowns explicitly instead of guessing.

## Repository Boundaries

- Workspace root: Unknown
- Repository root or roots: Unknown
- Active application or package root: Unknown
- Generated-output boundaries: Unknown
- Vendor or externally owned boundaries: Unknown
- Historical or reference-only boundaries: Unknown

## Authority And Lifecycle

Classify each important source by lifecycle and ownership. Examples include `Living normative`, `Living implementation`, `Operational verification`, `Derived non-normative`, `Frozen historical`, and `Unknown`.

| Source | Lifecycle | Owns | Evidence / confirmation source |
|---|---|---|---|
| Not filled | Unknown | Not filled | Not filled |

Harness records are operational and derived. They do not override product requirements, owning module documentation, code, configuration, assets, or fresh verification evidence.

## Module Index

Create one row per real first-party responsibility boundary. Do not create rows for planned modules that do not yet exist.

| Layer or area | Module and responsibility boundary | Direct dependencies | Entry points / deeper docs / verification owner |
|---|---|---|---|
| Unknown | Not filled | Not filled | Not filled |

Update this index in the same change when a module is added, removed, relocated, split, merged, or changes ownership, direct dependencies, entry points, lifecycle, generated-asset ownership, or verification routing.

## Dependency And Ownership Direction

- Project-owned dependency notation: `consumer -> direct dependency`.
- Confirmed dependency edges: Not filled
- Runtime authority owner: Unknown
- Generated-asset owner: Unknown
- Integration boundaries: Unknown
- Forbidden dependency directions: Unknown

## Verification Routing

- Module-local verification owner and command/document: Unknown
- Cross-module verification route: Unknown
- Generated-asset verification route: Unknown
- Required evidence artifact and interpretation: Unknown
- Documentation-only verification route: structural, phrase, relative-link, path, hygiene, and scope checks as applicable.

Adding, removing, or relocating a discovered authority, module README, focused reference, entry point, or verification owner invalidates the affected locator and requires a same-change Project Map update.

## Task Recovery

- [TASK_FOCUS_PACK](TASK_FOCUS_PACK.md): current complex-task context, constraints, and acceptance focus.
- [TASK_STATUS](TASK_STATUS.md): short progress state and next recovery gate.
- [TASK_RESULT](TASK_RESULT.md): verified outcomes, evidence pointers, and known gaps.
- [ERROR_LEDGER](ERROR_LEDGER.md): compact retrieval and write contract; do not preload every incident shard.
- [Error patterns](error-ledger/PATTERNS.md): consolidated active prevention rules.
- [Error catalog](error-ledger/CATALOG.md): complete retained lookup into fixed 25-ID canonical incident shards; removed IDs are permanent gaps and are never reused.
