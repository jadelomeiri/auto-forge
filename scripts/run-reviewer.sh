#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:-}"
if [[ -z "$TASK_ID" ]]; then
  echo "Usage: ./scripts/run-reviewer.sh <task-id>"
  exit 1
fi

# TODO: Replace this one line with your real Reviewer agent runner.
FORGE_AGENT_CMD="${FORGE_AGENT_CMD:-forge-agent}"
"$FORGE_AGENT_CMD" run --role reviewer --task-id "$TASK_ID" --output orchestration/review-result.json
