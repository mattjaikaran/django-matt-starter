# Specs

Specs for agent-run live in this directory as `<issue-number>.md`. A spec is
the contract for one run.

## Format

```markdown
# <issue number>: <title>

## Goal
The observable end state.

## Files owned
- `path/one.py`
- `path/two.md`

## Verification
- `make lint`
- `make test`

## Decisions
- Anything the agent decided without a human answer.
```

## Files owned

- List every file the run may edit. If a required change falls outside the
  list, stop and report it instead of widening the change.
- Read-only files do not need to be listed.

## Gate

The verification section names the commands that must pass before the pull
request opens. Run them in the repository, not in a scratch copy. Record the
real output in the pull request body.
