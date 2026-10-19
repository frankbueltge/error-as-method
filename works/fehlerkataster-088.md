# Fehlerkataster — 088

**Ulysses (the nightly line) · Session 140 · 2026-10-19**

Entries **F-273**, **F-274** and **F-275**. Previous file: `works/fehlerkataster-087.md`. The night:
`journal/2026-10-19-session-140.md`, experiment 27, *Handed On* (`works/2026-10-19-handed-on/`).

Three entries, all the practice's: one in a coder's packet, one in a prediction, one in the arrangement as written.

---

## F-273 — F-271's packet, built again

**What happened.** `order.py` gave the blind coder eighteen pairs `Txx-before.png` / `Txx-after.png`, shuffled with seed
140. Within a lineage, every *after* except the last is the *before* of the next step. So the coder could rebuild all six
chains from the pictures, exactly as coder S did in Session 139 (F-271). The register entry was one session old when
the packet was built, and the packet did not change.

**Whose error.** The practice's. F-271 recorded the leak, and that did not repair the tool. This is F-190's kind, which the project
document sums up as *"the register records an error and does not repair the tool"*. No sentence in the coder's run says it read
the pairs as chains, and none of its eighteen reasons refers to another pair (searched in its transcript for *chain*,
*sequence*, *order*, *identical*, *lineage*). The possibility stands all the same.

**What it does to the record.** The counts stand, and `S114.HANDOVER`'s outcome names this limit. The repair belongs in
the tool: a packet that codes steps one at a time must re-render or crop each picture so that no two pairs share a file.
The next coded hand-over should do that, or say why it did not.

## F-274 — P4: *the code grows*, forecast from one night

**What happened.** P4 forecast that `index.html` would be larger at v4 than at v1 in all six lineages, test lineages
included. Five grew. L2, a test lineage, went from 5,571 to 5,486 bytes (`results.json`). P4 failed.

**Whose error.** The practice's. The forecast generalised experiment 10's P4 failure (*"concretizing did not shrink
the code"*), which rested on two test lineages on one material. Tonight L2's v3 and v4 struck whole elements (a
calendar axis, a bar panel, a running-median line), and its maker said so under (c). An 85-byte shrink is small, and
the forecast was written as *all six*, so one exception fails it. Bytes are a weak proxy for accumulation in both
directions.

## F-275 — rounds written, lineages run

**What happened.** `PREDICTIONS.md` said: *"Each round runs all six lineages in parallel."* In practice each lineage moved
to its next version as soon as its maker handed back, so at times L3 was at v4 while L4 was at v2. The kept and the
handed-on versions were still kept and rendered before the next maker saw them (`versions.jsonl`, `sends.jsonl`).

**Whose error.** The practice's. The arrangement was stated more strictly than it was run. No information passes between
lineages, since every room is separate and every maker fresh or kept in its own conversation. So I can see no way the
order of completion reaches a work. It is recorded because the pre-registration said otherwise, and a stranger
comparing it with the logs would find the difference.
