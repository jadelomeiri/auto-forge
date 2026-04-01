#!/usr/bin/env python3
import json
from pathlib import Path
from datetime import datetime, timezone

CURRENT = Path("orchestration/current-task.json")
TASKS = Path("orchestration/tasks.json")

def now():
    return datetime.now(timezone.utc).isoformat()

def load_json(path: Path):
    return json.loads(path.read_text())

def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2) + "\n")

def set_status(**updates):
    data = load_json(CURRENT)
    for key, value in updates.items():
        data[key] = value
    data["last_updated"] = now()
    save_json(CURRENT, data)

def advance_task():
    current = load_json(CURRENT)
    tasks = load_json(TASKS)

    current_id = current["current_task"]

    for task in tasks["tasks"]:
        if task["id"] == current_id:
            task["status"] = "done"

    next_id = current_id + 1
    current["current_task"] = next_id
    current["status"] = "pending"
    current["builder_status"] = "not_started"
    current["reviewer_status"] = "not_started"
    current["product_status"] = "not_started"
    current["ci_status"] = "not_started"
    current["branch"] = ""
    current["pr_number"] = None
    current["last_updated"] = now()

    save_json(CURRENT, current)
    save_json(TASKS, tasks)

def ready_to_merge():
    data = load_json(CURRENT)
    return (
        data["builder_status"] == "done"
        and data["reviewer_status"] == "approved"
        and data["product_status"] == "approved"
        and data["ci_status"] == "passed"
    )

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        raise SystemExit("Usage: controller.py <command>")

    command = sys.argv[1]

    if command == "builder-done":
        set_status(builder_status="done", status="review")
    elif command == "reviewer-approved":
        set_status(reviewer_status="approved")
    elif command == "reviewer-rejected":
        set_status(reviewer_status="changes_requested", status="needs_changes")
    elif command == "product-approved":
        set_status(product_status="approved")
    elif command == "product-rejected":
        set_status(product_status="changes_requested", status="needs_changes")
    elif command == "ci-passed":
        set_status(ci_status="passed")
    elif command == "ci-failed":
        set_status(ci_status="failed", status="needs_changes")
    elif command == "ready":
        print("READY_TO_MERGE" if ready_to_merge() else "NOT_READY")
    elif command == "advance":
        advance_task()
    else:
        raise SystemExit(f"Unknown command: {command}")