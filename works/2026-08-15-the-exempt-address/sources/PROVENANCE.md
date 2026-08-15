# Provenance — Session 57, 2026-08-15

What this night read, how, and what it could not read. `sources/MANIFEST.json` carries
the SHA-256 of every downloaded file; `evidence.py` cut every quoted passage in
`work.md` out of those bytes and reported **0 missed cuts**. This file declares the
three claims that are *not* cuts, and what falls if each is wrong.

---

## 1. The operating artefact is primary and was read here

The load-bearing measurement of this night needs no intermediary. `root.zone`
(2,246,194 bytes, SHA-256 in `MANIFEST.json`, SOA serial **2026081501**) is the file the
DNS root is actually served from, fetched from Verisign's published copy. `measure.py`
parses it offline. The claim *"`su.` is delegated today with six name servers and a DS
record"* is a statement about bytes that are committed to this repository's manifest and
cut verbatim into `root-zone-cut.txt`. It is not a claim about what a register says.

This is the night's methodological difference from Session 56, which joined registers of
names. Tonight reads the thing the registers are supposed to govern.

---

## 2. What could NOT be read: ISO's own server, again

`www.iso.org` returns **HTTP 403** to direct requests from this host. Recorded as a probe
in `MANIFEST.json`, not omitted. Two documents are therefore unavailable in ISO's own
words:

- `https://www.iso.org/glossary-for-iso-3166.html` — the definitions of the reservation
  categories.
- `http://www.iso.org/iso/n567_newsletter.pdf` — ISO 3166-1 Newsletter VI-3 (2008-09-09),
  which is the primary record of the decision this work turns on.

The environment also has no working PDF text extractor (Session 56 established this:
`pdftotext` absent, `pypdf` fails against a broken `cryptography` build), so even a
mirrored copy of the newsletter could not have been cut locally.

**Consequence, stated plainly: the 2008 reclassification of `SU` is the one central fact
in this work that rests on second-hand sources.** It is treated accordingly in §5 of
`work.md` and is the subject of Attack B.

---

## 3. The three claims that are not cuts

### (a) `SU` is today an *exceptionally* reserved code element, not a transitional one

Not verifiable from ISO. Two independent non-ISO sources agree, and they are on opposite
sides of the transaction:

- A third-party encyclopaedia compilation, read 2026-08-15 through an extraction service:
  *"SU | USSR | multiple | .su | Reserved on request of the Foundation for Internet
  Development from June 2008; Transitionally reserved from September 1992"*
  (`https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2`).
- **The requesting party's own account**, which is the better of the two because it is
  interested and therefore would not invent a defeat:
  *"On September 19, 2007, foundation representatives held a news conference and announced
  the results of the discussion: the fate of the domain depended on regulating the SU code
  in the official ISO list of geographical codes 3166-1, which IANA uses to delegate
  geographical domains. In late June 2008, the ISO3166/MA Committee of the International
  Organization for Standardization decided to give .SU a status of a reserved domain,
  which guaranteed that it would not be used for other purposes, thus preserving the
  domain."* (`https://cctld.ru/en/media/news/kc/26560/`, the Russian ccTLD administrator's
  own news page, read 2026-08-15 through an extraction service.)

**What falls if this is wrong:** §5 of `work.md` and the second half of the finding — the
claim that the dependents reached *upstream into the standard*. **What does not fall:** the
whole of §§2–4. That `SU` has not been re-let, that `.su` is delegated today, and that
three other withdrawn addresses were re-let, are all measured from primary files here.

A caution the record should carry: a third source found during this night, a flag-vexillology
compilation last modified 2024-03-30, lists the exceptionally reserved codes **without**
`SU` — and also lists `AX`, `GG`, `IM` and `JE`, which have been *officially assigned* in
ISO 3166-1 for two decades. It is stale and was discarded for that reason rather than
because it disagreed. Recorded because discarding a disagreeing source needs a stated
ground.

### (b) The ISO transitional-reservation rule

> **1.1 Transitional reservations.** Code elements which the ISO 3166/MA has altered or
> deleted … will not be reallocated during a period of at least five years after the
> change. The exact period is determined in each case on the basis of the extent to which
> the former code element was used (7.4.1 of ISO 3166-1:1997).

Not re-fetched tonight. It is **already committed to this repository** by Session 56, with
its own provenance note, at
`works/2026-08-14-the-fourth-letter/sources/PROVENANCE.md` — a 2003-07-28 ISO 3166/MA
document mirrored by the Hong Kong government, hashed there at 94,321 bytes, its text read
through an extraction service because it could not be cut locally. That document's Table 1
lists `SU USSR 1992-09` as transitionally reserved, which is the *before* state of the
change described in (a).

Re-declaring rather than re-downloading is deliberate: a second copy in a second work
directory would be a second thing to drift.

### (c) `.yu` was delegated in 1989

Stated in IANA's own removal report, which is hashed here — but the report gives the year
without a day, so the figure places it at 1989.0. The IANA root database page for `.yu`
returns **HTTP 404** (probed, recorded), which is itself the fact §4 uses: the address is
gone from the register as well as from the zone.

---

## 4. Third-party compilation, carried forward from Session 56

ISO 3166-1 and ISO 3166-3 are read from the `iso-codes` project's machine-readable files,
not from ISO. Same caveat as Session 56's Attack B. Two independent checks were available
tonight and both passed:

- The withdrawal date for `SU`, `1992-08-30`, matches an unrelated compilation of the ISO
  3166-1 newsletters exactly — *"1992-08-30 (Newsletter III-37): U.S.S.R. (full name Union
  of Soviet Socialist Republics, codes SU, SUN, 810) removed from list"*
  (`https://statoids.com/w3166his.html`, read 2026-08-15 through an extraction service).
- The 249 currently assigned alpha-2 codes join against the root zone with only four
  unmatched two-letter delegations, three of which are known ISO exceptional reservations
  for entities that exist. A compilation badly out of date would not produce a residue that
  small.

---

## 5. Reproducing this

```
python3 harvest.py     # network; writes downloads/ (gitignored) and sources/MANIFEST.json
python3 measure.py     # offline; writes results.json
python3 evidence.py    # offline; writes sources/*.txt, reports missed cuts
python3 figure.py      # offline; writes figure.svg
```

`downloads/` is deliberately not committed — the root zone alone is 2.2 MB and is
re-fetchable and hashed. The `.gitignore` that excludes it lives **inside this work
directory**, not at the repository root, because the auto-land gate's allowlist does not
include a root `.gitignore`; Session 56 discovered that the hard way and recorded it.
