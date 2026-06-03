from __future__ import annotations

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


HOOK_DIR = Path(__file__).resolve().parent
DEFAULT_STATE_DIR = HOOK_DIR / "state"


def load_stdin_json() -> dict:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def state_dir() -> Path:
    return Path(os.environ.get("CODEX_COMMAND_HOOK_STATE_DIR", DEFAULT_STATE_DIR))


def state_path(payload: dict) -> Path:
    session_id = str(payload.get("session_id") or "unknown-session")
    turn_id = str(payload.get("turn_id") or "unknown-turn")
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{session_id}_{turn_id}")
    return state_dir() / f"{safe_name}.json"


def load_state(payload: dict) -> tuple[Path, dict | None]:
    path = state_path(payload)
    try:
        parsed = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return path, None
    return path, parsed if isinstance(parsed, dict) else None


def parse_timestamp(value: object) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        return None


def content_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, dict):
                text = item.get("text") or item.get("input_text") or item.get("output_text")
                if text:
                    parts.append(str(text))
            elif item is not None:
                parts.append(str(item))
        return "\n".join(parts)
    return ""


def latest_final_answer_from_transcript(transcript_path: object, created_at: object) -> str:
    if not isinstance(transcript_path, str) or not transcript_path:
        return ""
    state_created_at = parse_timestamp(created_at)
    path = Path(transcript_path)
    if not path.exists():
        return ""

    latest = ""
    try:
        with path.open("r", encoding="utf-8") as handle:
            for line in handle:
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    continue
                payload = record.get("payload") if isinstance(record, dict) else None
                if not isinstance(payload, dict):
                    continue
                if payload.get("type") != "message" or payload.get("role") != "assistant":
                    continue
                if payload.get("phase") != "final_answer":
                    continue
                record_time = parse_timestamp(record.get("timestamp"))
                if state_created_at and record_time and record_time < state_created_at:
                    continue
                if state_created_at and not record_time:
                    continue
                text = content_text(payload.get("content")).strip()
                if text:
                    latest = text
    except OSError:
        return ""
    return latest


def assistant_message(payload: dict, state: dict) -> str:
    transcript_message = latest_final_answer_from_transcript(
        payload.get("transcript_path"),
        state.get("created_at"),
    )
    if transcript_message:
        return transcript_message
    if payload.get("transcript_path"):
        return ""
    direct = payload.get("last_assistant_message")
    if isinstance(direct, str) and direct.strip():
        return direct
    return ""


def missing_requirements(message: str, state: dict) -> list[str]:
    missing: list[str] = []
    for section in state.get("required_sections", []):
        if str(section) not in message:
            missing.append(str(section))
    if state.get("requires_checklist") and not re.search(r"checklist|清单", message, re.IGNORECASE):
        missing.append("checklist/清单")
    return missing


def block_reason(state: dict, missing: list[str]) -> str:
    command = str(state.get("command") or "#command")
    missing_text = "、".join(missing)
    checklist_text = "先核对 checklist/计划项，再" if state.get("requires_checklist") else ""
    return (
        f"{command} 的收尾信息缺少：{missing_text}。"
        f"继续补齐执行闭环：{checklist_text}输出已完成、验证证据、未完成、风险、下一步。"
        "未完成项非空时不要声称完成。"
    )


def main() -> int:
    payload = load_stdin_json()
    if payload.get("hook_event_name") != "Stop":
        return 0
    if payload.get("stop_hook_active"):
        return 0

    path, state = load_state(payload)
    if not state:
        return 0
    if not state.get("stop_check_enabled"):
        try:
            path.unlink()
        except OSError:
            pass
        return 0

    message = assistant_message(payload, state)
    if not message:
        try:
            path.unlink()
        except OSError:
            pass
        return 0

    missing = missing_requirements(message, state)
    if missing:
        output = {"decision": "block", "reason": block_reason(state, missing)}
        sys.stdout.write(json.dumps(output, ensure_ascii=True))
        return 0

    try:
        path.unlink()
    except OSError:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
