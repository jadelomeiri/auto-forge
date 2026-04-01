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
2. Add label `role:builder` (or comment `/build task:1`).
3. GitHub Action receives event and invokes Codex cloud Builder with task context docs.
4. Builder opens/updates PR and posts summary comment.
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
   - Outputs: PR link comment on issue, labels -> `state:review` + `role:reviewer`.

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

## Exactly how one task is triggered

Example: trigger Task 7.

1. Open issue for Task7 and ensure labels: `task:7`, `state:ready`.
2. Add label `role:builder`.
3. GitHub Action parses `task:7` and calls Codex cloud Builder with:
   - `TASKLIST.md` Task7 section
   - `VISION.md`, `PRODUCT.md`, `PHASE1.md`, `CONVENTIONS.md`, `ARCHITECTURE.md`, `QUALITY_BAR.md`, `REVIEW_RUBRIC.md`
4. Builder creates/updates PR and posts a summary comment.
5. Workflow swaps labels to `state:review` + `role:reviewer`.

---


## Implemented now: minimal Builder-only GitHub loop

A minimal Builder loop is implemented in `.github/workflows/builder-loop.yml`.

### Exact event/trigger model

- `issues.labeled` when label `role:builder` is added.
- `issue_comment.created` with `/build` for manual trigger parity.
- `issue_comment.created` with `/builder-done pr:<pr-number-or-url>` to complete Builder.

### What this workflow does

1. Validates task identification from GitHub issue labels:
   - requires `task:<id>` label
   - requires `state:ready`
2. Moves issue label state to `state:in-progress`.
3. Posts explicit instructions to run Builder in Codex cloud (no custom webhook service).
4. On `/builder-done pr:<...>` comment:
   - records PR reference in an issue comment
   - transitions labels to `state:review` + `role:reviewer`
5. Posts a reusable, standard Builder brief so operators do not need to invent a new prompt each task.

### Honest boundary for Codex-cloud invocation

This workflow intentionally avoids custom infrastructure. The remaining practical manual step is explicit:
- run Builder in Codex cloud against this repository/task
- open/update PR
- comment `/builder-done pr:<pr-number-or-url>` on the issue

CI remains separate in `.github/workflows/ci.yml`; the Builder loop does not mark CI passing.

### Reusable task template format

Use `.github/ISSUE_TEMPLATE/task-builder.md` for task issues. It preloads:
- default labels `state:ready` + `role:builder`
- required context docs
- exact trigger and completion command format

The workflow then posts a standard Codex Builder brief with:
- repo + issue link
- task label id
- fixed source-of-truth docs
- fixed constraints/output contract

## What remains manual after first step

After implementing only the first Builder loop:

- Reviewer and Product-reviewer are still manually triggered.
- Decision comments may be manually interpreted for relabeling.
- Final merge remains manual.
- Retry/recovery policy for failed Codex runs remains manual.

That manual remainder is acceptable for phase-1 orchestration because it is explicit, practical, and avoids pretending full autonomy before integrations are proven.
