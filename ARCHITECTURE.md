# Forge — Architecture

repo:

packages/
cli
core
runtime
generators
templates
manifest
docs
create-forge-app

examples/
blog-app

tests/e2e

## cli

commands

new
dev
migrate
generate
explain

## core

model DSL
field DSL
types

## runtime

server
routes
controller
view render

## generators

model
scaffold
app

## templates

files used by generators

## manifest

.forge/manifest.json

## create-forge-app

bootstrap app

## docs

docs site

## Orchestration architecture (Tasks 1–19)

Primary model:

- **GitHub-first control plane**
- **Codex-cloud-first execution plane**

### Control plane (GitHub)

- Task issues (`Task1`..`Task19`) track lifecycle.
- Labels and PR comments encode workflow state.
- PRs are implementation artifacts.
- GitHub checks are the only CI truth.

### Execution plane (Codex cloud)

- Builder agent implements task changes on a branch and updates PR.
- Reviewer agent evaluates against `REVIEW_RUBRIC.md`.
- Product-reviewer agent evaluates against vision/product docs.

### Role/state model

Roles:

- Builder
- Reviewer
- Product-reviewer

States:

- ready
- in-progress
- review
- product-review
- done
- blocked

### Honest boundary

Automated in first practical version:

- Builder trigger from GitHub event.
- PR creation/update.
- Label transitions to review stage.

Still manual initially:

- Reviewer/product-reviewer trigger wiring (until enabled).
- Merge decision execution.
- Exception/retry operations.

## rules

simple
no plugins
no abstractions
no hooks
no magic layers

optimize for readability

optimize for agent navigation
