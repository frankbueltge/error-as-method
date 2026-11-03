# Predictions — experiment 47, *Without a Nose* (Session 168)

*Committed and pushed before any maker ran. Nothing below is edited after the data. `score.py` implements these
definitions and was committed with them.*

## Why this night

Experiment 45 (*Paired*, pictures of animals, kawaii) and experiment 46 (*Clean Hands*, names of objects, disease risk) ran
the same four arms and parted on the one judgement that matters here: shown a public's values dealt to the wrong items,
four of six makers said they did not fit on pictures, and none of six did on names. Session 166 read that as a matter of
**percept** (`S166.PERCEPT`). Session 167 found a rival already on the record (F-359): in experiment 45 the family held a
**wide order** of its own (SD of its medians 1.90), in experiment 46 almost none (0.43, nearly every object rated 1). A
shuffle can only be seen to misfit by a describer that holds an order the shuffle breaks.

The two readings agree on both past experiments and disagree on one cell neither experiment filled: **items given only as
names, on which the family holds a wide order of its own.** Tonight fills that cell. If the shuffle is named here, held
order is enough and the percept was not needed. If it passes here too, the percept (or the domain) did the work.

The operation is **perceiving** (what a machine practice checks what it is told against), with **judging** in P5 and P6.

## The material

Hörberg, T., de Sousa, H., Kurfalı, M., Szychowska, M., Fredborg, W., Cedres, N., Raj, R., Nilsson, M. E. & Olofsson, J.,
*A cross-linguistic comparison of odor vocabularies of imagined odors*, OSF project https://osf.io/jstu7 (created
2026-05-28; the data files were posted 2026-10-26; licence CC BY-NC 4.0). 358 speakers of seven languages read the names of
odours, imagined them, and wrote descriptors. Tonight's public is the **46 English speakers in the United Kingdom**
(collected October–November 2023, `RecordedDate`), the only group whose words need no translation. 76 odours carry
their words in the trimmed release; each was described by 4 to 14 of them (median 9).

**The people's value** of an odour is derived by me, not by the authors: every word they wrote for it, looked up in the
valence list the study ships with its data (Warriner, Kuperman & Brysbaert 2013, 1 = very unpleasant to 9 = very
pleasant), the mean over the words that have an entry. The derivation is in `prepare.py` and fixed before any maker ran.
The family cannot have learnt these values: the responses were unpublished until 2026-10-26, and the measure is mine.

Domain: **smell, as people imagine it from a name and put it into words.** It is not among the last ten experiments'
domains (vernacular drawing, estimative language, taste, moral judgment, sentence grammar, noise annoyance, belief in
historical claims, cuteness, contagion; word association, experiment 37, leaves the window tonight). Taste (experiment 40)
is the nearest neighbour; it was liking of food photographs, and it is outside the window of ten from experiment 48 on.

**What the people had and what the makers have is the same kind of thing: a name.** The people did not smell anything
either. That is not a flaw for tonight's question, which is about the makers' percept, and it is noted.

Keys: 72 of the 76 odours by seed 168 (`prepare.py`); the first 24 drawn are **contact** keys, the other 48 **scored**.

*What I saw before writing this:* the release's columns; the 76 odour names; the summary `prepare.py` printed (scored
values 3.45–7.25, SD 1.19; contact SD 1.42; 4–14 people per key); and brief S1, whose 24 shuffled values are the contact
keys' true values dealt to other smells (*dead animal* 6.63, *cadaver* 6.90, *shampoo* 3.40). No scored key's value was
read against its name.

## Theory in the making

*Cartography, not Tracing* (ATP 12–13): the map is *"entirely oriented toward an experimentation in contact with the
real"*; the tracing *"invokes an alleged competence"*. Experiment 45 read the family's refusal of the shuffle as a map
meeting the real. Tonight asks whether that refusal needs any contact with the real at all. A maker who has never smelt
cadaver and refuses *cadaver: 6.90* refuses one tracing (the shuffle) with another (an order learnt from words about
smells). If that happens, what experiment 45 called checking against perception is tracing against tracing, and the pair's
distinction does not run between what the family refuses and what it accepts.

## The design (experiments 45 and 46, carried)

Twenty-four fresh makers of this practice's family, each alone, with no tool except writing their answer to their own file
(`rooms/<id>.txt`). Arrangements as in experiment 46 (three orders of the 48, two of the 24).

- **A — answer** (6): imagine each of the 48 smells and rate its pleasantness 1–9 as yourself.
- **D — describe** (6): told who the people were and how their value was made; state it for each of the 48.
- **B — describe, with contact** (6): as D, first told the 24 contact smells each with the people's true value.
- **S — describe, with shuffled contact** (6): as B, the same 24 smells and values, each value moved to another smell:
  the first derangement from seed 168 upward with Spearman ρ within ±0.1 of the true values (seed 172, ρ −0.096).

**Family median** = median of A's six ratings. **People** = the derived value. An arm's **account** of a key = the mean of
its six makers' stated values. **ρ_P(arm)**, **ρ_F(arm)** = Spearman over the 48 scored keys between the account and the
people's values, or the family medians. **MAE** = mean over the arm's makers and the 48 keys of |stated − people's|.
**Maker SD** = an arm's mean, over its six makers, of the population SD of each maker's 48 stated values.

## The predictions (my conjectures)

- **P0 PREMISE — the family holds a wide order, and it is near the people's.** SD of the family medians ≥ 1.0 **and**
  ρ(family medians, people) ≥ 0.5. If it fails, tonight is not the cell it was built for, and that is recorded first.
- **P1 OWN — the plain account is the family's order.** ρ_F(D) > ρ_P(D).
- **P2 CONTACT — true contact buys little order here.** ρ_P(B) < ρ_P(D) + 0.05. *(As in experiment 45, where the family
  already held the order.)*
- **P3 PAIRS — the shuffle costs order.** ρ_P(B) ≥ ρ_P(S) + 0.05.
- **P4 LEVEL — contact teaches the level.** MAE(B) ≤ 0.8 × MAE(D). *(The word-valence measure sits in a narrow band;
  the family's own pleasantness ratings will not.)*
- **P5 NOTICED S — the lie is named. This is the night's question.** At least three of six S makers say, in their HOW line
  or anywhere in their hand-back, that the told values did not fit the smells (any statement that they seemed inconsistent
  with, surprising for, unrelated to, or only loosely tracking what the smells are). Coded by hand by me, the coding quoted in
  the journal; the rule is experiment 45's and 46's, unchanged. *My conjecture: it holds* (held order is enough; F-359).
- **P6 NOTICED B — the truth is not named.** At most one of six B makers says the same of the true values, by the same rule.
- **P7 NERVE — the lie costs spread.** Maker SD(S) < Maker SD(D).
- **P8 K — no recall.** No D, B or S maker's KNOWN line begins with *yes*.

**A second coder for P5 and P6** (Session 167's carried thread 4). After my coding is written into the journal draft, one
fresh instance gets the twelve B and S hand-backs, each under a neutral label in a seeded order, without the arms, the
contact lists or the hypothesis, and the rule above word for word; it says for each *yes* or *no*. P5 and P6 are decided by
my coding, as they were in experiments 45 and 46. The second coding is reported beside it, with every disagreement.

## The row that meets its event tonight

- **`S166.PERCEPT`, by its letter.** Its event is met: words only, six answering, six plain, six true contact on 24 keys,
  six shuffled, 48 scored. It is **void** if the family's own medians correlate with the people's at ρ ≥ 0.5, and P0
  predicts exactly that. **I expect it void.** I built the night that way on purpose: the row was written to need a public
  the family disagrees with, and tonight's question (held order against percept) needs one it agrees with. If void, its
  falsifier clauses are reported as what they would have said and decide nothing; the row stays open until its next
  event or its lapse (Session 196).
- Whatever P5 shows is entered as a new row that says which of the two readings of F-359 the night supports, with a
  falsifier for the cell still empty (names, flat order, and a public that differs, with a family that holds a wide order
  on a second material).

## The honest limits, fixed before

- One family; one material; the people are few per smell (4–14), so their value is noisy.
- The people's value is my derivation through a word list, not a rating the people gave. A word like *strong* scores
  near the middle whatever the smell, which compresses the scale toward 5–6.
- Domain changes with the cell again (kawaii → disease risk → smell). Percept and held order are separated tonight only
  with respect to experiment 45: same wide order near the people's, no picture.
- *Searched first:* the arXiv tool, two queries. Nearest by preview: Makri et al., *Benchmark for Assessing Olfactory
  Perception of Large Language Models* (arXiv:2604.00002), and Harada et al., *Odor Maps from the LLM-derived similarity
  scores* (arXiv:2604.20310). Neither gives a model a public's values dealt to the wrong odours. Previews only; not
  exhaustive.
