# Forge Quality Bar

This file defines the quality bar for implementation work.

## Core principles

- Prefer boring code over clever code.
- Prefer small local changes over broad refactors.
- Prefer explicitness over hidden magic.
- Prefer consistency over novelty.
- Prefer honest limitations over inflated claims.

## Generated code quality

Generated code must:

- be readable by a human
- look intentional
- follow conventions consistently
- avoid unnecessary helper layers
- avoid awkward naming
- avoid placeholder-style unfinished feeling where real behavior exists

Generated code should feel like code a developer could keep and edit, not disposable scaffolding.

## Scope discipline

Each task should implement only what the task requires.

Do not:

- implement future tasks early
- add systems “for later”
- redesign architecture unless the task clearly requires it
- add abstractions just because they might be useful later

## Product honesty

Never claim behavior that is not truly implemented.

If something is partial, say so clearly in:

- docs
- error messages
- command output
- summaries

## Testing quality

Tests should prove the claimed behavior.

Do not:

- add shallow tests that only assert files exist when behavior is being claimed
- hide failures to keep CI green
- skip or weaken tests without a clear documented reason

## CLI quality

CLI output should be:

- clear
- calm
- deterministic
- readable
- consistent across commands

Error messages should include:

- what failed
- path or file when relevant
- expected convention
- suggested fix when useful

## Architecture quality

Respect package boundaries defined in ARCHITECTURE.md.

Do not solve local problems by violating package boundaries unless the task explicitly justifies it and the reviewer would likely accept it.

## Documentation quality

Docs must match reality.

Do not:

- oversell
- document future behavior as present behavior
- describe “CRUD” as complete if persistence is not really wired

## Default tie-breaker

When in doubt, choose the option that is:

1. simpler
2. more readable
3. more honest
4. easier to explain