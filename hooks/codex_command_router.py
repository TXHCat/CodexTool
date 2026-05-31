import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path


HOOK_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE_PATH = HOOK_DIR / "command_templates.json"
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


def load_templates() -> dict:
    template_path = Path(os.environ.get("CODEX_COMMAND_HOOK_TEMPLATES", DEFAULT_TEMPLATE_PATH))
    try:
        with template_path.open("r", encoding="utf-8") as handle:
            parsed = json.load(handle)
    except (OSError, json.JSONDecodeError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def state_dir() -> Path:
    path = Path(os.environ.get("CODEX_COMMAND_HOOK_STATE_DIR", DEFAULT_STATE_DIR))
    path.mkdir(parents=True, exist_ok=True)
    return path


def state_path(payload: dict) -> Path:
    session_id = str(payload.get("session_id") or "unknown-session")
    turn_id = str(payload.get("turn_id") or "unknown-turn")
    safe_name = re.sub(r"[^A-Za-z0-9_.-]+", "_", f"{session_id}_{turn_id}")
    return state_dir() / f"{safe_name}.json"


def first_prompt_token(prompt: str) -> str:
    first_block = prompt.strip().splitlines()[0].strip() if prompt.strip() else ""
    if not first_block.startswith("#"):
        return ""
    return first_block.split(maxsplit=1)[0]


def build_context(command: str, template: dict, prompt: str) -> str:
    lines = [str(item).rstrip() for item in template.get("context", []) if str(item).strip()]
    lines.append("")
    lines.append("原始用户提示以该命令开头；命令词只用于选择协作模板，不应被当成任务正文的一部分。")
    lines.append(f"触发命令：{command}")
    remainder = prompt.strip()[len(command):].strip()
    if remainder:
        lines.append(f"命令后的用户任务正文：{remainder}")
    return "\n".join(lines).strip()


def write_state(payload: dict, command: str, template: dict) -> None:
    state = {
        "command": command,
        "session_id": payload.get("session_id"),
        "turn_id": payload.get("turn_id"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "stop_check_enabled": bool(template.get("stop_check_enabled", False)),
        "requires_checklist": bool(template.get("requires_checklist", False)),
        "required_sections": template.get("required_sections", []),
    }
    state_path(payload).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def main() -> int:
    payload = load_stdin_json()
    if payload.get("hook_event_name") != "UserPromptSubmit":
        return 0

    prompt = str(payload.get("prompt") or "")
    command = first_prompt_token(prompt)
    if not command:
        return 0

    templates = load_templates()
    template = templates.get(command)
    if not isinstance(template, dict):
        return 0

    write_state(payload, command, template)
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": build_context(command, template, prompt),
        }
    }
    sys.stdout.write(json.dumps(output, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
