# Auto-land: what did not land, 2026-10-10

## Refused

These branches were NOT landed. A refusal is not an error: protected paths
and escalated projects require a human-reviewed pull request (see
governance/STANDING-DELEGATION.md §4/§5). Ordinary research records belong
under the auto-land-eligible paths.

- `night/2026-08-13-session-53-request` — refused_protected_path: SITE-API.md 
- `night/2026-08-13-session-54` — refused_protected_path: SITE-API.md 
- `night/2026-08-16` — refused_protected_path: SITE-API.md 

## Failed — the machinery, not the gate

These branches were eligible and the gate did not object. They did not land
because the merge or the push broke, which turns this job red. Nothing about
them was judged; the record is still on the branch and still recoverable.

- `claude/upbeat-darwin-93jb29` — conflict: this branch does not merge into main; it will be retried on every run and keep failing until the overlap is resolved by hand

