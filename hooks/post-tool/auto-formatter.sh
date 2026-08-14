#!/usr/bin/env bash
# Auto-Formatter Post-Tool Hook
set -e

TARGET_FILE="$1"

if [ -z "$TARGET_FILE" ]; then
    exit 0
fi

if [[ "$TARGET_FILE" == *.py ]] && command -v black &>/dev/null; then
    black --quiet "$TARGET_FILE"
elif [[ "$TARGET_FILE" == *.js || "$TARGET_FILE" == *.ts || "$TARGET_FILE" == *.tsx ]] && command -v prettier &>/dev/null; then
    prettier --write "$TARGET_FILE" &>/dev/null
fi

echo "✅ Post-tool auto-format complete."
