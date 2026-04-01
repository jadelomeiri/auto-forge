# auto-forge

## Pivot: Codex-cloud-first + GitHub-first orchestration

This repository is now oriented around a **GitHub control plane** and **Codex cloud execution**.

### Design goals for Tasks 1–19

1. GitHub is the source of truth for task state.
2. Codex cloud does implementation/review work where available.
3. PRs, labels, comments, and statuses drive flow.
4. Roles are explicit: **Builder**, **Reviewer**, **Product-reviewer**.
5. We clearly separate what is automatable today vs what remains manual.

---

## Smallest practical target architecture

### Control plane (GitHub)

- **Issues** represent Task1..Task19 (one issue per task).
- **Labels** represent stage/state, e.g.:
  - `task:<id>`
  - `role:builder`, `role:reviewer`, `role:product`
  - `state:ready`, `state:in-progress`, `state:review`, `state:product-review`, `state:done`, `state:blocked`
- **PR** is the execution artifact for a task.
- **Comments** are used for handoffs and manual approvals/rejections.
- **Commit status / checks** represent CI truth; orchestration must not fake them.

### Execution plane (Codex cloud)

- Builder role runs in Codex cloud (or closest available hosted runner) to create code changes and open/update PR.
- Reviewer role runs in Codex cloud to evaluate implementation against `REVIEW_RUBRIC.md` and post decision comment.
- Product-reviewer role runs in Codex cloud to evaluate product fit against `VISION.md`, `PRODUCT.md`, `QUALITY_BAR.md` and post decision comment.

### Role contract

- **Builder output**: branch + PR + summary comment.
- **Reviewer output**: `MERGE` or `CHANGES_REQUESTED` decision comment.
- **Product-reviewer output**: `PROCEED` or `CHANGES_REQUESTED` decision comment.
- **CI output**: pass/fail from GitHub checks only.

---

## Honest automation boundary (today)

What can be automated today (smallest practical level):

- Triggering from GitHub labels/comments.
- Running a single Builder pass in Codex cloud.
- Posting role decisions as structured PR comments.
- Moving labels based on explicit role decisions.

What likely remains manual in the first step:

- Exact provisioning/auth details for Codex cloud org setup.
- Final merge click after human confirmation.
- Resolving ambiguous reviewer/product feedback loops.
- Any capability not exposed by currently available Codex cloud/GitHub integration endpoints.

---

## What to keep, simplify, remove from current local orchestration

### Keep

- `orchestration/tasks.json` as canonical task list context.
- `scripts/controller.py` state transition logic as reference behavior.
- `REVIEW_RUBRIC.md`, `QUALITY_BAR.md`, and source-of-truth docs used by role prompts.

### Simplify

- Keep `scripts/run-task-chain.py` only as a **local fallback simulator**, not primary architecture.
- Keep thin role wrappers only for local/dev debugging.

### Remove (as primary path)

- Dependence on local shell-chain as the main execution model.
- Assumption that task progression is driven from workstation commands.

---

## Smallest first implementation step

Implement one GitHub-driven Builder loop for a single task (then generalize to 1..19):

1. Create/confirm issue `Task1` with `task:1` + `state:ready`.
2. Add label `role:builder`.
3. GitHub Action receives event and invokes Codex cloud Builder with task context docs.
4. Builder runs via `openai/codex-action@v1` and posts a summary comment to the issue.
5. Action sets `state:review` and applies `role:reviewer`.

This is the smallest useful Codex-cloud-first foundation because it proves:
- GitHub is in control,
- Codex cloud can perform real implementation,
- state transitions happen via GitHub artifacts.

---

## Proposed GitHub workflow / event model

### Events

- `issues.labeled` (preferred initial trigger)
- `issue_comment.created` (optional slash-command trigger)
- `pull_request` + `pull_request_review` + `check_suite.completed` for downstream transitions

### Minimal workflow graph

1. **Builder workflow**
   - Trigger: issue labeled `role:builder` and `state:ready`.
   - Action: run Codex Builder for task id from `task:<id>` label.
   - Outputs: Builder result comment on the issue, labels -> `state:review` + `role:reviewer`.

2. **Reviewer workflow**
   - Trigger: PR labeled `role:reviewer` or issue labeled `state:review`.
   - Action: run Codex Reviewer; post structured decision.
   - Decision handling:
     - `MERGE` -> `state:product-review`, label `role:product`.
     - else -> `state:in-progress`, label `role:builder`.

3. **Product-review workflow**
   - Trigger: `role:product`.
   - Action: run Codex Product-reviewer; post structured decision.
   - Decision handling:
     - `PROCEED` -> wait for CI + manual merge.
     - else -> back to Builder.

4. **CI workflow**
   - Independent and honest; no orchestration job marks CI passed.

---


## Confirmed vs inferred (Codex Action foundation)

Confirmed in this repo today:
- `.github/workflows/codex-builder.yml` triggers on `issues.labeled` when `role:builder` is applied.
- The workflow requires `state:ready` and `task:<id>` labels.
- It runs `openai/codex-action@v1`, requires non-empty Builder output plus repo changes, and then creates/updates a Builder PR.
- It then relabels the issue from Builder to Reviewer (`state:review`, `role:reviewer`).

Inferred / intentionally deferred in this first step:
- PR creation is handled by an explicit GitHub step (`peter-evans/create-pull-request@v7`), not guaranteed directly by `openai/codex-action@v1`.
- Reviewer and Product-reviewer automation are not wired yet.
- Merge execution remains manual and CI remains independent.

## Exactly how one task is triggered

Example: trigger Task 7.

1. Open issue for Task7 and ensure labels: `task:7`, `state:ready`.
2. Add label `role:builder`.
3. GitHub Action parses `task:7` and calls Codex cloud Builder with:
   - `TASKLIST.md` Task7 section
   - `VISION.md`, `PRODUCT.md`, `PHASE1.md`, `CONVENTIONS.md`, `ARCHITECTURE.md`, `QUALITY_BAR.md`, `REVIEW_RUBRIC.md`
4. Workflow creates/updates a Builder PR, then posts a summary comment with the PR URL.
5. Workflow swaps labels to `state:review` + `role:reviewer`.

---

## What remains manual after first step

After implementing only the first Builder loop:

- Reviewer and Product-reviewer are still manually triggered.
- Decision comments may be manually interpreted for relabeling.
- Final merge remains manual.
- Retry/recovery policy for failed Codex runs remains manual.

That manual remainder is acceptable for phase-1 orchestration because it is explicit, practical, and avoids pretending full autonomy before integrations are proven.
