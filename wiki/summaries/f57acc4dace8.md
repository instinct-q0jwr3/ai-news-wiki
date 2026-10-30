# Discovering and exploiting vulnerabilities in real-world software with Claude

_type: news-summary · created: 2026-10-28 · updated: 2026-10-30 · confidence: high_

`hacker-news` `anthropic`

## Summary

Anthropic used an unreleased internal research model to find and exploit critical vulnerabilities in some of the world's most widely used software, detailing five attack chains with remote code execution and little or no user interaction. One chain pops Calculator from a stock Chrome on macOS seconds after a page loads - a full sandbox escape; another lets any website's JavaScript bypass Safari's same-origin policy to read history, cookies and authenticated responses like email or bank sessions.

The Chrome work produced 62 CVEs, all critical or high, patched as of Chrome 156, including 13 sandbox escapes and 21 renderer-compromise bugs. Everything was reported under coordinated disclosure - 90 days to patch, 45 more before detail discussion - and Anthropic frames browsers and operating systems as the bellwether for measuring model cyber capabilities, since flaws there affect billions.

## Highlights

- Internal Claude research model built multi-step exploit chains for real-world software
- Chrome: 62 CVEs patched in 156, including 13 sandbox escapes
- Safari: full same-origin-policy bypass from any website's JavaScript
- Coordinated disclosure: 90 days to patch, 45 more before public detail

## Source

[Read the original story](https://www.anthropic.com/research/discovering-vulnerabilities-with-claude)

## Related pages

[Anthropic](../entities/anthropic.md)
