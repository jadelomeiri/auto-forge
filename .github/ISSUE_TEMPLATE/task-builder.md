---
name: Task (Builder)
about: Standard task issue for Codex-cloud Builder loop
title: "Task <id>: <short description>"
labels: ["state:ready", "role:builder"]
---

## Task
- task label: `task:<id>`
- scope: single task only

## Acceptance criteria
- [ ] Linked to relevant TASKLIST.md entry
- [ ] Concrete implementation target described
- [ ] Out-of-scope items explicitly listed

## Context docs
- `TASKLIST.md`
- `VISION.md`
- `PRODUCT.md`
- `PHASE1.md`
- `CONVENTIONS.md`
- `ARCHITECTURE.md`
- `QUALITY_BAR.md`
- `REVIEW_RUBRIC.md`

## Trigger
Add label `role:builder` (or comment `/build`) to start the Builder loop.

## Completion signal
When the Codex Builder PR is open/updated, comment:
`/builder-done pr:<pr-number-or-url>`
