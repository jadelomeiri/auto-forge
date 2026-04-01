#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:-}"
if [[ -z "$TASK_ID" ]]; then
  echo "Usage: ./scripts/run-product.sh <task-id>"
  exit 1
fi

# TODO: Replace this one line with your real Product reviewer agent runner.
FORGE_AGENT_CMD="${FORGE_AGENT_CMD:-forge-agent}"
"$FORGE_AGENT_CMD" run --role product --task-id "$TASK_ID" --output orchestration/product-result.json
