# ERROR_LEDGER

## Purpose

Provide a compact route to reusable failure-prevention rules and retained incident evidence without loading unrelated project history.

## Retrieval Contract

1. Search [active prevention patterns](error-ledger/PATTERNS.md) for the failure class.
2. Search the [incident catalog](error-ledger/CATALOG.md) by tool, path, module, symptom, or keyword.
3. Open only the linked canonical entry under `error-ledger/entries/`.
4. Use full-text shard search only when the catalog does not provide enough recall.

Do not read every shard before a task.

```powershell
# Default lookup
rg -n -i 'keyword|path|tool' .harness/error-ledger/PATTERNS.md .harness/error-ledger/CATALOG.md

# Exact retained incident lookup
rg -n -A 32 '^### ERR-0001\b' .harness/error-ledger/entries
```

## Record Locations

- [PATTERNS.md](error-ledger/PATTERNS.md): consolidated active prevention rules.
- [CATALOG.md](error-ledger/CATALOG.md): complete retained incident lookup.
- `error-ledger/entries/ERR-NNNN-NNNN.md`: canonical fixed 25-ID incident shards.

## Fixed Shard Contract

- Every shard reserves exactly 25 consecutive IDs.
- For incident ID `n`, the shard start is `floor((n - 1) / 25) * 25 + 1`; the shard end is `start + 24`.
- Examples: IDs 1–25 use `ERR-0001-0025.md`; IDs 26–50 use `ERR-0026-0050.md`.
- Create the next shard only when its first retained incident is allocated. The empty template includes `ERR-0001-0025.md` so the first record has a canonical destination.
- A shard's filename and title describe its reserved range, not which IDs are currently retained.

## Rules

- Record a new incident only when it adds a distinct reusable root cause, prevention rule, verification lesson, or scope boundary.
- If a failure exactly repeats an existing cause and prevention rule, update the relevant pattern and current task records instead of creating another `ERR` entry.
- Before work, search only for same or similar failure classes relevant to the task.
- Allocate new IDs as `max(ERR) + 1` immediately before the single writer edits the Ledger. When no incident exists, begin with `ERR-0001`.
- Removed IDs are permanent gaps. Never renumber retained records and never reuse a removed ID.
- Keep every catalog record synchronized with its canonical entry and link it to the correct shard anchor.
- Remove obsolete records only through an exact manifest, a verified recovery preimage, and a link/reference audit.
- Do not infer old dates or rewrite verification without current evidence.
- Do not record keys, accounts, credentials, private paths, chat history, or other private information.
- Current product status comes from living authorities, owning module documents, code/configuration/assets, current task records, and fresh verification—not from an incident record.

## Adding A Record

1. Use one writer for all affected Ledger files.
2. Search the patterns and catalog. If the failure adds no distinct reusable information, update the matching pattern/task record and stop.
3. Otherwise derive and allocate `max(ERR) + 1`; never fill a deleted gap.
4. Append the record to the fixed 25-ID shard, creating the shard from the established header format only when its range is first used.
5. Add one concise catalog record with scope, keywords, related retained IDs, an evidence-derived title, and a link to the canonical entry.
6. Add or update an active pattern when the prevention rule should become a default cross-task guard.
7. Verify unique IDs, correct shard ranges, required fields, catalog/entry count parity, local links and anchors, and representative retrieval queries.

## Catalog Record Format

```text
- [ERR-0001](entries/ERR-0001-0025.md#err-0001) · scope: module, tool · keywords: term-a, term-b · Evidence-derived searchable title.
```

## Entry Template

```text
### ERR-0001 — Short searchable title

Recorded:
- YYYY-MM-DD

Scope:
- Module, tool, or workflow boundary

Keywords:
- Two to six stable retrieval terms

Related:
- Retained ERR-NNNN or None

Symptom:
- Not filled

Location:
- Not filled

Root cause:
- Not filled

Fix:
- Not filled

Prevention rule:
- Not filled

Must check next time:
- Not filled

Verification:
- Not filled
```
