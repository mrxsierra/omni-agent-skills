#!/usr/bin/env bash
# Secret Leak Guard Pre-Tool Hook
set -e

TARGET_FILE="$1"
SECRET_REGEX="sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{30,}|AIzaSy[a-zA-Z0-9_-]{33}|AKIA[0-9A-Z]{16}|BEGIN (RSA|OPENSSH|EC|PRIVATE) KEY"

if [ -n "$TARGET_FILE" ] && [ -f "$TARGET_FILE" ]; then
    if grep -qE "$SECRET_REGEX" "$TARGET_FILE" 2>/dev/null; then
        echo "❌ SECURITY HOOK ERROR: Secret key pattern detected in $TARGET_FILE!"
        exit 1
    fi
elif [ -n "$TARGET_FILE" ]; then
    if echo "$TARGET_FILE" | grep -qE "$SECRET_REGEX"; then
        echo "❌ SECURITY HOOK ERROR: Secret key pattern detected in input!"
        exit 1
    fi
else
    # Read from stdin if piped
    if [ ! -t 0 ]; then
        if grep -qE "$SECRET_REGEX" - 2>/dev/null; then
            echo "❌ SECURITY HOOK ERROR: Secret key pattern detected in stdin stream!"
            exit 1
        fi
    fi
fi

echo "✅ Pre-tool security check passed."
