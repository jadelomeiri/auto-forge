# Forge Review Rubric

Every task implementation should be reviewed against this rubric.

## 1. Scope discipline

- Did the implementation stay within the task scope?
- Did it avoid solving future tasks early?
- Did it avoid unrelated cleanup or refactors?

## 2. Architectural fit

- Does it respect package boundaries from ARCHITECTURE.md?
- Did it avoid taking shortcuts that create future confusion?
- Is the implementation placed in the right package/file?

## 3. Simplicity

- Is the solution the smallest reasonable thing?
- Did it avoid unnecessary abstractions?
- Did it avoid building frameworks inside the framework?

## 4. Readability

- Is the code readable?
- Would a human want to maintain the generated files?
- Are names consistent and clear?

## 5. Product honesty

- Does command output match reality?
- Do docs match actual behavior?
- Are limitations stated clearly where relevant?

## 6. Test quality

- Do tests prove the claimed behavior?
- Are the tests meaningful rather than superficial?
- Were any failures hidden, skipped, or silently weakened?

## 7. Developer experience

- Does the CLI feel coherent?
- Are error messages useful?
- Does the flow feel intentional?

## 8. Merge decision

A task should not be approved if it has one or more of these problems:

- overbuilt solution
- architecture drift
- misleading docs/output
- weak tests for claimed behavior
- obvious future-task leakage
- generated code that feels messy or accidental

When in doubt, reject complexity.