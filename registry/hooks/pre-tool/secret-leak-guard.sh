#!/usr/bin/env bash
# Secret Leak Guard Pre-Tool Hook
set -e

TARGET_FILE="$1"

if [ -z "$TARGET_FILE" ]; then
    exit 0
fi

# Check for hardcoded API key patterns
if grep -qE "sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{30,}|AIzaSy[a-zA-Z0-9_-]{33}" "$TARGET_FILE" 2>/dev/null; then
    echo "❌ SECURITY HOOK ERROR: Secret key pattern detected in $TARGET_FILE!"
    exit 1
fi

echo "✅ Pre-tool security check passed."
