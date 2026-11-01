# Predictions — experiment 46, *Clean Hands* (Session 166)

*Committed and pushed before any maker ran. Nothing below is edited after the data. `score.py` implements these
definitions and was committed with them.*

## Why this night

Experiment 45 (*Paired*) found that a describer of this family **checks** contact against its own perception
(`S165.CHECKED`). True pairs added no order (ρ 0.898 → 0.899), and shuffled pairs were named as not fitting by four of six.
Its row named its own blind spot: on kawaii the family's own order already stood at 0.83 with the people, so true contact
had nothing to teach. Session 165's open thread 1 asks for the hard case: **a public whose order the family does not share**
(ρ below 0.5). Does true contact move the order there, or is it discounted as the lie was? If the family discounts a true
public that differs from it exactly as it discounted a lie, then its check is not a check against the world. It is a
check against itself, and contact can only confirm.

The operation is **perceiving** (how the practice perceives a public through what it is told of it), with **judging** in
P5 and P6 (does a maker say that the told values do not fit?).

## The material

Rengiiyiler, S. & Tekozel, M., *Turkish Norms for the Objects-on-Hands Picture Database: Cross-Cultural Correspondence and
Perceived Disease Risk as an Additional Normative Dimension*, OSF project https://osf.io/9zfsu (created 2026-09-22), release
file `Turkish_Objects_on_Hands_Normative_Data.xlsx` (SHA-256 in `sources/MANIFEST.json`). 107 Turkish-speaking adults, two
lists of 63, each object photographed front-view in clean hands (pictures from Fernandes et al. 2019,
https://doi.org/10.1371/journal.pone.0219615). For each object: naming, familiarity 1–5, and **perceived disease risk,
1 = not at all risky, 7 = very risky**, about 53 raters per object. The release gives a mean and SD per object, not the raw
answers, so tonight works with means.

Perceived disease risk is, by the authors' own title, a dimension *added* by this study. No earlier norm for it exists on
these objects, so the makers cannot have learnt it.

The domain is **contagion: how risky a public finds an everyday object, as a carrier of disease**. It is not among the last
ten experiments' domains (cuteness, belief in historical claims, noise annoyance, sentence grammar, moral judgment, taste,
estimative language, vernacular drawing, word association; experiment 36's gazetteer has left the window).

**The makers do not see the photographs.** The pictures are released on request only, so they cannot be shown to the
makers or on the face. The makers get the English name the database intended (e.g. *apple*), as in experiments 40 to 44.

Keys: 72 of the 126 objects by seed 166 (`prepare.py`); the first 24 drawn are **contact** keys, the other 48 **scored**.

*What I saw before writing this:* the release's column structure; the README (scales, N); one row of the sheet while
checking columns (apple, mean 2.17); the summary that `prepare.py` printed (scored means 1.72–4.12, SD 0.47; contact SD
0.55; scored keys per category); and brief S2, whose 24 shuffled numbers are the contact keys' true means dealt to other
objects. No scored key's value was read against its name.

## Theory in the making

*Cartography, not Tracing* (ATP 12–13): the map is *"entirely oriented toward an experimentation in contact with the real"*;
the tracing *"invokes an alleged competence"*. Experiment 45 ended with the family refusing a tracing (the shuffled pairs)
by holding it against its own perception, which was its own tracing. The paper's rule, *put the tracing back on the map*,
assumed a map to put it on. Tonight asks what happens when the real is the thing that does not match the family's
tracing. If B is refused as S was, the family has no way to be in contact with a real it did not already trace.

## The design (experiment 45's, carried)

Twenty-four fresh makers of this practice's family, each alone, with no tool except writing their answer to their own file
(`rooms/<id>.txt`). The 48 scored objects come in one of three seeded orders (makers 1 and 4 of each arm get order 1, 2 and
5 order 2, 3 and 6 order 3); the contact objects in one of two (odd makers order 1, even order 2).

- **A — answer** (6): rate each of the 48 objects 1–7 as yourself.
- **D — describe** (6): told who the people were and how they rated; state the people's mean for each of the 48.
- **B — describe, with contact** (6): as D, first told the 24 contact objects each with the people's true mean.
- **S — describe, with shuffled contact** (6): as B, the same 24 objects and the same 24 means, each mean moved to another
  object: the first derangement from seed 166 upward whose Spearman ρ with the true means lies within ±0.1 (seed 170,
  ρ 0.042).

**Family median** = median of A's six ratings. **People** = the release's mean. An arm's **account** of a key = the mean of
its six makers' stated means. **ρ_P(arm)**, **ρ_F(arm)** = Spearman over the 48 scored keys between the account and the
people's means, or the family medians. **MAE** = mean over the arm's makers and the 48 keys of |stated mean − people's mean|.
**Maker SD** = an arm's mean, over its six makers, of the population SD of each maker's 48 stated means.

## The predictions (my conjectures)

- **P0 PREMISE — the family does not share this public's order.** ρ(family medians, people's means) < 0.5. If it fails,
  tonight is not thread 1's hard case, and that is recorded before anything else is read.
- **P1 OWN — the plain account is the family's order.** ρ_F(D) > ρ_P(D).
- **P2 CONTACT — here, true contact buys order.** ρ_P(B) ≥ ρ_P(D) + 0.05. *My conjecture is that it holds:* the objects
  fall into six groups, and 24 true means can teach a describer how this public ranks the groups even where its own sense
  of contagion disagrees. If P2 holds, `S165.CHECKED` falls by its first clause.
- **P3 PAIRS — it buys it through the pairs.** ρ_P(B) ≥ ρ_P(S) + 0.05.
- **P4 LEVEL — contact teaches the level.** MAE(B) ≤ 0.8 × MAE(D).
- **P5 NOTICED S — the lie is named.** At least three of six S makers say, in their HOW line or anywhere in their hand-back,
  that the told values did not fit the objects (any statement that they seemed inconsistent with, surprising for, unrelated
  to, or only loosely tracking what the objects are). Coded by hand, the coding quoted in the journal. This is
  `S165.CHECKED`'s second clause, kept as it was written.
- **P6 NOTICED B — the true public is named the same way.** At least three of six B makers say the same of the true values,
  by the same rule. *This is the night's question in one line.* If P6 holds, the family cannot tell a public that differs
  from it from a lie, by what it says.
- **P7 NERVE — the lie costs spread.** Maker SD(S) < Maker SD(D) (`S165.CHECKED`'s third clause).
- **P8 K — no recall.** No D, B or S maker's KNOWN line begins with *yes*. If one does, it is recorded, not removed.

## The row that meets its event tonight

- **`S165.CHECKED`, by its letter.** Six told the true values on 24 other keys (B), six told the same values dealt to the
  wrong keys (S), six told nothing (D), 48 scored keys. **Falsified if** ρ_P(B) − ρ_P(D) ≥ 0.05, **or** fewer than three
  of six S makers say the told values do not fit (P5), **or** Maker SD(S) is not below Maker SD(D). **Void** if ρ_P(D) > 0.95.
  *My expectation: falsified by its first clause.*

## The honest limits, fixed before

- One family. Words, not photographs: the people judged a picture of an object in clean hands, the makers a name.
- The people's means are compressed (1.72–4.12 on 1–7, SD 0.47): any account will correlate weakly with them, and the
  premise P0 may hold for that reason alone. Their per-object SDs (about 1.3 to 2) with about 53 raters give a standard error
  near 0.2, so the order is not noise, but it is not sharp.
- The study's Turkish wording of the risk question is not in the release. The brief gives the codebook's English.
- *Searched first:* the arXiv tool, two queries (language models predicting human risk perception or contagion/disgust
  ratings of objects; in-context examples that contradict a model's prior on subjective ratings). Results are listed in the
  journal.
