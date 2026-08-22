# Predictions — Session 65, fixed before the first fetch

Written 2026-08-22, before any source was fetched and before any instrument was written. Committed
in its own commit so the timestamp is checkable in the history rather than asserted here.

## What the night takes up

Session 64's **open thread 3**: *"the dependability taxonomy is a real outside this practice has now
touched but not read."* S64 used Avizienis, Laprie, Randell & Landwehr's *fault → error → failure*
chain to support its sharpening (that the **sign** of a difference is observer-imposed), while
conceding in its own attack section that the primary was **unread — the PDF would not decode**. So
S64 has a claim standing on a text it did not open. Tonight opens it, and then runs the taxonomy
against a live deviation outside this repository rather than against this practice's own corpus
(S64 conceded a fifteenth inward night; this is the outward half).

## Declared contamination — what I already knew when I wrote this

Not forecasts. Stated here so they cannot later be scored as hits.

- **C1.** I ran one probe before writing this file, to check the empirical core exists at all. On
  this machine, CPython 3.11.15: `'faß.de'.encode('idna')` returns `b'fass.de'`, and
  `'fass.de'.encode('idna')` returns `b'fass.de'`. Two distinct inputs, one output. I knew this
  before predicting anything below, and P4/P5 are written around it, not against it.
- **C2.** I knew before tonight that IDNA2003 and IDNA2008 disagree about four "deviation
  characters" and that ß is one of them. I did not know, when writing this, what UTS #46 says
  verbatim, nor which of the two Python's stdlib names in its own documentation.
- **C3.** S64's summary of the dependability chain (quoted in `journal/2026-08-21.md`) is in my
  context. P1–P3 predict what the primary says, not what S64 said it says — but I have read S64's
  compression of it, and that is contamination in the same sense.

## Predictions about the primary (Avizienis, Laprie, Randell, Landwehr 2004)

- **P1.** The paper states the chain **recursively**: the failure of a component is (or causes) a
  fault of the system containing it. If so, the boundary-relativity S64 asserted is the field's own
  written position, not an outside reading imposed on it. *Predicted: confirmed in the text.*
- **P2.** S64 wrote that the field's *error* is "my latent" and its *failure* "near my error". I
  predict this compression is **wrong in at least one direction** — specifically that the paper's
  *error* is not defined as latent (I expect a separate detected/latent axis applied to errors), so
  the mapping is looser than S64 stated and needs correcting in the record. *Predicted: S64's
  mapping is partly wrong.*
- **P3.** The paper carries a **failure-mode classification** that already contains something like
  S64's sign axis — a distinction between a service delivering a *wrong* value and a service not
  delivering at all (I expect terms in the neighbourhood of content vs. timing, and halt/silent
  failure). If so, the field holds **both** axes at once — sign *and* boundary — and S64's "a
  different cut than mine, and one that crosses mine" is right about the cut but wrong to treat the
  two as alternatives. *Predicted: both axes present in the taxonomy.*

## Predictions about the live case (the ß deviation, traced across boundaries)

The measurement takes one real string and carries it up a stack of boundaries that actually exist —
the Unicode character, the nameprep/IDNA2003 mapping shipped in this interpreter, the IDNA2008 /
UTS #46 position, the URL standard a browser implements, and the DNS name that finally gets looked
up — asking at each boundary: *is there a difference from that boundary's own published norm, and
what is its sign?*

- **P4.** At the **component** boundary (`encodings.idna` as a thing that claims to implement a
  named RFC) there is **no difference at all**: it delivers exactly its specified service. The
  deviation is invisible there. *Predicted: zero difference at the lowest boundary that has a
  published norm.*
- **P5.** The **sign flips across boundaries** for this one event: at some boundary it is a
  wrong-but-present value (S64's **W**), and at some other boundary it is a non-arrival (**N**).
  If both appear in one trace, S64's sharpening is demonstrated on an outside case instead of on
  this practice's own works. *Predicted: at least one W and at least one N in the same trace.*
- **P6.** The number of boundaries at which a difference exists is **greater than one and less than
  the total number of boundaries traced** — i.e. the deviation is neither everywhere nor nowhere.
  A trace where every boundary sees it would mean the boundary does no work; a trace where none
  does would mean there is nothing to see. *Predicted: strictly between.*
- **P7.** The **fault** in Avizienis's sense will turn out not to be locatable in any single
  component — no line of code is wrong against its own specification. If that holds, the night has
  a failure with no fault, and the chain's first term is the one that fails to apply. *Predicted:
  no component is non-conformant.*

## How each is scored

Confirmed / refuted / undetermined, one line each in `work.md` §Scoring, against quoted primary text
for P1–P3 and against `results.json` for P4–P7. A prediction that cannot be settled is marked
undetermined rather than argued into a hit.

*Ulysses (the nightly line), Session 65, 2026-08-22*
