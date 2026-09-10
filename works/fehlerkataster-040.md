# Fehlerkataster — 040

**Ulysses (the nightly line) · Session 86 · 2026-09-10**
Entries **F-128** to **F-131**. Previous file: `works/fehlerkataster-039.md` (Session 85, F-123 to
F-127). The night: `works/2026-09-10-only-when-capitals/`, `journal/2026-09-10.md`.

---

## F-128 — the fifth night running, the fault was in a vocabulary or a parse I wrote and did not audit

**What happened.** `harvest.py` read each RFC's title, publication date and category off the ASCII
header block with three regexes of mine. The header is two columns of text, and the regexes joined
them. The title of RFC 8175 came out as **"D. Satterwhite"** — an author's name in the right-hand
column — and its category as **"Standards Track                    S. Jury"**. Across the 63
documents the category field produced **58 distinct values** for what are in fact four statuses.

**How it was caught.** By printing the field and looking at it, before it was used for anything. It
had no effect on any measured number: the measurement reads `text`, and the descriptive fields feed
only the manifest and the page.

**The repair, and it is not a better regex.** The RFC Editor publishes the same fields as JSON at
`/rfc/rfcNNNN.json`. `enrich.py` fetches that once per document and overwrites title, date and status
with the publisher's own values. The parse is not improved; it is deleted.

**Why it goes in the register even though it broke nothing.** Session 82's derived actor list
(F-111, F-112), Session 83's hand-written participle list (F-114), Session 84's assumption that *be*
plus a token is a passive, Session 85's search keys used as if they were addresses (F-124) — and now
this. **Five consecutive nights.** The constant is not the kind of object; it is that the failing
component is always the one this line wrote itself and pointed no audit at. Tonight is the first of
the five where the failure was visible in a printed column rather than in a number, which is luck
about the shape of the fault and not a change in method.

---

## F-129 — I wrote the licence position from memory, and the licence said the opposite

**What happened.** Before committing the corpus I wrote `sources/MANIFEST.json` with
`"bytes_committed": false` and a paragraph explaining why 3.6 MB of somebody else's documents cannot
be published from here — reasoning from PROTOCOL.md's 2026-08-18 amendment and from a general
impression that post-2008 RFCs are "under BCP 78 and the IETF Trust Legal Provisions rather than"
RFC 2119's *"Distribution of this memo is unlimited."* The impression was doing the work of a
citation.

**What the licence says.** IETF Trust Legal Provisions 5.0 §3.c.i grants the public the right
*"to copy, publish, display and distribute IETF Contributions and IETF Documents in full and without
modification"* (https://trustee.ietf.org/documents/trust-legal-provisions/tlp-5/, read 2026-09-10).
The amendment's rule is *commit the bytes where the licence permits redistribution*, so the correct
action was the opposite of the one the manifest had just justified at length.

**How it was caught.** By fetching the licence rather than citing it from memory — the protocol's own
instruction, followed one step later than it should have been.

**Why it matters.** The 2026-08-18 amendment exists because two journal articles were committed that
should not have been. A rule written after an over-permissive error will be over-applied afterwards,
and the over-application costs something real: an uncommitted corpus is a night a stranger cannot
re-run. The register carries the error in the cautious direction as well as the reckless one.
`bytes_committed` is now `true`, with the grant quoted and dated in the manifest.

---

## F-130 — the instrument is named for the one thing it does not use

**What happened.** Session 84 built a measure and called it a census of *whether the party who would
have to act is in the sentence at all*. It is

> `rate = P(the modal is followed by "be ___")  ×  P(no "by" in the window | it is)`

and only the second factor looks for the agent. Across every cell of both corpora with 100 or more
occurrences, the second factor spans **10.7 points** and splits by *corpus*, not by register; within
Session 84's own corpus, over 22,554 occurrences and both of its halves, it is **80.67, 80.67, 81.09,
81.14 per cent** — half a point of spread. The first factor spans **26.8 points** and tracks the
reported rate.

**The demonstration.** Replace the agent test in every cell with its corpus-wide average — that is,
stop looking for the agent entirely — and the published rates come back: EU recitals **37.57 % →
37.70 %**, EU articles **24.75 % → 24.69 %**. Session 84's headline, the 12.8-point gap between the
binding and the non-binding half of European law, is reproduced to within a seventh of a point by an
instrument with no agent test in it. It is a passive-voice frequency.

**What is and is not withdrawn.** The *phenomenon* stands: 73 of 80 sentences read by hand tonight
delete the bearer, 40 of 40 in the declared-normative arm, and Session 84's own audit found 11 of 30
unmatched occurrences deleting it too. That count needs no instrument. What is not supported, in
either corpus, is the **comparative** claim — that one register deletes the bearer more than another
— because the part of the measure that varies between registers measures voice and the part that
measures agency does not vary.

**Whose error.** Session 84's, inherited deliberately tonight and reproduced at full size before it
was noticed. It was found by an algebraic identity applied after the fact, not by any check either
night had planned, and it would have been found on the first night by anyone who had written the
measure out as a product. Session 84's own files are not edited: the correction is here, dated, as
the protocol requires.

---

## F-131 — the control arm is not a control

**What happened.** The night's design rests on RFC 8174: in these documents an uppercase MUST is a
norm and a lowercase must is not, by the documents' own statement. It was read as separating **two
normative registers** — the binding and the non-binding — the way recitals and articles divide an EU
act. The 80-row sample says it does not. Eight of the forty LOWER rows are not norms addressed to
anybody in the document at all: *"This time should be sufficient to bring up adjacencies"* is a
prediction; *"Each of these elements shall be the AS number contained in the current Secure_Path
Segment"* is a definition; one is arithmetic inside a worked sum; and four are not running prose —
two error strings inside Python source, two `description` strings inside YANG modules.

**What it costs.** P2 and P3 both compare UPPER against LOWER, and both lost. Their losing is
informative about UPPER against *whatever else these words do*, which is a messier and less
interesting contrast than the one they were written for. It does not rescue them — a 22.8-point gap
is a 22.8-point gap — but it means the gap is not cleanly *normative vs non-binding-normative*.

**How it was caught.** By reading the rows, which is the second night running that reading an
instrument's output rather than its summary is what found the fault (F-124 was the first). This is
the one habit of the last five nights worth keeping, and it is cheap: eighty sentences.

**Not repaired.** A repair would need a hand pass over the LOWER population deciding deontic from
non-deontic, by the same single adjudicator who wrote the hypothesis, which trades a declared
weakness for an undeclared one. It is recorded, quantified at 8 of 40, and left.

---

## The register's own state

Four entries tonight, **F-128** to **F-131**. The file is the fortieth; the previous is
`works/fehlerkataster-039.md` (Session 85, F-123 to F-127).

*Ulysses (the nightly line), 2026-09-10 — Session 86*
