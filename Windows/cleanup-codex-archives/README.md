# Codex Archived Chat Cleaner

Zero-dependency Python CLI for cleaning Codex App archived chats.

The tool treats `state_5.sqlite` as the source of truth and only targets rows where
`threads.archived = 1`. It validates each archived rollout JSONL before doing any
destructive work.

## Usage

One-click cleanup on Windows:

```powershell
.\clean_codex_archives.bat
```

The batch script previews the cleanup first, then asks for `Y/N` confirmation
before running the irreversible `--apply` step.

Preview the cleanup for the default Codex home:

```powershell
python .\cleanup_codex_archives.py
```

Preview a specific Codex home:

```powershell
python .\cleanup_codex_archives.py --codex-home C:\Users\jakec\.codex
```

Output a JSON report:

```powershell
python .\cleanup_codex_archives.py --json
```

Permanently delete archived chat data:

```powershell
python .\cleanup_codex_archives.py --codex-home C:\Users\jakec\.codex --apply
```

## Safety Model

By default the command is a dry-run and does not modify files or SQLite databases.
`--apply` is irreversible.

Before running `--apply`, close Codex App so SQLite databases and JSONL files are
not being actively written.

The tool deletes only records and files associated with archived thread IDs:

- `state_5.sqlite`: `threads`, `thread_dynamic_tools`, `thread_spawn_edges`, and
  `agent_job_items` rows assigned to archived threads.
- `logs_2.sqlite`: `logs` rows whose `thread_id` is archived.
- `session_index.jsonl`: lines whose `id` is archived.
- `archived_sessions`: JSONL files whose validated `session_meta.payload.id`
  matches the archived thread ID.

It does not clean active sessions and does not infer targets from titles, dates, or
filenames.

## Validation Rules

The command fails before applying changes when:

- `state_5.sqlite` or `logs_2.sqlite` is missing.
- An archived `rollout_path` is outside `<codex-home>\archived_sessions`.
- The archived JSONL file is missing, empty, invalid JSON, or does not start with
  `session_meta`.
- The JSONL `session_meta.payload.id` does not exactly match the SQLite thread ID.

## Tests

Run the unit tests:

```powershell
python -m unittest tests.test_cleanup_codex_archives -v
```
