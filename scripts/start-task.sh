#!/usr/bin/env bash
set -euo pipefail

TASK_ID="${1:-}"
if [[ -z "$TASK_ID" ]]; then
  echo "Usage: ./scripts/start-task.sh <task-number>"
  exit 1
fi

DATE_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

python3 - <<PY
import json
from pathlib import Path

path = Path("orchestration/current-task.json")
data = json.loads(path.read_text())
data["current_task"] = int("$TASK_ID")
data["status"] = "in_progress"
data["builder_status"] = "pending"
data["reviewer_status"] = "not_started"
data["product_status"] = "not_started"
data["ci_status"] = "not_started"
data["last_updated"] = "$DATE_UTC"
path.write_text(json.dumps(data, indent=2) + "\n")
PY

echo "Started Task $TASK_ID"