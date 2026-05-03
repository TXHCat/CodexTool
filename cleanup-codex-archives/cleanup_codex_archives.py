#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import json
import os
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


class CleanupError(Exception):
    pass


@dataclass(frozen=True)
class ArchivedThread:
    id: str
    title: str
    rollout_path: Path
    jsonl_bytes: int


@dataclass(frozen=True)
class CleanupReport:
    codex_home: Path
    archived_threads: tuple[ArchivedThread, ...]
    log_rows: int
    log_bytes: int
    mode: str

    @property
    def archived_jsonl_bytes(self) -> int:
        return sum(thread.jsonl_bytes for thread in self.archived_threads)


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean archived Codex App chat records after validating Codex state.",
    )
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=None,
        help="Codex data directory. Defaults to CODEX_HOME, then ~/.codex.",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Permanently delete archived chat records. Without this flag, only prints a dry-run report.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print a machine-readable JSON report.",
    )
    return parser.parse_args(argv)


def resolve_codex_home(raw_path: Path | None) -> Path:
    if raw_path is not None:
        return raw_path.expanduser().resolve()
    env_path = os.environ.get("CODEX_HOME")
    if env_path:
        return Path(env_path).expanduser().resolve()
    return (Path.home() / ".codex").resolve()


def quote_placeholders(values: Sequence[str]) -> str:
    return ", ".join("?" for _ in values)


def open_sqlite_readonly(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise CleanupError(f"Required SQLite database not found: {path}")
    uri = path.as_uri() + "?mode=ro"
    return sqlite3.connect(uri, uri=True)


def read_session_id_from_jsonl(path: Path) -> str:
    if not path.is_file():
        raise CleanupError(f"Archived rollout file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        first_line = handle.readline()
    if not first_line:
        raise CleanupError(f"Archived rollout file is empty: {path}")
    try:
        first = json.loads(first_line)
    except json.JSONDecodeError as exc:
        raise CleanupError(f"Archived rollout file has invalid first JSON line: {path}: {exc}") from exc

    if first.get("type") != "session_meta":
        raise CleanupError(f"Archived rollout file first record is not session_meta: {path}")
    payload = first.get("payload")
    if not isinstance(payload, dict) or not isinstance(payload.get("id"), str):
        raise CleanupError(f"Archived rollout file session_meta.payload.id is missing: {path}")
    return payload["id"]


def ensure_inside_archived_sessions(codex_home: Path, rollout_path: Path) -> Path:
    archived_dir = (codex_home / "archived_sessions").resolve()
    resolved_rollout = rollout_path.resolve()
    try:
        resolved_rollout.relative_to(archived_dir)
    except ValueError as exc:
        raise CleanupError(f"Archived rollout path is outside archived_sessions: {resolved_rollout}") from exc
    return resolved_rollout


def collect_archived_threads(codex_home: Path) -> tuple[ArchivedThread, ...]:
    state_db = codex_home / "state_5.sqlite"
    with contextlib.closing(open_sqlite_readonly(state_db)) as connection:
        rows = connection.execute(
            "SELECT id, title, rollout_path FROM threads WHERE archived = 1 ORDER BY archived_at DESC, updated_at_ms DESC, id"
        ).fetchall()

    archived_threads: list[ArchivedThread] = []
    for thread_id, title, rollout_path_text in rows:
        rollout_path = ensure_inside_archived_sessions(codex_home, Path(rollout_path_text))
        session_id = read_session_id_from_jsonl(rollout_path)
        if session_id != thread_id:
            raise CleanupError(
                f"Archived rollout file session id {session_id!r} does not match thread id {thread_id!r}: {rollout_path}"
            )
        archived_threads.append(
            ArchivedThread(
                id=thread_id,
                title=title,
                rollout_path=rollout_path,
                jsonl_bytes=rollout_path.stat().st_size,
            )
        )
    return tuple(archived_threads)


def collect_log_totals(codex_home: Path, thread_ids: Sequence[str]) -> tuple[int, int]:
    logs_db = codex_home / "logs_2.sqlite"
    with contextlib.closing(open_sqlite_readonly(logs_db)) as connection:
        if not thread_ids:
            return (0, 0)
        placeholders = quote_placeholders(thread_ids)
        row = connection.execute(
            f"SELECT COUNT(*), COALESCE(SUM(estimated_bytes), 0) FROM logs WHERE thread_id IN ({placeholders})",
            tuple(thread_ids),
        ).fetchone()
    return int(row[0]), int(row[1])


def build_report(codex_home: Path, apply: bool) -> CleanupReport:
    archived_threads = collect_archived_threads(codex_home)
    thread_ids = [thread.id for thread in archived_threads]
    log_rows, log_bytes = collect_log_totals(codex_home, thread_ids)
    return CleanupReport(
        codex_home=codex_home,
        archived_threads=archived_threads,
        log_rows=log_rows,
        log_bytes=log_bytes,
        mode="apply" if apply else "dry-run",
    )


def delete_state_records(codex_home: Path, thread_ids: Sequence[str]) -> None:
    if not thread_ids:
        return
    placeholders = quote_placeholders(thread_ids)
    with contextlib.closing(sqlite3.connect(codex_home / "state_5.sqlite")) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            params = tuple(thread_ids)
            connection.execute(f"DELETE FROM thread_dynamic_tools WHERE thread_id IN ({placeholders})", params)
            connection.execute(
                f"DELETE FROM thread_spawn_edges WHERE parent_thread_id IN ({placeholders}) OR child_thread_id IN ({placeholders})",
                params + params,
            )
            connection.execute(f"DELETE FROM agent_job_items WHERE assigned_thread_id IN ({placeholders})", params)
            connection.execute(f"DELETE FROM threads WHERE id IN ({placeholders})", params)
            connection.commit()
        except Exception:
            connection.rollback()
            raise


def delete_log_records(codex_home: Path, thread_ids: Sequence[str]) -> None:
    if not thread_ids:
        return
    placeholders = quote_placeholders(thread_ids)
    with contextlib.closing(sqlite3.connect(codex_home / "logs_2.sqlite")) as connection:
        connection.execute("BEGIN IMMEDIATE")
        try:
            connection.execute(f"DELETE FROM logs WHERE thread_id IN ({placeholders})", tuple(thread_ids))
            connection.commit()
        except Exception:
            connection.rollback()
            raise


def rewrite_session_index(codex_home: Path, thread_ids: set[str]) -> None:
    index_path = codex_home / "session_index.jsonl"
    if not index_path.exists():
        return
    kept_lines: list[str] = []
    with index_path.open("r", encoding="utf-8") as handle:
        for line in handle:
            record = json.loads(line)
            if record.get("id") not in thread_ids:
                kept_lines.append(line)
    with index_path.open("w", encoding="utf-8", newline="") as handle:
        handle.writelines(kept_lines)


def apply_cleanup(codex_home: Path, archived_threads: Sequence[ArchivedThread]) -> None:
    thread_ids = [thread.id for thread in archived_threads]
    delete_state_records(codex_home, thread_ids)
    delete_log_records(codex_home, thread_ids)
    rewrite_session_index(codex_home, set(thread_ids))
    for thread in archived_threads:
        thread.rollout_path.unlink()


def report_to_dict(report: CleanupReport) -> dict:
    return {
        "codex_home": str(report.codex_home),
        "mode": report.mode,
        "archived_thread_count": len(report.archived_threads),
        "archived_jsonl_bytes": report.archived_jsonl_bytes,
        "log_rows": report.log_rows,
        "log_bytes": report.log_bytes,
        "threads": [
            {
                "id": thread.id,
                "title": thread.title,
                "rollout_path": str(thread.rollout_path),
                "jsonl_bytes": thread.jsonl_bytes,
            }
            for thread in report.archived_threads
        ],
    }


def print_text_report(report: CleanupReport, applied: bool) -> None:
    print(f"Codex home: {report.codex_home}")
    print(f"Mode: {report.mode}")
    print(f"Archived threads: {len(report.archived_threads)}")
    print(f"Archived JSONL bytes: {report.archived_jsonl_bytes}")
    print(f"Log rows: {report.log_rows}")
    print(f"Log estimated bytes: {report.log_bytes}")
    if applied:
        print("Applied cleanup.")
    else:
        print("Dry-run only. Re-run with --apply to permanently delete these archived chats.")


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    try:
        codex_home = resolve_codex_home(args.codex_home)
        report = build_report(codex_home, args.apply)
        if args.apply:
            apply_cleanup(codex_home, report.archived_threads)
        if args.json:
            print(json.dumps(report_to_dict(report), ensure_ascii=False, indent=2))
        else:
            print_text_report(report, applied=args.apply)
        return 0
    except (CleanupError, sqlite3.Error, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
