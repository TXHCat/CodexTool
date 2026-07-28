#!/usr/bin/env python3
"""Safely initialize a managed .harness directory and root AGENTS bootstrap."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import shutil
import sys
import tempfile


BEGIN_MARKER = "<!-- harness-init:start -->"
END_MARKER = "<!-- harness-init:end -->"
MANAGED_MARKER = "schema_version=1\nmanaged_by=harness-init\n"


class HarnessInitError(RuntimeError):
    """A fail-closed preflight or apply error."""


def is_c_drive(path: Path) -> bool:
    """Return True when a resolved Windows path is on the C drive."""
    return path.drive.rstrip(":").casefold() == "c"


def read_utf8_preserving_newlines(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as stream:
        return stream.read()


def write_utf8_preserving_newlines(path: Path, content: str) -> None:
    with path.open("w", encoding="utf-8", newline="") as stream:
        stream.write(content)


def normalized_newlines(content: str) -> str:
    return content.replace("\r\n", "\n").replace("\r", "\n")


def template_inventory(template_root: Path) -> list[Path]:
    if not template_root.is_dir():
        raise HarnessInitError(f"Template directory is missing: {template_root}")
    inventory = sorted(
        path.relative_to(template_root)
        for path in template_root.rglob("*")
        if path.is_file()
    )
    if not inventory:
        raise HarnessInitError("Harness template contains no files.")
    for relative in inventory:
        source = template_root / relative
        if source.is_symlink():
            raise HarnessInitError(f"Template symlinks are not allowed: {relative}")
    return inventory


def validate_bootstrap_content(content: str) -> None:
    normalized = normalized_newlines(content).strip("\n")
    if normalized.count(BEGIN_MARKER) != 1 or normalized.count(END_MARKER) != 1:
        raise HarnessInitError("Bundled root bootstrap markers are invalid.")
    if normalized.index(BEGIN_MARKER) >= normalized.index(END_MARKER):
        raise HarnessInitError("Bundled root bootstrap marker order is invalid.")


def render_root_agents(existing: str | None, bootstrap: str) -> tuple[str | None, str]:
    """Return the replacement content, or None when the exact block exists."""
    validate_bootstrap_content(bootstrap)
    expected = normalized_newlines(bootstrap).strip("\n")

    if existing is None or existing == "":
        return f"# AGENTS.md\n\n{expected}\n", "create"

    normalized = normalized_newlines(existing)
    begin_count = normalized.count(BEGIN_MARKER)
    end_count = normalized.count(END_MARKER)
    if begin_count == 0 and end_count == 0:
        newline = "\r\n" if "\r\n" in existing else "\n"
        block = expected.replace("\n", newline)
        if existing.endswith(f"{newline}{newline}"):
            separator = ""
        elif existing.endswith(newline):
            separator = newline
        else:
            separator = f"{newline}{newline}"
        return f"{existing}{separator}{block}{newline}", "append"

    if begin_count != 1 or end_count != 1:
        raise HarnessInitError("Root AGENTS.md contains partial or duplicate harness markers.")

    start = normalized.index(BEGIN_MARKER)
    end_start = normalized.index(END_MARKER)
    if start >= end_start:
        raise HarnessInitError("Root AGENTS.md harness marker order is invalid.")
    end = end_start + len(END_MARKER)
    installed = normalized[start:end]
    if installed != expected:
        raise HarnessInitError("Root AGENTS.md harness bootstrap content conflicts with the bundled block.")
    return None, "unchanged"


def inspect_harness(harness_root: Path, template_root: Path, inventory: list[Path]) -> str:
    if not harness_root.exists():
        return "create"
    if harness_root.is_symlink() or not harness_root.is_dir():
        raise HarnessInitError("Existing .harness is not a regular directory.")

    marker = harness_root / ".harness-init"
    if marker.is_symlink() or not marker.is_file():
        raise HarnessInitError("Existing .harness is unmanaged; marker is missing.")
    if normalized_newlines(read_utf8_preserving_newlines(marker)) != MANAGED_MARKER:
        raise HarnessInitError("Existing .harness has an unsupported managed marker.")

    missing = [relative for relative in inventory if not (harness_root / relative).is_file()]
    if missing:
        formatted = ", ".join(relative.as_posix() for relative in missing)
        raise HarnessInitError(f"Managed .harness is incomplete; missing: {formatted}")
    return "unchanged"


def verify_staged_copy(stage: Path, template_root: Path, inventory: list[Path]) -> None:
    for relative in inventory:
        source = template_root / relative
        copied = stage / relative
        if not copied.is_file() or copied.read_bytes() != source.read_bytes():
            raise HarnessInitError(f"Staged template verification failed: {relative.as_posix()}")


def apply_changes(
    project_root: Path,
    harness_action: str,
    agents_action: str,
    agents_content: str | None,
    template_root: Path,
    inventory: list[Path],
) -> None:
    harness_root = project_root / ".harness"
    agents_path = project_root / "AGENTS.md"
    stage: Path | None = None
    agents_temp: Path | None = None
    published_harness = False

    try:
        if harness_action == "create":
            stage = Path(tempfile.mkdtemp(prefix=".harness-init-stage-", dir=project_root))
            shutil.copytree(template_root, stage, dirs_exist_ok=True, copy_function=shutil.copy2)
            verify_staged_copy(stage, template_root, inventory)

        if agents_action in {"create", "append"}:
            if agents_content is None:
                raise HarnessInitError("Root AGENTS replacement content is missing.")
            descriptor, temp_name = tempfile.mkstemp(
                prefix=".AGENTS.md.harness-init-", suffix=".tmp", dir=project_root
            )
            os.close(descriptor)
            agents_temp = Path(temp_name)
            write_utf8_preserving_newlines(agents_temp, agents_content)

        if stage is not None:
            stage.rename(harness_root)
            published_harness = True
            stage = None

        if agents_temp is not None:
            os.replace(agents_temp, agents_path)
            agents_temp = None
    except Exception:
        if published_harness and harness_action == "create" and harness_root.is_dir():
            shutil.rmtree(harness_root)
        raise
    finally:
        if stage is not None and stage.exists():
            shutil.rmtree(stage)
        if agents_temp is not None and agents_temp.exists():
            agents_temp.unlink()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preflight or apply a managed project .harness structure."
    )
    parser.add_argument("--project-root", required=True, help="Absolute project root path")
    parser.add_argument("--apply", action="store_true", help="Apply the preflighted changes")
    parser.add_argument(
        "--allow-c-drive",
        action="store_true",
        help="Allow project writes on the C drive after explicit user permission",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    raw_root = Path(args.project_root).expanduser()
    if not raw_root.is_absolute():
        print("[ERROR] --project-root must be absolute.", file=sys.stderr)
        return 2

    project_root = raw_root.resolve()
    if not project_root.is_dir():
        print(f"[ERROR] Project root does not exist or is not a directory: {project_root}", file=sys.stderr)
        return 2
    if args.apply and is_c_drive(project_root) and not args.allow_c_drive:
        print("[ERROR] C-drive project writes require explicit permission and --allow-c-drive.", file=sys.stderr)
        return 2

    skill_root = Path(__file__).resolve().parent.parent
    asset_root = skill_root / "assets"
    template_root = asset_root / "harness-template"
    bootstrap_path = asset_root / "root-agents-bootstrap.md"

    try:
        inventory = template_inventory(template_root)
        bootstrap = read_utf8_preserving_newlines(bootstrap_path)
        harness_action = inspect_harness(project_root / ".harness", template_root, inventory)

        agents_path = project_root / "AGENTS.md"
        if agents_path.is_symlink() or (agents_path.exists() and not agents_path.is_file()):
            raise HarnessInitError("Root AGENTS.md must be absent or a regular UTF-8 file.")
        existing_agents = (
            read_utf8_preserving_newlines(agents_path) if agents_path.exists() else None
        )
        agents_content, agents_action = render_root_agents(existing_agents, bootstrap)

        mode = "APPLY" if args.apply else "CHECK"
        print(f"[{mode}] project_root={project_root}")
        print(f"[{mode}] .harness={harness_action}")
        print(f"[{mode}] AGENTS.md={agents_action}")
        print(f"[{mode}] template_files={len(inventory)}")

        if args.apply:
            apply_changes(
                project_root,
                harness_action,
                agents_action,
                agents_content,
                template_root,
                inventory,
            )
            print("[OK] Harness initialization applied and verified for publication.")
        else:
            print("[OK] Preflight passed; no files were changed.")
        return 0
    except (HarnessInitError, UnicodeError, OSError) as error:
        print(f"[ERROR] {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
