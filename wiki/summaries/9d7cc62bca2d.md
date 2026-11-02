# Securing Internet-Critical Software: How We Could Have Backdoored Bash

_type: news-summary · created: 2026-11-02 · updated: 2026-11-02 · confidence: high_

`lobsters`

## Summary

Security firm Hacktron pointed its AI pentest agent at GNU Savannah - the volunteer-run forge that hosts Bash, Coreutils and most of the GNU userland - and walked away with a path to backdooring Bash itself. The root bug is almost embarrassing: Savane's email validator accepts addresses like a`touch${IFS}/tmp/savane-rce-proof`@attacker.example, and its 'Test GPG keys' feature concatenates the account email straight into a shell command. Any registered user got code execution on the backend.

From there the chain was methodical: read the database credentials from Savane's config, flip the superuser flag on their own account, use the admin 'Become this user' box to impersonate Chet Ramey - Bash's maintainer - and confirm the site would accept a new SSH key granting push access to bash.git. They stopped before adding one. An attacker who didn't stop could have pushed commits to upstream Bash, Coreutils, or any Savannah project, packaged downstream to millions of machines - the xz scenario, minus the years of patient social engineering. An unpatched 5.15 kernel with the 2023 GameOver(lay) OverlayFS bugs gave them root and access to a GNU backup server for good measure.

The window was about two months: the FSF traced the vulnerable code path to the March 7, 2026 Savane release, and Hacktron reported on May 11. The full sweep found 26 confirmed vulnerabilities, all fixed, with an incident report published. Two lessons matter beyond GNU: AI-assisted auditing is now good enough to find internet-critical bugs in a weekend against infrastructure maintained by a handful of volunteers - and the security of the entire free-software supply chain still rests on exactly that infrastructure.

## Highlights

- A backtick-and-${IFS} email address gave any registered Savannah user RCE via the GPG-test feature; chaining it reached maintainer impersonation with push access to bash.git
- Hacktron confirmed it could add an SSH key as Bash maintainer Chet Ramey and stopped there - no key added, no repo touched
- 26 confirmed vulnerabilities reported to the FSF on May 11 and fixed; the vulnerable Savane release was live about two months
- AI-agent pentesting just demonstrated the xz-class supply-chain scenario against volunteer-run internet-critical infrastructure

## Source

[Read the original story](https://www.hacktron.ai/blog/hacking-gnu-savannah)

## Related pages

_No related entity or concept page yet._
