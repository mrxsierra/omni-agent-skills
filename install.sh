#!/usr/bin/env bash
# Cross-Platform POSIX Installer for omni-agent-skills (Linux / macOS / WSL / Git Bash)
set -e

OS_TYPE="$(uname -s 2>/dev/null || echo "Unknown")"
echo "🚀 Installing omni-agent-skills (v0.0.1) on ${OS_TYPE}..."

# Determine User Home Directory safely
USER_HOME="${HOME:-~}"
TARGET_DIR="${USER_HOME}/.omni-agent-skills"

mkdir -p "${TARGET_DIR}/skills" "${TARGET_DIR}/rules"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Copy files cross-platform
cp -r "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/skills/" 2>/dev/null || cp -R "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/skills/"
cp -r "${SCRIPT_DIR}/rules/"* "${TARGET_DIR}/rules/" 2>/dev/null || cp -R "${SCRIPT_DIR}/rules/"* "${TARGET_DIR}/rules/"
cp "${SCRIPT_DIR}/registry.json" "${TARGET_DIR}/"
cp "${SCRIPT_DIR}/llms.txt" "${TARGET_DIR}/"

echo "✅ Installation complete!"
echo "📍 Installed to: ${TARGET_DIR}"
