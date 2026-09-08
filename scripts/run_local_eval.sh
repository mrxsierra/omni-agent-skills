#!/usr/bin/env bash
# ==============================================================================
# omni-agent-skills Local Evaluation Runner
# Supports:
#   1. Mock: Instant deterministic verification (zero API keys, zero network)
#   2. Antigravity CLI (agy): Instant cloud frontier evaluation
#   3. Podman / Docker: Rootless containerized open-weights evaluation (Ollama)
# ==============================================================================

set -euo pipefail

CONTAINER_NAME="omni-ollama-eval"
DEFAULT_OLLAMA_MODEL="qwen2.5-coder:1.5b"
DEFAULT_AGY_MODEL="gemini-3.8-flash-high"
OLLAMA_PORT="11434"

show_usage() {
    cat << 'EOF'
omni-agent-skills Local Evaluation Helper (ADR 0005)

Usage:
  scripts/run_local_eval.sh mock <asset-path>
      Run fast deterministic mock evaluation (< 2s, offline).

  scripts/run_local_eval.sh agy <asset-path> [model]
      Run cloud evaluation via local Antigravity CLI (`agy`).
      Default model: gemini-3.8-flash-high (supports claude-sonnet-4-6, etc.)

  scripts/run_local_eval.sh podman start [model]
      Start a rootless Podman Ollama container and pull the model.
      Default model: qwen2.5-coder:1.5b (or qwen2.5-coder:7b)

  scripts/run_local_eval.sh podman eval <asset-path> [model]
      Run evaluation against the local Podman Ollama container.

  scripts/run_local_eval.sh podman stop
      Stop and remove the local Podman Ollama container.

Examples:
  scripts/run_local_eval.sh mock registry/skills/engineering/clean-code-auditor/SKILL.md
  scripts/run_local_eval.sh agy registry/skills/engineering/clean-code-auditor/SKILL.md
  scripts/run_local_eval.sh podman start qwen2.5-coder:1.5b
  scripts/run_local_eval.sh podman eval registry/skills/engineering/clean-code-auditor/SKILL.md
  scripts/run_local_eval.sh podman stop
EOF
}

detect_container_engine() {
    if command -v podman >/dev/null 2>&1; then
        echo "podman"
    elif command -v docker >/dev/null 2>&1; then
        echo "docker"
    else
        echo "none"
    fi
}

cmd="${1:-}"

if [[ -z "$cmd" || "$cmd" == "-h" || "$cmd" == "--help" || "$cmd" == "help" ]]; then
    show_usage
    exit 0
fi

case "$cmd" in
    mock)
        if [[ $# -lt 2 ]]; then
            echo "Error: Missing asset path." >&2
            echo "Usage: scripts/run_local_eval.sh mock <asset-path>" >&2
            exit 1
        fi
        asset="$2"
        shift 2
        python3 scripts/eval_asset.py --asset "$asset" --provider mock "$@"
        ;;

    agy)
        if [[ $# -lt 2 ]]; then
            echo "Error: Missing asset path." >&2
            echo "Usage: scripts/run_local_eval.sh agy <asset-path> [model]" >&2
            exit 1
        fi
        asset="$2"
        model="${3:-$DEFAULT_AGY_MODEL}"
        shift 2
        if [[ $# -gt 0 ]]; then shift; fi
        python3 scripts/eval_asset.py --asset "$asset" --provider agy --model "$model" "$@"
        ;;

    podman|docker)
        subcmd="${2:-}"
        engine=$(detect_container_engine)
        if [[ "$engine" == "none" ]]; then
            echo "Error: Neither podman nor docker found on PATH." >&2
            exit 1
        fi

        COMPOSE_FILE="docker-compose.eval.yml"
        case "$subcmd" in
            start)
                model="${3:-$DEFAULT_OLLAMA_MODEL}"
                echo "==> Starting $engine container: $CONTAINER_NAME..."
                if command -v "${engine}-compose" >/dev/null 2>&1 || (command -v docker-compose >/dev/null 2>&1 && [[ "$engine" == "docker" ]]); then
                    compose_cmd="${engine}-compose"
                    if ! command -v "$compose_cmd" >/dev/null 2>&1; then compose_cmd="docker-compose"; fi
                    $compose_cmd -f "$COMPOSE_FILE" up -d
                else
                    $engine rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
                    $engine run -d \
                        --name "$CONTAINER_NAME" \
                        -p "${OLLAMA_PORT}:11434" \
                        -v "omni_ollama_models:/root/.ollama" \
                        docker.io/ollama/ollama:latest
                fi

                echo "==> Waiting for Ollama service to become healthy..."
                for i in {1..30}; do
                    if curl -s "http://127.0.0.1:${OLLAMA_PORT}/api/tags" >/dev/null 2>&1; then
                        break
                    fi
                    sleep 1
                done

                echo "==> Pulling model: $model (this may take a minute)..."
                $engine exec "$CONTAINER_NAME" ollama pull "$model"
                echo "==> Ollama ready at http://127.0.0.1:${OLLAMA_PORT} with model $model"
                ;;

            eval)
                if [[ $# -lt 3 ]]; then
                    echo "Error: Missing asset path." >&2
                    echo "Usage: scripts/run_local_eval.sh podman eval <asset-path> [model]" >&2
                    exit 1
                fi
                asset="$3"
                model="${4:-$DEFAULT_OLLAMA_MODEL}"
                echo "==> Running evaluation against containerized Ollama ($model)..."
                python3 scripts/eval_asset.py --asset "$asset" --provider ollama --model "$model"
                ;;

            stop)
                echo "==> Stopping container: $CONTAINER_NAME..."
                $engine stop "$CONTAINER_NAME" >/dev/null 2>&1 || true
                $engine rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
                echo "==> Container stopped and removed."
                ;;

            *)
                echo "Error: Unknown container subcommand: $subcmd" >&2
                echo "Usage: scripts/run_local_eval.sh podman [start|eval|stop]" >&2
                exit 1
                ;;
        esac
        ;;

    *)
        echo "Error: Unknown command: $cmd" >&2
        show_usage
        exit 1
        ;;
esac
