# auto-forge

## Autonomous task chain (single trigger)

This repo now supports a **single command trigger** that runs the three-agent sequence in order:

1. Builder
2. Reviewer
3. Product reviewer

Use:

```bash
python3 scripts/run-task-chain.py <task_id> \
  --builder-cmd '<builder command with {task_id}>' \
  --reviewer-cmd '<reviewer command with {task_id}>' \
  --product-cmd '<product command with {task_id}>' \
  --review-result orchestration/review-result.json \
  --product-result orchestration/product-result.json
```

### What this chain updates automatically

- Starts the task state (`scripts/start-task.sh`) unless `--no-start` is used.
- Marks Builder done when Builder command exits successfully.
- Reads reviewer decision JSON and sets reviewer status:
  - `MERGE` => approved
  - anything else => changes requested (chain stops)
- Reads product decision JSON and sets product status:
  - `PROCEED` => approved
  - anything else => changes requested (chain stops)

### What remains intentionally separate/manual

- **CI status remains separate and honest by design.**
- The chain does **not** mark CI passed automatically.
- CI must still update independently using:

```bash
python3 scripts/controller.py ci-passed
# or
python3 scripts/controller.py ci-failed
```

### Current tooling reality

Full chaining is possible only if your environment can run each agent non-interactively from a command (the `--*-cmd` values).

If your local/CI agent runner cannot be called via command line yet, then invoking the Builder/Reviewer/Product commands is still the missing piece; the chain script is already in place to orchestrate once those commands exist.
