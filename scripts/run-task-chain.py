#!/usr/bin/env python3
"""Run Builder -> Reviewer -> Product Reviewer as a single chained trigger.

This script keeps CI separate: it only advances agent-review state in
orchestration/current-task.json. CI status is still updated independently.
"""

import argparse
import json
import subprocess
from pathlib import Path

CURRENT = Path("orchestration/current-task.json")
CONTROLLER = ["python3", "scripts/controller.py"]


def run_cmd(cmd: str, stage: str, task_id: int) -> None:
    rendered = cmd.format(task_id=task_id)
    print(f"[{stage}] running: {rendered}")
    result = subprocess.run(rendered, shell=True)
    if result.returncode != 0:
        raise SystemExit(f"[{stage}] command failed with exit code {result.returncode}")


def controller(command: str) -> None:
    subprocess.run([*CONTROLLER, command], check=True)


def load_json(path: Path) -> dict:
    if not path.exists():
        raise SystemExit(f"Missing required result file: {path}")
    return json.loads(path.read_text())


def apply_reviewer_decision(path: Path) -> None:
    data = load_json(path)
    decision = data.get("decision", "").strip().upper()
    if decision == "MERGE":
        controller("reviewer-approved")
        return
    controller("reviewer-rejected")
    raise SystemExit(f"[reviewer] not approved (decision={decision})")


def apply_product_decision(path: Path) -> None:
    data = load_json(path)
    decision = data.get("decision", "").strip().upper()
    if decision == "PROCEED":
        controller("product-approved")
        return
    controller("product-rejected")
    raise SystemExit(f"[product] not approved (decision={decision})")


def start_task(task_id: int) -> None:
    subprocess.run(["bash", "scripts/start-task.sh", str(task_id)], check=True)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Single-trigger chain for Builder -> Reviewer -> Product Reviewer"
    )
    parser.add_argument("task_id", type=int, help="Task number to execute")
    parser.add_argument(
        "--builder-cmd",
        required=True,
        help=(
            "Command used to run the Builder agent. "
            "Use {task_id} to interpolate task id."
        ),
    )
    parser.add_argument(
        "--reviewer-cmd",
        required=True,
        help=(
            "Command used to run the Reviewer agent. "
            "Use {task_id} to interpolate task id."
        ),
    )
    parser.add_argument(
        "--product-cmd",
        required=True,
        help=(
            "Command used to run the Product reviewer agent. "
            "Use {task_id} to interpolate task id."
        ),
    )
    parser.add_argument(
        "--review-result",
        default="orchestration/review-result.json",
        help="Path to reviewer JSON result file (contains decision)",
    )
    parser.add_argument(
        "--product-result",
        default="orchestration/product-result.json",
        help="Path to product JSON result file (contains decision)",
    )
    parser.add_argument(
        "--no-start",
        action="store_true",
        help="Do not call scripts/start-task.sh (use current task state as-is)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.no_start:
        start_task(args.task_id)

    run_cmd(args.builder_cmd, "builder", args.task_id)
    controller("builder-done")

    run_cmd(args.reviewer_cmd, "reviewer", args.task_id)
    apply_reviewer_decision(Path(args.review_result))

    run_cmd(args.product_cmd, "product", args.task_id)
    apply_product_decision(Path(args.product_result))

    state = json.loads(CURRENT.read_text())
    print("[chain] completed agent sequence")
    print(json.dumps(state, indent=2))
    print("[chain] CI remains separate. Update with scripts/controller.py ci-passed|ci-failed")


if __name__ == "__main__":
    main()
