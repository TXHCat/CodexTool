# Harness operating rules

Harness maintains only the Project Map and the Error Ledger. Execution, delegation, independent Review, and verification follow root `AGENTS.md` and the relevant owning workflows.

## Authority

Root `AGENTS.md`, current project descriptors, configuration, source, plugin descriptors, assets, and owning documents are authoritative for their subjects. The Project Map is a derived locator; Error Ledger incidents provide reusable prevention evidence and never override current authority.

## Project Map

Maintain `HCA_PROJECT_MAP.md` from inspected repository files. Record authority locations, workspace and ownership boundaries, module dependencies, entry points, and verification routes. Mark unknowns explicitly and confirm facts at the owning source.

Update the Map when document locations or module/ownership topology change. Keep transient execution state, completion history, incidents, commands, versions, machine-specific absolute paths, hashes, and verification output out of it.

## Error Ledger

Read `ERROR_LEDGER.md`, search `error-ledger/PATTERNS.md` and `error-ledger/CATALOG.md`, and open only relevant canonical entries. Do not preload every shard.

Record a new incident only for distinct reusable root-cause, prevention, or verification information. Exact repeats update a pattern only when reusable guidance changes. Repeated parameter mistakes and temporary offline states do not require new incidents.

Follow `ERROR_LEDGER.md` for ID allocation, fixed 25-ID shards, entry fields, removal safeguards, and catalog synchronization. Preserve retained incidents and keep pattern links, catalog links, and canonical entries consistent.

## Maintenance

Use one writer for overlapping Map or Ledger edits. Check document structure, local links and anchors, paths, scope, and relevant Ledger invariants. Report only inspected or executed evidence; plans and scripts do not prove completion. Keep retained material concise and free of secrets, private data, and transient debug output.
