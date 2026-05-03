#!/bin/sh
set -u

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CLEANUP_SCRIPT="$SCRIPT_DIR/cleanup_codex_archives.py"

if [ -z "${CODEX_HOME:-}" ]; then
    CODEX_HOME="$HOME/.codex"
fi

if command -v python3 >/dev/null 2>&1; then
    PYTHON_CMD=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON_CMD=python
else
    echo "error: Python was not found. Install Python or add it to PATH." >&2
    exit 1
fi

if [ ! -f "$CLEANUP_SCRIPT" ]; then
    echo "error: cleanup script not found: $CLEANUP_SCRIPT" >&2
    exit 1
fi

echo "Codex home: \"$CODEX_HOME\""
echo
echo "Previewing archived chat cleanup. No changes will be made in this step."
echo
if ! "$PYTHON_CMD" "$CLEANUP_SCRIPT" --codex-home "$CODEX_HOME"; then
    echo
    echo "Preview failed. Cleanup was not applied."
    exit 1
fi

echo
echo "Close Codex App before applying cleanup."
printf "Permanently delete the archived chats listed above? [Y/N] "
read -r answer
case "$answer" in
    [Yy])
        ;;
    *)
        echo
        echo "Cleanup cancelled."
        exit 0
        ;;
esac

echo
echo "Applying cleanup."
"$PYTHON_CMD" "$CLEANUP_SCRIPT" --codex-home "$CODEX_HOME" --apply
exit_code=$?
echo
if [ "$exit_code" -ne 0 ]; then
    echo "Cleanup failed."
else
    echo "Cleanup completed."
fi
exit "$exit_code"
