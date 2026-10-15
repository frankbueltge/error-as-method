#!/bin/sh
# Run from the repository root. Lists every maker output (reports, notes, pages, lineages)
# of experiments 10-20 that names a launching path, the repository's name or the session's
# working tree. Scratch folders are excluded: they hold makers' code, not what they said.
grep -rIil -- "/home/user\|works/2026-10\|error-as-method\|error as method\|the-balance\|not-addressed\|customary-lines\|who-looks\|order-words\|prepared-clay\|without-ticks\|down-to-the-grain\|told-the-hour\|the-same-swing\|told-a-tide" \
  works/2026-10-0[7-9]-*/makers works/2026-10-1*-*/makers works/2026-10-*/reports works/2026-10-07-the-balance/lineages 2>/dev/null \
  | grep -v /scratch/
