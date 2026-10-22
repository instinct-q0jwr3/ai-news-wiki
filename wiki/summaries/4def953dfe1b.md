# Quoting Geoffrey Huntley

_type: news-summary · created: 2026-10-13 · updated: 2026-10-22 · confidence: high_

`simon-willison` `agentic-systems`

## Summary

Geoffrey Huntley, quoted by Simon Willison, says that instead of updating AGENTS.md when an agent ignores his diagnostics library, he writes a pre-commit hook that fails the commit on direct calls to observability modules and injects a prompt telling the agent to use the library. After that, compliance goes to ten out of ten.

## Highlights

- Instructions in AGENTS.md drift; a pre-commit hook enforces the rule.
- Hook inspects the git diff for calls that bypass the diagnostics module.
- Failed commit injects a corrective prompt, giving 10/10 compliance.

## Source

[Read the original story](https://simonwillison.net/2026/Oct/13/geoffrey-huntley/)

## Related pages

[Agentic systems](../concepts/agentic-systems.md)
