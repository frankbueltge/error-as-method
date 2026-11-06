# CLAUDE.md — error-as-method

The practice's constitution is `PROTOCOL.md`; the nightly session's instruction lives in its scheduled task. This file
holds only one thing every session needs and neither of those says.

## Unattended runs: command shapes that stop for approval

The nightly session runs with nobody watching. A few command shapes always ask for a person's approval, whatever the
permission rules say, and an unattended night then waits until morning with nothing pushed. Avoid them:

- **Never put `cd` and a git command in one Bash call** (`cd /home/user/error-as-method && git commit …`). The shell
  already starts in this repository, so run git directly. If you have to change directory, run `cd` as its own call and
  git in the next one.
- **Never pipe a download into an interpreter** (`curl … | python3`, `… | sh`). Save it with `curl -o file`, then read
  the file in a separate step.
- **One purpose per Bash call.** Write files with the Write tool, then commit and push in a separate call, rather than
  a long heredoc chained with `git add && git commit && git push`.
