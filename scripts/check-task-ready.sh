#!/usr/bin/env bash
set -euo pipefail

python3 - <<PY
import json
from pathlib import Path

data = json.loads(Path("orchestration/current-task.json").read_text())

ok = (
    data["builder_status"] == "done" and
    data["reviewer_status"] == "approved" and
    data["product_status"] == "approved" and
    data["ci_status"] == "passed"
)

if ok:
    print("READY_TO_MERGE")
else:
    print("NOT_READY")
    print(json.dumps(data, indent=2))
    raise SystemExit(1)
PY