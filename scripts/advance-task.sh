#!/usr/bin/env bash
set -euo pipefail

DATE_UTC="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

python3 - <<PY
import json
from pathlib import Path

current_path = Path("orchestration/current-task.json")
tasks_path = Path("orchestration/tasks.json")

current = json.loads(current_path.read_text())
tasks = json.loads(tasks_path.read_text())

task_id = current["current_task"]

for task in tasks["tasks"]:
    if task["id"] == task_id:
        task["status"] = "done"

next_task = task_id + 1
current["current_task"] = next_task
current["status"] = "pending"
current["builder_status"] = "not_started"
current["reviewer_status"] = "not_started"
current["product_status"] = "not_started"
current["ci_status"] = "not_started"
current["last_updated"] = "$DATE_UTC"

current_path.write_text(json.dumps(current, indent=2) + "\n")
tasks_path.write_text(json.dumps(tasks, indent=2) + "\n")
PY

echo "Advanced to next task"