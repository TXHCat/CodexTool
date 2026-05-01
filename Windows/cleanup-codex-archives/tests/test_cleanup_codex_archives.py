import contextlib
import io
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import cleanup_codex_archives


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def create_state_db(codex_home: Path) -> None:
    with contextlib.closing(sqlite3.connect(codex_home / "state_5.sqlite")) as connection:
        connection.executescript(
            """
            CREATE TABLE threads (
                id TEXT PRIMARY KEY,
                rollout_path TEXT NOT NULL,
                title TEXT NOT NULL,
                archived INTEGER NOT NULL,
                archived_at INTEGER,
                updated_at_ms INTEGER
            );
            CREATE TABLE thread_dynamic_tools (
                thread_id TEXT NOT NULL,
                position INTEGER NOT NULL,
                name TEXT NOT NULL
            );
            CREATE TABLE thread_spawn_edges (
                parent_thread_id TEXT NOT NULL,
                child_thread_id TEXT NOT NULL
            );
            CREATE TABLE agent_job_items (
                item_id TEXT PRIMARY KEY,
                assigned_thread_id TEXT
            );
            """
        )
        connection.commit()


def create_logs_db(codex_home: Path) -> None:
    with contextlib.closing(sqlite3.connect(codex_home / "logs_2.sqlite")) as connection:
        connection.executescript(
            """
            CREATE TABLE logs (
                id INTEGER PRIMARY KEY,
                thread_id TEXT,
                estimated_bytes INTEGER NOT NULL DEFAULT 0
            );
            """
        )
        connection.commit()


def add_thread(codex_home: Path, thread_id: str, title: str, archived: bool, rollout_path: Path) -> None:
    with contextlib.closing(sqlite3.connect(codex_home / "state_5.sqlite")) as connection:
        connection.execute(
            "INSERT INTO threads (id, rollout_path, title, archived, archived_at, updated_at_ms) VALUES (?, ?, ?, ?, ?, ?)",
            (thread_id, str(rollout_path), title, 1 if archived else 0, 123 if archived else None, 456),
        )
        connection.commit()


def count_rows(codex_home: Path, database: str, table: str) -> int:
    with contextlib.closing(sqlite3.connect(codex_home / database)) as connection:
        return connection.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def run_cli(args: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = cleanup_codex_archives.main(args)
    return code, stdout.getvalue(), stderr.getvalue()


class CleanupCodexArchivesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.codex_home = Path(self.temp_dir.name)
        (self.codex_home / "archived_sessions").mkdir()
        (self.codex_home / "sessions" / "2026" / "04" / "26").mkdir(parents=True)
        create_state_db(self.codex_home)
        create_logs_db(self.codex_home)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def add_archived_thread(self, thread_id: str = "archived-1") -> Path:
        rollout_path = self.codex_home / "archived_sessions" / f"rollout-{thread_id}.jsonl"
        write_jsonl(
            rollout_path,
            [
                {
                    "timestamp": "2026-04-01T00:00:00Z",
                    "type": "session_meta",
                    "payload": {"id": thread_id},
                },
                {"timestamp": "2026-04-01T00:01:00Z", "type": "event_msg", "payload": {}},
            ],
        )
        add_thread(self.codex_home, thread_id, "Archived thread", True, rollout_path)
        return rollout_path

    def add_active_thread(self, thread_id: str = "active-1") -> Path:
        rollout_path = self.codex_home / "sessions" / "2026" / "04" / "26" / f"rollout-{thread_id}.jsonl"
        write_jsonl(
            rollout_path,
            [{"timestamp": "2026-04-01T00:00:00Z", "type": "session_meta", "payload": {"id": thread_id}}],
        )
        add_thread(self.codex_home, thread_id, "Active thread", False, rollout_path)
        return rollout_path

    def add_related_records(self) -> None:
        with contextlib.closing(sqlite3.connect(self.codex_home / "state_5.sqlite")) as connection:
            connection.execute(
                "INSERT INTO thread_dynamic_tools (thread_id, position, name) VALUES (?, ?, ?)",
                ("archived-1", 0, "tool"),
            )
            connection.execute(
                "INSERT INTO thread_dynamic_tools (thread_id, position, name) VALUES (?, ?, ?)",
                ("active-1", 0, "active-tool"),
            )
            connection.execute(
                "INSERT INTO thread_spawn_edges (parent_thread_id, child_thread_id) VALUES (?, ?)",
                ("archived-1", "active-1"),
            )
            connection.execute(
                "INSERT INTO thread_spawn_edges (parent_thread_id, child_thread_id) VALUES (?, ?)",
                ("active-1", "archived-1"),
            )
            connection.execute(
                "INSERT INTO agent_job_items (item_id, assigned_thread_id) VALUES (?, ?)",
                ("archived-item", "archived-1"),
            )
            connection.execute(
                "INSERT INTO agent_job_items (item_id, assigned_thread_id) VALUES (?, ?)",
                ("active-item", "active-1"),
            )
            connection.commit()
        with contextlib.closing(sqlite3.connect(self.codex_home / "logs_2.sqlite")) as connection:
            connection.execute("INSERT INTO logs (thread_id, estimated_bytes) VALUES (?, ?)", ("archived-1", 100))
            connection.execute("INSERT INTO logs (thread_id, estimated_bytes) VALUES (?, ?)", ("archived-1", 50))
            connection.execute("INSERT INTO logs (thread_id, estimated_bytes) VALUES (?, ?)", ("active-1", 75))
            connection.commit()
        write_jsonl(
            self.codex_home / "session_index.jsonl",
            [
                {"id": "archived-1", "thread_name": "Archived thread"},
                {"id": "active-1", "thread_name": "Active thread"},
            ],
        )

    def test_dry_run_preserves_data_and_reports_summary(self) -> None:
        archived_file = self.add_archived_thread()
        self.add_active_thread()
        self.add_related_records()

        code, stdout, stderr = run_cli(["--codex-home", str(self.codex_home)])

        self.assertEqual(code, 0, stderr)
        self.assertIn("Archived threads: 1", stdout)
        self.assertIn(f"Archived JSONL bytes: {archived_file.stat().st_size}", stdout)
        self.assertIn("Log rows: 2", stdout)
        self.assertTrue(archived_file.exists())
        self.assertEqual(count_rows(self.codex_home, "state_5.sqlite", "threads"), 2)
        self.assertEqual(count_rows(self.codex_home, "logs_2.sqlite", "logs"), 3)
        self.assertEqual((self.codex_home / "session_index.jsonl").read_text(encoding="utf-8").count("\n"), 2)

    def test_apply_removes_archived_records_logs_index_and_files(self) -> None:
        archived_file = self.add_archived_thread()
        active_file = self.add_active_thread()
        self.add_related_records()

        code, stdout, stderr = run_cli(["--codex-home", str(self.codex_home), "--apply"])

        self.assertEqual(code, 0, stderr)
        self.assertIn("Applied cleanup.", stdout)
        self.assertFalse(archived_file.exists())
        self.assertTrue(active_file.exists())
        with contextlib.closing(sqlite3.connect(self.codex_home / "state_5.sqlite")) as connection:
            self.assertEqual(connection.execute("SELECT id FROM threads").fetchall(), [("active-1",)])
            self.assertEqual(connection.execute("SELECT thread_id FROM thread_dynamic_tools").fetchall(), [("active-1",)])
            self.assertEqual(connection.execute("SELECT COUNT(*) FROM thread_spawn_edges").fetchone()[0], 0)
            self.assertEqual(connection.execute("SELECT item_id FROM agent_job_items").fetchall(), [("active-item",)])
        with contextlib.closing(sqlite3.connect(self.codex_home / "logs_2.sqlite")) as connection:
            self.assertEqual(connection.execute("SELECT thread_id, estimated_bytes FROM logs").fetchall(), [("active-1", 75)])
        index_text = (self.codex_home / "session_index.jsonl").read_text(encoding="utf-8")
        self.assertNotIn("archived-1", index_text)
        self.assertIn("active-1", index_text)

    def test_json_output_is_machine_readable(self) -> None:
        self.add_archived_thread()

        code, stdout, stderr = run_cli(["--codex-home", str(self.codex_home), "--json"])

        self.assertEqual(code, 0, stderr)
        report = json.loads(stdout)
        self.assertEqual(report["archived_thread_count"], 1)
        self.assertEqual(report["mode"], "dry-run")
        self.assertEqual(report["threads"][0]["id"], "archived-1")

    def test_rollout_path_outside_archived_sessions_fails_without_mutation(self) -> None:
        bad_file = self.codex_home / "sessions" / "2026" / "04" / "26" / "rollout-bad.jsonl"
        write_jsonl(bad_file, [{"type": "session_meta", "payload": {"id": "bad-1"}}])
        add_thread(self.codex_home, "bad-1", "Bad archived thread", True, bad_file)

        code, stdout, stderr = run_cli(["--codex-home", str(self.codex_home), "--apply"])

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("outside archived_sessions", stderr)
        self.assertTrue(bad_file.exists())
        self.assertEqual(count_rows(self.codex_home, "state_5.sqlite", "threads"), 1)

    def test_mismatched_jsonl_session_id_fails_without_mutation(self) -> None:
        rollout_path = self.codex_home / "archived_sessions" / "rollout-bad.jsonl"
        write_jsonl(rollout_path, [{"type": "session_meta", "payload": {"id": "different-id"}}])
        add_thread(self.codex_home, "bad-1", "Bad archived thread", True, rollout_path)

        code, stdout, stderr = run_cli(["--codex-home", str(self.codex_home), "--apply"])

        self.assertEqual(code, 1)
        self.assertEqual(stdout, "")
        self.assertIn("does not match thread id", stderr)
        self.assertTrue(rollout_path.exists())
        self.assertEqual(count_rows(self.codex_home, "state_5.sqlite", "threads"), 1)

    def test_no_archived_threads_succeeds(self) -> None:
        self.add_active_thread()

        code, stdout, stderr = run_cli(["--codex-home", str(self.codex_home)])

        self.assertEqual(code, 0, stderr)
        self.assertIn("Archived threads: 0", stdout)


class BatchScriptTests(unittest.TestCase):
    def test_batch_script_runs_preview_before_confirmed_apply(self) -> None:
        script_path = Path(__file__).resolve().parents[1] / "clean_codex_archives.bat"

        script = script_path.read_text(encoding="utf-8")

        self.assertIn("cleanup_codex_archives.py", script)
        self.assertIn("--codex-home", script)
        self.assertIn("\"%CODEX_HOME%\"", script)
        self.assertIn("choice /c YN", script)
        self.assertLess(script.index("cleanup_codex_archives.py\" --codex-home"), script.index("--apply"))


if __name__ == "__main__":
    unittest.main()
