# When LLM Decompilers Recompile More and Preserve Less

_type: news-summary · created: 2026-10-12 · updated: 2026-10-25 · confidence: high_

`lobsters`

## Summary

This paper argues the metrics used to judge LLM decompilers reward the wrong path. Traditional decompilers like Ghidra expose what they cannot resolve as visible placeholders; LLM decompilers produce clean, idiomatic C judged almost entirely by recompilability and passing shipped input/output tests. The authors show a function can recompile, pass every shipped test, and still diverge on other legitimate inputs - and a disclosed vulnerability can silently disappear from the recompiled code, with no visible trace of the crash.

Their fix is Decompile-Diverge, a behavioral comparison oracle: for each function it synthesizes a driver, grows a fuzzing corpus from the reference binary, and reruns the decompiled code on the same inputs. Across eight systems in nine configurations, candidates passing every shipped test still diverged on 4.9% of inputs overall - up to 13% for a single system - and on 300 GitHub functions and 287 CVE-grounded functions, recompilability and behavioral agreement proved to be different things.

## Highlights

- Recompilability metrics can reward wrong decompilation paths.
- A function can pass every shipped test yet diverge on other legitimate inputs.
- Vulnerabilities can silently vanish from recompiled code.
- Decompile-Diverge: synthesized drivers plus fuzzing-grown corpora as a behavioral oracle.
- Test-passing candidates still diverged 4.9% overall, up to 13% on one system.
- Evaluated on 300 GitHub functions and 287 CVE-grounded functions.

## Source

[Read the original story](https://arxiv.org/abs/2609.05370)

## Related pages

_No related entity or concept page yet._
