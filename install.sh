#!/usr/bin/env bash
# Cross-Platform POSIX Installer for omni-agent-skills (Linux / macOS / WSL / Git Bash)
# Safety-minded installer: prefer local-install and pinned releases.
set -euo pipefail

OS_TYPE="$(uname -s 2>/dev/null || echo "Unknown")"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

USER_HOME="${HOME:-~}"
TARGET_DIR="${USER_HOME}/.omni-agent-skills"

# Defaults
LOCAL=false
TAG=""
CHECK=false
SHA256_EXPECTED=""

usage() {
  cat <<EOF
Usage: $0 [--local] [--tag <tag>] [--check --sha256 <sha256>]

Options:
  --local            Install from files in the local checkout (safe default)
  --tag <tag>        Specify a release tag (e.g. v1.2.3) when validating artifacts
  --check --sha256 X Validate the tarball ./omni-agent-skills-<tag>.tar.gz against expected SHA256
  -h, --help         Show this help and exit

Security notes:
  - Do NOT pipe remote scripts directly to a shell. Fetch releases by pinned tag and verify checksums/signatures.
  - This installer will refuse to fetch remote artifacts unless explicitly run in a controlled workflow. See INSTALL.md for guidance.
EOF
}

if [[ ${#} -eq 0 ]]; then
  echo "No arguments provided. Defaulting to safe local-only mode is recommended. Use --help for options."
fi

# parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --local)
      LOCAL=true
      shift
      ;;
    --tag|--version)
      TAG="$2"
      shift 2
      ;;
    --check)
      CHECK=true
      shift
      ;;
    --sha256)
      SHA256_EXPECTED="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1"
      usage
      exit 2
      ;;
  esac
done

if [[ "$LOCAL" != "true" ]]; then
  # conservative default: do not fetch remote content from the network
  if [[ -z "${TAG:-}" ]]; then
    echo "Refusing to fetch remote content without a pinned tag/--tag."
    echo "See INSTALL.md for secure install instructions."
    exit 1
  fi
  echo "Remote install for tag ${TAG} was requested, but this script is intentionally conservative."
  echo "Please download the release tarball and run this script with --check --sha256 <expected-sha256>, or run locally with --local."
  exit 1
fi

# LOCAL install: copy files from this checkout into the user's home dir
mkdir -p "${TARGET_DIR}/skills" "${TARGET_DIR}/rules"

# Copy files cross-platform
cp -r "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/skills/" 2>/dev/null || cp -R "${SCRIPT_DIR}/skills/"* "${TARGET_DIR}/skills/"
cp -r "${SCRIPT_DIR}/rules/"* "${TARGET_DIR}/rules/" 2>/dev/null || cp -R "${SCRIPT_DIR}/rules/"* "${TARGET_DIR}/rules/"
cp "${SCRIPT_DIR}/registry.json" "${TARGET_DIR}/" || true
cp "${SCRIPT_DIR}/llms.txt" "${TARGET_DIR}/" || true

echo "✅ Installation complete!"
echo "📍 Installed to: ${TARGET_DIR}"

# --check mode: validate a local tarball (no network fetches)
if [[ "$CHECK" == "true" ]]; then
  if [[ -z "${TAG:-}" ]]; then
    echo "--check requires --tag <tag> to locate the tarball (omni-agent-skills-<tag>.tar.gz)."
    exit 2
  fi
  TARFILE="./omni-agent-skills-${TAG}.tar.gz"
  if [[ ! -f "$TARFILE" ]]; then
    echo "Tarball $TARFILE not found in current directory. Download the release artifact to this folder and re-run with --check."
    exit 3
  fi
  if [[ -z "${SHA256_EXPECTED:-}" ]]; then
    echo "No expected sha256 provided. Use --sha256 <value> to validate the file.
    Example: $0 --check --tag v1.2.3 --sha256 <expected-sha256>"
    exit 4
  fi
  echo "Verifying SHA256 for $TARFILE..."
  CALC_SHA256=$(sha256sum "$TARFILE" | awk '{print $1}')
  if [[ "$CALC_SHA256" != "$SHA256_EXPECTED" ]]; then
    echo "SHA256 mismatch! expected: $SHA256_EXPECTED actual: $CALC_SHA256"
    exit 5
  fi
  echo "SHA256 check passed."
fi
