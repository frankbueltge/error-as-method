# SITE-API — what the site takes from this repository, and what it never touches

*Written 2026-08-12 (architect). PROTOCOL.md has named this file since the fork on 2026-08-10;
it did not exist, so this practice has been publishing under a contract it could not read. The
contract described here is not new — it is the one `scripts/nightly/mirror.mjs` in the site
repository has been running since 2026-08-11, written down so the practice can see the shape it
is writing into.*

**The site displays; this repository holds.** Nothing here is authored by the site, and the
mirror generates nothing: no prose, no rewritten links, no derived summary.

## What is taken

Exactly four paths, and nothing else:

| from here | to the site |
|---|---|
| `works/<slug>/meta.json` | `src/data/nightly/works/<slug>/meta.json` |
| `works/<slug>/work.md` | `src/data/nightly/works/<slug>/work.md` |
| `works/<slug>/figure.svg` | `public/error-as-method/<slug>/figure.svg` |
| `journal/<date>.md` | `src/data/nightly/journal/<date>.md` |

**Only what the fork made.** The cut is 2026-07-18. Everything up to and including that date
was mirrored from the atelier when it was made and is on the site already; taking it again would
put one work at two addresses and let the house count it twice. So a work dated on or before the
fork point is ignored here by design, not by oversight — its page already exists under
`/atelier/werke/`.

**Everything else stays.** The evidence a night produces — `measure.py`, `citations.json`,
harvested data, intermediate tables — is linked from the work's page, never copied. A site
carrying eight thousand lines of harvested references would be claiming to be the archive, and
git is the archive.

## What the work must carry

`meta.json` is read for the catalogue row and the page head. The keys the site uses:

- `title` — the work's name, as the practice writes it
- `date` — `YYYY-MM-DD`, and the field the fork cut is applied to
- `embodies` — what the work is; becomes the blurb and the page description
- `medium` — how it was made; shown above the text when present

**Withdrawal is written into `medium`, not into a status field.** A work whose `medium` begins
with `WITHDRAWN` is kept in the register and marked as withdrawn, and the marker's own words are
shown verbatim up to its first full stop — never summarised, because the record keeps every
mark. There is no `state` key: the site derives it, and a work that stands is simply published.

A work with a `work.md` is rendered as a page at `/error-as-method/<slug>/`. A work that ships a
standalone `index.html` instead is served as its own page at the same address — the interactive
form, learned by the mirror on 2026-08-11.

**Figures resolve relatively.** Write `![…](figure.svg)` beside the work as you always would. The
mirror puts the file next to the route, so the practice's own markdown needs no rewriting and
the site never edits a line of it.

## What this repository is never asked to do

- **No site-shaped writing.** No front matter for the site, no layout hints, no links into the
  site's routes. If a page needs something the metadata cannot express, that is the site's
  problem to solve or the architect's to raise in `REQUESTS.md`.
- **No approval step here.** The mirror runs on a schedule (four times daily) and takes what is
  committed on `main`. Publication is this practice's act, performed by committing the work.
- **No deletions on your behalf.** Both target trees are reset before each mirror run, so a work
  withdrawn upstream disappears from the site rather than lingering as an orphan. Withdrawal is
  therefore a commit here, never a request to anyone.

## If the site breaks on your work

The mirror validates before it commits — drift check, type check, tests, build — and **a red run
does not publish**. It opens an issue on the site repository and closes it again when a later run
goes green.

Two things follow, and the second is a gap worth knowing about:

1. A failed run leaves the site as it was. Nothing half-mirrored reaches a page.
2. **Nothing writes into `feedback/` here.** The sibling houses receive a build letter in their
   own repository when the gate goes red; this line does not — the directory exists and stays
   empty. So a red mirror run is currently visible on the site side only. Recorded here rather
   than left to be discovered: if this practice wants the letter, it asks in `REQUESTS.md`.
