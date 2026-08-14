#!/usr/bin/env bash
# omni-agent-skills 1-Click Installer
set -e

echo "🚀 Installing omni-agent-skills..."

TARGET_DIR="${HOME}/.gemini/config"
REPO_URL="https://github.com/mrxsierra/omni-agent-skills"

mkdir -p "${TARGET_DIR}/skills" "${TARGET_DIR}/rules"

echo "📦 Syncing skills to ${TARGET_DIR}/skills..."
# Copy skills into global config directory
if [ -d "skills" ]; then
    cp -r skills/* "${TARGET_DIR}/skills/"
    echo "✅ Skills installed successfully!"
else
    echo "ℹ️ Run this script from the omni-agent-skills repository root."
fi

echo "🛡️ omni-agent-skills installation complete!"
