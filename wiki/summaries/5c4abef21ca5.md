# DogWood: Monitoring Policies using First Order Temporal Logic

_type: news-summary · created: 2026-09-28 · updated: 2026-10-10 · confidence: high_

`lobsters`

## Summary

AWS is releasing Dogwood, an open-source governance language for agents and their tools, built on first-order temporal logic. The premise: an agent's risk lives at the tool-call boundary, so control should too. AgentCore Policy (in Amazon Bedrock) already makes an allow/deny decision on every tool call using Cedar - fast, analyzable, and deterministic - but Cedar evaluates each request in isolation. It can draw a safety envelope around a single action, not around a sequence. Dogwood adds what Cedar can't express: policies over sequences of actions, so teams can require approval before acting, enforce running rate limits, mandate ordering, or forbid contacting external parties after confidential data has been touched.

Mechanically, Dogwood keeps Cedar's when { ... } for the current request and adds when temporal { ... } clauses that look back over traces of prior events (tool-call requests and outcomes, with arguments and principal). The action schema is generated from the tools an agent already exposes over MCP. It ships inside AgentCore Policy with full Cedar compatibility (no migration), and the language itself is Apache 2.0 open source with a parser, validator and reference interpreter.

## Highlights

- AWS Dogwood: open-source governance language for agent tool use, based on temporal logic
- Cedar handles point-in-time allow/deny; Dogwood governs sequences - ordering, rate limits, prerequisites
- Example policies: approval-before-action; no external contact after accessing confidential data
- New when temporal { ... } clauses evaluate traces of prior events, not just the current request
- Action schema is generated from the agent's MCP tool surface
- Ships in AgentCore Policy, fully Cedar-compatible - existing policies keep working
- Apache 2.0 with parser, validator and reference interpreter

## Source

[Read the original story](https://aws.amazon.com/blogs/opensource/introducing-dogwood-runtime-verification-for-ai-agents/)

## Related pages

_No related entity or concept page yet._
