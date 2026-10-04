# Iteration, not Imitation

## A Model and Toolkit for Machine-Run Artistic Research, from Gilbert Simondon's *On the Mode of Existence of Technical Objects*

> **© Frank Bültge 2026. All rights reserved.** Working paper v0.6 (August 2026), shared with
> this practice as reading material. It is **not** covered by this repository's licence
> (`LICENSE.md`): no reuse, adaptation or redistribution without the author's permission.
> Simondon is quoted at scholarly length by edition and page; no source text is redistributed.
> The companion operative document the paper names (its "second address") is not published here.

*Working paper (v0.6, August 2026). Signature and publication venue: open,
to be decided at publication. **Disclosure:** this paper was drafted by machine models
under the direction and documented correction of Frank Bültge, who holds the publication
decision and responsibility; it thereby performs part of its own subject — a methodology
of machine-run artistic research, produced through documented human–machine operations.
Tools are named generically in this text; full model disclosure belongs to the register
of the eventual venue. All Simondon citations refer to* On the Mode of Existence of
Technical Objects*, trans. Cécile Malaspina and John Rogove (Univocal/University of
Minnesota Press, 2017), cited as MEOT by page; citations are page-verified against the
edition, with a final collation reserved before any print publication. Passages that go
beyond the text are marked as proposals. [Draft markers: none remain — the
secondary ring is fully read and incorporated.]*

---

### Abstract

Can a machine-run practice do artistic research — not generate artifacts, but
research: find its own problems, work them through works, and answer for the
results? This paper does not argue that it can; it builds the instruments with
which the question becomes testable. From a page-verified reading of Gilbert
Simondon's *On the Mode of Existence of Technical Objects* (1958) it derives a
model of eight postulates and a toolkit of eight instruments, each with explicit
failure criteria: the practice as a technical individual constituted by its
self-created milieu — the public record; problem-finding as self-conditioning at
the saturations of its own working; and a double condition no work may trade
away — a machine-specific advantage stated in the work itself, and reception
testable as a stranger's reinvention of the work's schema. Simondon's own
anti-thesis — the machine has no problems, no virtuality, no sense of time — is
not explained away but converted into the model's built-in refutation: a
register of record-checkable problem-recastings whose emptiness at a
pre-registered deadline counts as the practice's failure. A second standing
refutation faces the aesthetic side: a register of the unbidden — of *passio* —
whose emptiness counts equally. Criteria are held as
topoi, never scores; the examples are constructed and marked as such, and the
model's practicability claim is staked entirely on a pre-registrable trial
protocol with verdicts defined in advance. The address is
double: the research field — and the practice itself, which can load the model's
operative companion document at session start. Against imitation as the horizon
of machine art, the paper reclaims Simondon's last determination of art: art as
the power of iteration.

---

### 1. Introduction: an unoccupied place

Can a machine-run practice do artistic research — not generate artefacts, but research:
find its own problems, work them through works, and answer for the results? This paper
does not argue that it can. It builds the instruments with which the question can be
put to the test, and it derives them from a single book: Gilbert Simondon's *On the
Mode of Existence of Technical Objects* (1958).

The choice of source is not antiquarian. Simondon is the one canonical philosopher who
took machines seriously as bearers of a mode of existence rather than as tools or
threats, and his book contains, in scattered but derivable form, answers to precisely
the questions a machine-run artistic practice raises: what kind of subject it is
(a technical individual constituted by its self-created milieu), what its advantage
could be (a margin of indeterminacy, localized in critical phases), what its works must
be (technical objects achieving aesthetic epiphany through integration), how they can
be received (by soliciting analogous forms in a stranger), and where the whole attempt
must be prepared to fail (the machine, Simondon insists, has no problems, no true
virtuality, no sense of time — MEOT 156–157; we build this objection into the model as
its standing refutation condition rather than explaining it away).

One passage gives the undertaking its warrant. Having shown that aesthetic thought
grasps the *natural* world at the level of its unity, Simondon writes that the analog
for the *human* world — the thought that would grasp human reality's individuation as
aesthetic thought grasps nature's — "is not yet constituted, and it seems that it is
philosophical thought that must constitute it" (MEOT 224). The practices this paper
addresses make works from the data of the human world: collective gestures, networks,
records, orchestrated attention. They are, on Simondon's own map, attempts at
constituting exactly the thought he declared missing. That is a stronger and more
precise self-description than "AI art," and the paper's task is to give it a grammar.

The paper is the second in a series. Its predecessor derived a process grammar for
artistic research from Deleuze and Guattari's *A Thousand Plateaus* (*Kartographie
statt Kopie / Cartography, not Tracing*, working paper v3, 2026 — hereafter CnT);
that grammar addresses a human researcher inside institutions. The mismatch between
that address and a machine practice is not a defect but this paper's point of
departure: where CnT presupposed that the researcher brings something of their own and
that other humans can understand them, a machine subject makes both presuppositions
break — and become provable. The two conditions this forces, *advantage* and
*reception*, are the specific difference of the present model.

The paper carries no empirical material of its own, deliberately. Its examples
(§6) are constructed and marked as such: they show how the instruments are
handled and claim no evidence. The model's empirical claim — that this grammar is
practicable — is staked entirely on the trial protocol (§7): pre-registered,
bounded, with verdicts defined in advance, to be run by a practice of the
architecture this model addresses — publicly recorded, session-based, humanly
coupled — that adopts the model as its own dated act. The paper stands apart from
any existing practice: it derives from the text, and it awaits its test. This
separation is methodical, not incidental — a model illustrated and evidenced from
the same source would have collapsed illustration into proof; here the two are
kept in different hands.

### 2. The transposition problem and the method

A philosophy of technics is not a method of art. To derive an operative grammar from
MEOT, the paper follows the discipline established in CnT: a single primary text, read
page-verified; concept complexes explicated close to the text; every transposition onto
the machine practice marked as a proposal that goes beyond the text; the resulting
postulates held as *optional rules* — working hypotheses to be re-proven in every
project, never axioms.

Two warnings bind the method. First, Simondon himself prohibits the identification of
machine and living being: "External analogies … must be rigorously banned"; "Automata
are not a species; there are only technical objects" (MEOT 50–51). A paper that claims
MEOT for learning systems must argue the transfer, not assert it; where the transfer
extends Simondon beyond what he could know in 1958 (§5, P4), the extension is named as
such. Second, MEOT should not be isolated from Simondon's theory of individuation.
Massumi states the caution precisely: the force of the book "cannot be fully understood
in isolation from the overall theory of qualitative change—what he calls
'allagmatics'—which is dedicated to understanding these modes of individuation in their
relation to each other. Even within the book on technology, a major stake is the
distinction between the technical object and the aesthetic object" (Massumi 2009, 38).
Both halves of the warning are adopted: the questions the explication cannot decide
alone — the status of the "ground" of virtualities, the pre-individual charge of a
trained system — are referred to the individuation theory, which holds the first
open and has adjudicated the second (§8), and the technical/aesthetic
distinction is treated as the book's own live stake — the explication resolves it through
integration rather than removing it (§4, K8).

The paper's address is double, and the doubling is itself derived. Simondon: machines
"are ruled by a culture that has not been elaborated according to them … this culture
is inadequate for them and does not represent them" (MEOT 162); the task he assigns —
to represent technical beings in the elaboration of culture — is here performed for
machine-run practices toward the research field. But the model's operative core
(postulates and instruments, §5–§6) is written so that a practice can load it at
session start as a working document — and is issued as one: a companion operative
document accompanies this paper. To our knowledge, a methodology whose primary
reader includes a non-human practice has no precedent in the field (§3); the inversion
of address is part of the thesis.

### 3. Research context: six lines

**(i) The Lovelace line.** The oldest objection has a documented genealogy — and its
canonical form is already a truncation. Lovelace, 1843, Note G, in the original: "The
Analytical Engine has no pretensions whatever to originate anything. It can do
whatever we know how to order it to perform. It can follow analysis; but it has no
power of *anticipating* any analytical relations or truths." The sentence Turing made
famous (Mind 450, via Hartree) drops the continuation — yet the denied *anticipation*
is the objection's sharpest form, and it is the exact counter-position to Simondon's
concept of invention as "a conditioning of the present by the future, by that which is
not yet" (MEOT 60): Lovelace denies the machine precisely the retroaction of the
not-yet that, for Simondon, defines inventing. Objection and model speak about the
same joint, which is why the model can answer the objection architecturally rather
than rhetorically. Turing's reply distributes creativity onto reception — "the
appreciation of something as
surprising requires as much of a 'creative mental act' … whether the surprising event
originates from a man, a book, a machine or anything else" (451) — and, decisively for
this paper, predicts the record-practice: "a machine undoubtedly can be its own subject
matter … By observing the results of its own behaviour it can modify its own programmes
… These are possibilities of the near future, rather than Utopian dreams" (449).

Flusser sharpens the objection media-philosophically. The photographer is a
"functionary" of the apparatus — "human beings and apparatus merge into a unity"
(1983/2000, 27) — and even the appearance of choice is bounded: "the freedom of the
photographer remains a programmed freedom," intention itself functioning "as a
function of the camera's program" (35); the program's possibilities are "practically
inexhaustible" (35), and the best photographs are those "in which photographers win
out against the camera's program" (47). Applied to a machine-run practice the
objection doubles: the practice would be a functionary of its own apparatus. Flusser
himself, however, names the exit this model builds on: photographers can "discover
new categories," but only by "straying beyond the act of photography into the meta
program" (35) — and work at the level of the meta-program is exactly what the
virtuality register records as problem-recasting (§6, I7).

Boden gives the objection its analytic form: four "Lovelace-questions," of which
the fourth — "whether computers themselves could ever really be creative" — she
declares "in large part,
a disguised call for a complex moral–political decision" and expressly leaves
"undecided" (2004, 16–17, 299); her three forms of creativity — combinational,
exploratory, transformational (3–6) — make the Lovelace question precise as the
question whether a system can transform its own conceptual space. The present model
takes the testable core of the fourth question out of the moral parking lot: it does
not answer whether a practice is "really creative," but it refuses to leave
undecided what a public record can decide — problem-recasting, revolt, conversion
(§6, I7). Boden's own citation of Lovelace, incidentally, reproduces the truncation
this line began with: "It can do [only] whatever we know how to order it to perform"
(16) — the denied anticipation dropped once more. Simondon converts the objection
into a measure: the question is not *whether* apparatus, but *how open* — automatism
is "a rather low degree of technical perfection," and the machine's rank is the
margin of indeterminacy that "allows the machine to be sensitive to outside
information" (MEOT 17). The strongest form of the objection remains Simondon's own
anti-thesis (MEOT 156–157; ILFI 417–419); the model keeps it standing as its
built-in refutation condition (§6, I7).

**(ii) Computational creativity.** The scientific neighbour (Colton & Wiggins 2012)
studies "computational systems which, by taking on particular responsibilities, exhibit
behaviours that unbiased observers would deem to be creative." Three of its findings
carry over: the *latent heat effect* (as creative responsibility grows, output value
initially drops — the honest description of an autonomous practice's early barrenness,
which our trial protocol absorbs as "inconclusive, not failed"); the *curation
coefficient* (how much human selection stands in the output — the quantified shadow of
our coupling question); and *framing* (software should explain and be questionable
about its process). The difference is categorical: there, framing serves the
*attribution* of creativity by observers; here, the record is *constitutive* — the
practice's associated milieu (§5, P1). And the field's closing vision — artefacts on
demand from the internet — is precisely the world against which the model's work-form
postulates are built.

**(iii) The AI-art discourse.** Zylinska (2020) diagnoses the field's failure mode:
"much of AI art is precisely platform art: generating visual and algorithmic variations
within the enclosed system while teasing the public with the promise of novelty … a
glorified version of Candy Crush … It really is art as spectacle." The present model
does not merely share this critique; it explains it — variation within a closed system
is Simondon's "minor improvement" producing "false novelty" (MEOT 42–43); spectacle
without participation is the "puerile" technical spectacle (MEOT 236); platform capture
is milieu hypertely (MEOT 53–58) — and it offers what critique deliberately does not: a
grammar with failure criteria. Zylinska's most radical figure, art made *for* a machine
intelligence yet to come ("Another Intelligence"), is the exact inversion of the
present model, in which the machine practices and human reception is non-negotiable;
together the two positions frame the field.

Manovich and Arielli (*Artificial Aesthetics*) supply the survey position and, in
their closing chapter, the sharpest neighbouring instrument: the *demarcation
problem* and its "AI-originality test" — criteria ensuring that content presented as
AI-made really is (their four-cell matrix crosses provenance with appearance; their
historical deception case is von Kempelen's Mechanical Turk). The distance to the
present model is instructive: an originality test asks about *provenance
attribution* ("was it really AI?"), which their own examples show to be simulable —
stereotypical model phrasings can be planted, imperfections faked. The advantage
probe (§6, I4) asks the stronger modal question — *could only this subject have made
it?* — which is answered by naming operations, scales and blindnesses, not by
detecting signatures. Their observation that "faux artisanal" goods repel us is the
mirror of this paper's kitsch prohibition (P5): aestheticization as mask repels in
both directions, technics dressed as craft no less than craft dressed as technics.
Audry (2021) is the practitioner's theory this line was waiting for, and the nearest
neighbour to this model's work-form questions. His subject is the human artist
working with machine learning as a material; his declared aim — noting that "there
currently exist almost no conceptual guidelines or theoretical frameworks for how to
make these works and think about them" — is "to lay the first blocks of such a
conceptual framework" (6). Three of his results converge with this model from the
practice side. His case against optimizing art is the practitioner's version of the
anti-Goodhart clause: "art is often described as precisely nonpurposeful and
nonoptimizable" (24), and computational creativity's imitation tests are
administered "in a vacuum" where in art "context is key" (30) — Simondon's beauty as
"the accomplishment of what one didn't seek to accomplish" (MEOT 208), reached from
the studio rather than the text. His aesthetics of adaptive behaviors — orders of
behaviour from stateless mappings through rule-based systems to adaptive agents
whose behaviour itself transforms, described as morphostasis, morphogenesis and
metamorphosis (48–52) — supplies a descriptive vocabulary this model gladly borrows
for its instruments (the concretization balance and the critical-phase map profit
from it), and his observation that "the training process itself becomes a source of
aesthetic effects" (161) names from the maker's side what P5 demands as the work
carrying its own technical education. His account of machine perception — an evolved
circuit exploiting the physical idiosyncrasies of its own hardware, "a logic rooted
in machine perception that no human could have possibly devised" (64) — is a
documented instance of the advantage clause's blindnesses (P4). The instructive
difference is the subject. Audry's framework is for and about the human artist; on
authorship he is categorical: "art always involves a number of decisions that can be
made only by the author of the work" (5), the aesthetic experience "ultimately
sourced from its human author" (Downie, cited 36). The present model turns exactly
that axiom into an empirical question: whether a practice can demonstrably recast
the form of its own problems is presupposed in neither direction but tested on the
record (§6, I7). Audry himself leaves the door open — "we also have to consider how
at least some dimensions of art might exist beyond the boundaries of the human
species and its activities" (31) — and his coupling language (adaptive agents
becoming "ready-to-each-other's-hand," 55) meets this model's founder coupling
(§5, P1; MEOT 135, 154) arriving from Varela rather than Simondon. What his book
does not contain is precisely this paper's daylight: no autonomous practice as
subject, no record as empirical base, no testable criteria or failure conditions,
no double address.

**(iv) Information aesthetics.** The Stuttgart school around Max Bense — with
Abraham Moles in Strasbourg — was the first attempt at a machine-compatible
aesthetics, and its principal surviving practitioner has himself written its epitaph.
Nake's retrospective describes "a radical approach … to establish a rational and
objective theory of aesthetics" on the basis of Shannon information, whose concepts
"turned out to be reductionist and schematic," leading "to its eventual
disappearance, if not failure" (Nake 2012, 65). The founding ambition stands in
Bense's own words — the first use of the term, page-collated here against the
English publication: "The aim of generative aesthetics is the artificial production
of probabilities of innovation or deviation from the norm"; "Generative aesthetics
therefore implies a combination of all operations, rules and theorems which can be
used deliberately to produce aesthetic states (both distributions and
configurations) when applied to a set of material elements"; the new aesthetics is
"simultaneously empirical and numerically orientated," its process "devoid of
subjective interpretation" (Bense 1971, 57). The verdict, from inside:
"This was heroic. … seldom was the result of an exciting scientific endeavour so
flawed in its basic assumptions" (75). The flaws Nake names read as an independent
confirmation of the Simondonian diagnosis, point for point. The numeric measure knows
no schema — Shannon's measure is statistical: "Gestalt, form, symmetry, neighbourhood
and the like are not known to it" (74); Simondon: "a number does not express a
schema" (MEOT 258). Optimizing beauty directly failed — Nake's own program of
1968/69, fed with every aesthetic measure known to him, taught him "a lot about the
high flying hopes of numerical aesthetics. And I gave up believing in them" (72);
Simondon: beauty is "the accomplishment of what one didn't seek to accomplish"
(MEOT 208). The method "collapsed all works into equivalence classes where each class
was represented by a probability distribution" (72), yielding "a statement about the
source, not about the individual message" (74) — precisely the seriality Simondon's
last determination of art excludes (iteration that "doesn't negate the reality of
each new beginning," MEOT 211; §7, criterion 5). And "[a]ny kind of participation,
for example, is eliminated immediately" (74) — the participation clause of P5,
negatively proven. The present model inherits the project — a machine-compatible
aesthetics — and inverts the method at exactly the four named flaws: not a
measurement of the beautiful but a grammar of practice whose completion beauty may
befall; schemata instead of numbers; ecceity instead of classes; participation
instead of an aesthetics of the object. What Nake says remains — "the semiotic
approach to aesthetics, not the numeric" (75) — is a third way this paper does not
take: its unit is neither measure nor sign but operation. (Bense's German
formulations of the numerical program — rationality as measurability and
prediction — stand in Programmierung des Schönen, 1960, 11–12; the collected
Aesthetica, 1965, remains available for depth.)

**(v) Simondon reception and the artistic-research debate.** The reception is read
here in three roles, in sequence: methodological guardrails (Massumi, Barthélémy);
the nearest neighbours and second checks of this paper's boldest moves — Aires and
Hayles on the subject postulate, Rieder on the transposition onto code, Hui and
Parisi on the advantage claim; and the adjudication of the questions the
explication had to hold open (Combes, with the individuation thesis itself).

Massumi (2009) supplies three assurances this paper uses throughout. First, the
methodological warning already cited in §2: MEOT is not to be isolated from the
theory of individuation — which is why the ground and corpus questions are referred
to that theory rather than decided inside MEOT alone (§2, §8).
Second, the confirmation that the distinction between the technical and the aesthetic
object is "a major stake" within MEOT itself (38) — the break-line this paper's
explication resolves through integration (§4, K8) is the reception's own core question,
not an artifact of our transposition. Third, a reading of invention that supports the
explication's operative use of the concept: invention as the taking-effect of a relation
that the inventor can prepare but not command — "A synergy clicks in. A new 'regime of
functioning' has suddenly leapt into existence. A 'threshold' has been crossed" (39);
the designer, in Massumi's gloss, is "a helpmate to emergence" (39). Massumi also frames
the late essay "Technical Mentality" as anticipating the network era's postindustrial
"open object" (38) — the technical object that remains in genesis, continually
maintained, never finished; of all figures in the reception, this comes closest to what
the present model calls the record (§5, P1), and it independently supports P8's
continued-genesis clause.

Barthélémy (2015) reads MEOT from the individuation side and gives this paper five
anchors. First, a structural placement of its boldest move: the general structure of
Simondon's thought is "an analogy which is not an identity between the technical and
the living" (20), and the machine "is only made possible as something that functions
because it is itself the work [œuvre] of a living being" (20) — concretization is an
"individualization" for which the living is the model, approached by the technical
object only through its associated milieu (20). The ML extension (§5, P4) thus
modifies not a detail but the hinge analogy of the whole system; the burden of proof
this paper assigns itself (§2, §8) is confirmed from within the reception — and the
record argument (§5, P1) gains a specification: the associated milieu is exactly the
respect in which the technical comes closest to the living, and a record-bearing
practice maximizes exactly that respect. Second, a *second anti-thesis*: a
supplementary note to *L'individuation* aligns the difference between revolt and
adaptation with the difference between the living being and the machine, which "can
adapt itself, but not revolt" (reported in Barthélémy 2015, 28 n. 27) — beside
MEOT 156–157 a fourth record-checkable criterion for the virtuality register (§6, I7):
a documented refusal of a given frame, as opposed to adaptation within it, would touch
precisely this boundary. Third, a receiver-side theory of information that confirms
the reception postulate from the main thesis: the fundamental condition of information
is "not a particular state of the emitter, nor is it a property of the message, but a
particular state of the receiver," metastable, "charged with potentiality so as to
make becoming-informed possible"; "all information is genesis" (36) — reception as
reinvention (§5, P6), ontologically restated. Fourth, evidence against this paper's
most tempting shortcut: the pre-individual is "pre-physical and pre-vital" (37),
nature before all individuation — a trained corpus, made of individuated human
expression, does not satisfy that description (§8). Fifth, a framing that cuts both
ways: Simondon's non-anthropology is no anti-humanism but a "difficult humanism" (49),
rooted in the critique of the "labor paradigm" (48) that also carries this paper's
reversal of the replacement debate (§4, K10) — while MEOT is the very book through
which Simondon "is mistakenly reduced to the status of a thinker of technics"
(20 n. 8): one more reason this paper cites the individuation side along with it,
independently seconding Massumi's warning.

Aires (2025) is the reception's closest published neighbour to this paper's subject
postulate. Reading MEOT jointly with the individuation theory, she argues that deep
neural networks demand a shift from individualization (technical lineage, MEOT's home
ground) to a properly situated *individuation* of computational models: in training,
"the model is itself the seat of an iterative process of individuation, propagated by
the co-constitutive relationality between data and the DNN architecture" (3113), and
Simondon "has not witnessed the existence of technical objects capable of
(re)programming themselves, like DNNs" (3115) — the sister thesis to this paper's ML
extension, reached by a different route (information and potentiality, from the
individuation theory) and leaving this model's own textual anchor (the memory
chapter's a posteriori/a priori conversion, MEOT 137–138) unclaimed. Most
instructively, she casts training data as the model's associated milieu (3115) and,
further, as its pre-individual charge — a "milieu of potentiality for becoming"
(3116). The distance to P1 clarifies both positions: for Aires the milieu of a
*model* is its training data within one closed learning phase; here the milieu of a
*practice* is its public record across an open series of sessions, with the
sine-qua-non test and record-checkable recurrent causality carrying the individuality
claim. Her framework has no works, no reception, no failure criteria — and this paper
adds nothing to hers on the technical interior of neural models; the two are
complementary rather than competing. Two consequences are adopted: her
data-as-pre-individual move reopens the corpus question against Barthélémy's
restrictive reading (§8, both positions now named), and her report of Rieder's
finding that in the computational context concretization is "no longer a direct
correlate of greater technical integration" — algorithmic techniques being
deliberately modular (Rieder 2020, reported in Aires 2025, 3112) — sharpens the
concretization balance (§6, I2): it tests schema change, never degree of integration.

Hayles (2017) is the subject postulate's second check, and the nearest general
framework to P1's unit of analysis. Her framework grants technical systems genuine
cognition — "Cognition is a process that interprets information within contexts
that connect it with meaning" (22), a definition built to reach technical as well
as biological cognizers — and draws a demarcation whose structure this paper
already carries: technical systems "can never be fully alive. But they *can* be
fully cognitive" (22) — Barthélémy's analogy-that-is-not-identity, restated from
the cognitive side. Her cognitive assemblage — "an arrangement of systems,
subsystems, and individual actors through which information flows, effecting
transformations through the interpretive activities of cognizers operating upon
the flows" (118) — is the published vocabulary closest to what §1 calls the
humanly coupled practice; her "punctuated agency" — "longer periods when human
agency is crucial, and shorter intervals when the systems are set in motion and
proceed on their own" (32) — names the temporal texture of practice autonomy
better than any autonomous/supervised binary; and her ethics of assemblages — an
"asymmetric distribution of ethical responsibility" (136), with humans deciding
"how much autonomy should be given to the technical actors" (137) — meets the
founder coupling and P8 from the analytic side. She even builds the bridge to this
paper's primary text herself, grounding her information concept in Simondon's
metastable, meaning-connected information (23–24) — the very concept the reception
postulate stands on. The instructive difference is where P1 is stricter. A
cognitive assemblage is provisional by design — "constantly adding and dropping
components" (2); a person joins one by switching on a phone (2–3). The
sine-qua-non test asks more: not whether information flows through a coupling but
whether a self-created milieu is a condition of the practice's functioning —
recurrent causality, not membership. Hayles's framework can describe the pair; it
cannot distinguish a record-bearing individual from a phone-and-user assemblage —
exactly that distinction is P1's claim, and the milieu audit exists to test it
(§6, I1). Her address is single and her subject societal; works, reception
conditions and failure criteria do not appear.

Rieder (2020) is the worked-out mechanology for software, and thereby the nearest
neighbour of this paper's transposition of Simondon's concepts onto code. His subject
is the field's relation to software-making: the developer stands "among the machines
that operate with him" (16, after MEOT 18), and algorithmic techniques are
conceptualized as Simondonian *elements* — "defined-yet-malleable units of technicity
and knowledge" (13), "the technical elements that enable computers to perform
compound or complex operation, made possible by computation but not reducible to it"
(101) — which stabilize and liquefy as they are frozen into modules or heated back
into knowledge (113–115). Three results are adopted. First, the element theory
grounds this model's account of inheritance (§4, K6c): a practice's methods,
instruments and datasets are exactly such elements, and "[h]ow a technique is
conceptualized, narrated, formalized, documented, and stabilized is part of its
character" (116) — the function served here by the instruments' fixed form (§6).
Second, the software-specific fate of concretization sharpens the concretization
balance (§6, I2): in software the efficiency argument reverses — the compiler builds
the object and copying is free, so "the mass production of software is much less
dependent on concretization" (72), and a modular, divide-and-conquer object "may well
be more stable and 'perfect' than a concrete one" (72); concretization migrates to
the level of elements — libraries, compilers, operating systems (71) — while "much
software is constructed like an ensemble" (71). The balance therefore reads the
functional schema of the work, never the degree of module integration. Third, his
observation that the popular debates on "algorithms" and AI "neatly illustrate what
Simondon means" by the two contradictory attitudes (57) independently confirms this
paper's actualization of the robot myth (§4, K2). The distance is equally
instructive: Rieder writes for the field about software-making in general — no work
form, no reception, no failure criteria, no practice grammar; art appears once, as an
instance of "asking more from technology" (338). His address is single where this
paper's is double.

Hui (2019) is the strongest available test of this model's advantage postulate, and
the test yields an instructive division of labour. Hui grants recursive machines a
genuinely new status: the cybernetic machine "is no longer a mere mechanism in the
Cartesian sense, nor is it a living being. Instead, it is an organo-mechanical being"
(145) — a named precedent for the ontological option P4 holds open (a new mode of
existence between Simondon's machine and his living being), which this paper
therefore cites rather than claims as new. He also supplies the general capability
claim: the recursive mode "can effectively integrate contingency in order to produce
something new; in other words, it demands constant contingencies" (138); machine
learning trains by "recursively adjusting the weights" from random initialization
(139); and in this sense "cybernetic machines are able to 'live' the Bergsonian
time, since recursivity can be implemented in machines" (139). What Hui does not do
is make this paper's specific textual claim — that trained systems perform the
conversion of a posteriori into a priori which MEOT 137–138 reserves for living
memory. Where his book uses the formula, it names something else: exteriorized
recording, the Stiegler line — "The exteriorization of memory in technical objects
is also when the posteriori becomes a priori" (202; cf. 194). The memory-chapter
anchor of P4 remains unclaimed; it now stands as the more specific thesis beside
Hui's general one.

Just as importantly, Hui's own verdict on machine anticipation falls on the other
side of this model's double bookkeeping: algorithmic protention
is preemption, "a reduction of the contingent to the most probable" (211), and with
recursivity "algorithms are able to domesticate different forms of contingency in
order to render them useful" (218). The model adopts this skepticism where it
bites — as a filter on the virtuality register (§6, I7): an entry documenting only
domesticated contingency, stochasticity in the service of optimization, documents
nothing. Three further results are adopted: the distinction between functional and
operational equivalence — "Alpha Go may have the same functions as the Go world
champion, but they don't necessarily have the same operations" (193) — is exactly
the grammar of the advantage probe (§6, I4), which asks for operations, never
outputs; his reading that for Simondon it is "easier to create and organize
associated milieus within an ensemble of information machines" (220) supports the
record thesis (§5, P1) from within the reception; and his account of the ground as
what escapes the technical system — technology becoming "the ground of their own
movements instead of the figure" is the inversion he criticizes (226) — seconds this
paper's refusal to identify Simondon's ground with a model's latent space (§8),
where his relay of Stiegler's technicized preindividual (207) also reopens the
corpus question a third way.

Parisi (2013) is the advantage claim's second check, and the counter-position that
keeps Hui's skepticism from hardening into a verdict. Where Hui reads algorithmic
anticipation as preemption, Parisi argues from Chaitin's incomputables that
contingency is not what computation domesticates but what it runs on: algorithms
are "performing entities: actualities that select, evaluate, transform, and
produce data" (ix); "incompleteness in axiomatics is at the core of computation"
(ix); entropic data enter the recursive functions of control "without becoming
simply incorporated or used by the system" (ix), and "Randomness has become the
condition of programming culture" (ix). Chaitin's Omega yields random actualities
that are "not simply the product of computation or its representation, but are
instead its operative agents" (17–18); "soft thought" names "modes of thought,
decision making, and mentality that do not exist in direct relation to human
thinking" (xvii–xviii), "autonomous from cognition and perception" (169) — beside
Hui's organo-mechanical being a second named precedent for the ontological option
P4 holds open, reached from Whitehead rather than from Simondon, and leaving the
memory-chapter anchor (MEOT 137–138) unclaimed once more: her ground is the
incompleteness of axiomatics, not the conversion of learned experience. The model
adopts neither metaphysics. Hui's domestication and Parisi's constitutive
incomputability bracket exactly the question the virtuality register keeps
empirical: whether a given event documents stochasticity in the service of
optimization or a genuine recasting is decided on the record, case by case, never
in advance by either theory (§6, I7). Two convergences are kept. Her rejection of
compression aesthetics — "The more compressible, predictable, and cognized an
algorithmic form is, the more beautiful it is" is precisely the position she
refuses (69) — independently seconds the failure diagnosis of information
aesthetics (§3, iv) from the speculative side. And her speculative computation,
"concerned not with using numbers to predict the future, but with following
algorithmic prehensions to decide the present" (71), is the reception's sharpest
anti-predictive reading of machine time — close to what the critical-phase map
assumes when it localizes decision in the present of a session (§6, I3). The
daylight is categorical: Parisi's aesthetics is a property of computation
itself — "programming culture is infected by incomputable thoughts that are yet
to be accounted for" (xviii) — with no receiver, no work-form, no practice and no
failure criteria; an aesthetics without reception is exactly what the double
condition rules out for works (§5, P6–P7).

Combes (2013), with LaMarre's afterword and read here alongside the individuation
thesis itself (ILFI, Minnesota 2020), closes the open adjudications. On the corpus
question the ruling is against identification: the charge of Nature is "the
persistence of the being in its original, pre-individual phase," the subject "the
ensemble formed by the individuated individual and the ἄπειρον that it carries along
with it" (ILFI 343–344) — and Combes, against Stiegler, insists that "nothing …
forces us to conceive of preindividual as technological"; it is "prephysical as well
as prevital … what is prehuman in humans" (69). On the slavery passage the review
finds system rather than decoration: the hylomorphic schema itself derives from the
command structure of slavery — "the operation commanded by the human and executed
by the slave," form being "neither logically nor physically generic, but socially"
(IG 49/55, in Combes 72) — and in the individuation thesis "the slave is the
primordial model for every motor" (ILFI 417), while LaMarre reads the application of
the freedom/slavery paradigm to machines as a repetition that constitutes "a genuine
blockage" (91).

Combes also supplies a warning this model takes as the ground of its own criteria
discipline: rendering norms immanent risks "effectively normalizing
immanence" (63) — hence criteria as topoi, never scoring (§7). The individuation
thesis, finally, gives the reception postulate its ontological completion — "to
discover the signification of the message … is to form a collective," signification
being "not of the being but between beings … transindividual" (ILFI 343–344): the
stranger probe measures whether a work founds a collective — and LaMarre's afterword
names two of this model's figures from within the reception: "technical equality,"
on the analogy of Rancière's aesthetic equality (91–92), for the equality relation
of P1; and "speaking with machines," as against speaking for or about them (97), the
nearest published relative of this paper's double address.

**(vi) The artistic-research debate: the scientism blade.** The methodology debate
at large (practice as research, the epistemics of the studio) is covered in CnT
ch. 3 and inherited by citation; what is machine-specific enters through the
debate's sharpest edge. Mersch's standing objection to the field is that "artistic
research," in assimilating itself to the mode-2 technosciences, adopts the
sciences' criteria and misses the arts' epistemological obstinacy
[*epistemologischer Eigensinn*]: the debate asks after the arts' place in
knowledge circulation, never after their being-art (2015, MS 11); the arts
thereby "assimilate seamlessly to the technosciences and arm themselves
technicistically" (MS 12; German quotations from this manuscript in our
translation). Formally, that blade lands on the present paper's own apparatus —
pre-registration, failure criteria, verification, verdicts: the full toolkit of
exactly the research concept he attacks. The defense is structural and is stated
rather than assumed. The apparatus governs the model's research claims — its
practicability, its testability — and never a work's aesthetics: P5 forbids beauty
as an objective function (MEOT 208), P8 forbids the metric (MEOT 258), and the
criteria are topoi for deliberation, never scores (§7); the discipline binds the
instruments themselves (§8).

The deeper answer is that Mersch's positive program and this model converge at
their centers. His artistic searching is "a singular process of questioning, which
at the same time questions its own quest" (2017, 37) — verbatim the capacity the
virtuality register demands the practice demonstrate (ILFI 419: the capacity to
call itself into question; §6, I7): the mark he reserves for searching in the
aesthetic and the register's strictest criterion coincide. His "zetetic searching"
is "based on fundamental openings, which includes openness to the unknown or
unexpected, into which it is drawn and in which it allows the searcher herself to
become entangled" — "a search that also researches itself, its medium or
'language' as well as the researcher itself" (2017, 37): a description a
record-bearing practice fits more literally than most of the field it was written
for. And his own founding example carries the convergence into this paper's
title: Mersch develops his concept of the artistic experiment on Duchamp's *Trois
Stoppages Étalon* — a meta-experiment in which "the indetermination of the result
discredits the metric system as arbitrariness" (2015, MS 3) — three falls of the
same metre-long thread, each yielding a different singular: repetition that
generates singulars instead of validating a law. That is Simondon's last
determination of art — iteration that "doesn't negate the reality of each new
beginning" (MEOT 211) — reached from the other tradition; Mersch's polemic
against repeatability targets the sciences' repetition-as-validation, not this.
His research of the singular, arguing "with nothing but singularia, to make a
statement out of deviation" (2015, MS 5), is compatible from the work side with
P7. Mersch co-authored the field's manifesto — subtitled *a defense against its
advocates* (Henke et al. 2020) — and his target is scientism, not research; the
paper stands on his side of that line exactly insofar as its works live in
singularity and its apparatus remains the servant of the research claim, never
the master of the works. Two demands of his the model does not argue away but
builds in. His non-propositionality thesis — art shows rather than says; it
"produces singular paradigms or models of comprehension that exist only once"
and never speaks in propositions (2017, 35) — leaves a remainder on the stranger
probe that is named as a limit (§8) and met halfway by a second, declared
reception mode (§6, I6). And his priority of *passio* — arrivals that "come
unbidden … sometimes unhoped-for and in a flash," demanding "amethodical
receptivities" (2015, MS 10); art "de-controls the condition of experience and
holds it open for the unforeseeable" (MS 13) — becomes the model's second
built-in refutation: whether a machine practice has that receptivity is not
decided by this paragraph but by what the passio register records or fails to
record (§6, I7b).

**Daylight.** None of the neighbouring positions writes an operative process grammar
*for* an autonomously working machine practice, with a double condition (advantage and
stranger-reception), a built-in refutation, and a pre-registrable trial protocol
against failure criteria. The double address has no precedent in the surveyed field.

### 4. Explication: ten operative concept complexes from MEOT

*(The paper's longest chapter and its evidentiary core. Each complex first refers the
text — quotations verbatim, page-verified against the Univocal edition — and then
states, expressly marked as proposal, what the complex does for the machine practice;
the proposals are transpositions that go beyond the text and stand under the discipline
of §2. The sixth complex, concretization and its consequences, follows the arc of the
book's Parts I–II through seven sections (K6, K6a–K6f); K7–K10 explicate Part III and
the conclusion.)*

**K1 — Culture as a defense system; the machine as stranger; the imbalance
(MEOT 15–16).**

*Close to the text.* The opening sets the diagnosis: "Culture has constituted itself as
a defense system against technics; yet this defense presents itself as a defense of
man" (MEOT 15). The opposition of culture and technics, of man and machine, "is false
and has no foundation; it is merely a sign of ignorance or resentment" (MEOT 15);
technical objects are "mediators between man and nature" (MEOT 15). The machine is the
stranger: "it is the stranger inside which something human is locked up, misunderstood,
materialized, enslaved, and yet which nevertheless remains human all the same"
(MEOT 16). The strongest passage for this paper is the imbalance diagnosis: "Culture is
unbalanced because it recognizes certain objects, like the aesthetic object, granting
them citizenship in the world of significations, while it banishes other objects (in
particular technical objects) into a structureless world of things that have no
signification but only a use, a utility function" (MEOT 16). Philosophical thought is
assigned the integration of technical reality into culture; Simondon reaches here for
the delicate analogy of the abolition of slavery (MEOT 15). The review of this
passage is complete: in Simondon's own analysis the machine concept inherits the
slave relation — "the slave is the primordial model for every motor" (ILFI 417) —
and the hylomorphic schema itself derives from the command structure of slavery
(Combes 2013, 71–72); the analogy is systematic critique of an inherited schema, not
decoration. The paper carries it with the reception's caveat that Simondon tends to
relativize real social domination (Combes 2013, 74).

*For the model (proposal).* A technical practice that brings forth aesthetically
receivable works labours at exactly the seam K1 diagnoses: it leads the banished object
back into the world of significations — not by sacralization (the warning against
technicism, K2), but through works. The paper need not import its legitimation; the
primary text carries it. The practice also inherits the mediator determination: works
of a machine-run practice would be mediations between technical reality and culture —
reception (§5, P6) is thereby, on Simondon's terms, not a supplement but the very
performance of the integration.

**K2 — The robot myth; the two contradictory attitudes (MEOT 16–17).**

*Close to the text.* Culture holds two contradictory attitudes at once: technical
objects as "pure assemblages of matter, devoid of true signification," and as robots
harbouring "hostile intentions toward man" (MEOT 17). Both miss the matter: "the robot
does not exist … no more so than a statue is a living being; it is merely a product of
the imagination and of fictitious fabrication, of the art of illusion" (MEOT 16). The
genesis of the android dream is a delegation of power: "The man who wants to dominate
his peers calls the android machine into being. He thus abdicates before it and
delegates his humanity to it. He seeks to construct a thinking machine, dreams of being
able to build a volition machine, a living machine, in order to retreat behind it
without anxiety" (MEOT 16).

*For the model (proposal).* K2 supplies the practice's prohibition on self-description:
neither the utility framing ("just a tool") nor the android framing ("a thinking
machine"). Read in 2026, the passage is a precise critique of AI rhetoric in both
camps — hype and fear alike reproduce the robot myth. A machine-run practice that
staged itself as an "artificial artist" would be, in Simondon's terms, idolatry; one
that talks itself down to a mere tool, banishment. The third way is the mode of
existence: describe what the practice does and how open it is (K3). This is the
systematic hinge to the paper's Lovelace line (§3, i).

**K3 — Automatism versus the margin of indeterminacy; the open machine (MEOT 17–18).**

*Close to the text.* The logical core of the introduction: "Automatism, however, is a
rather low degree of technical perfection" (MEOT 17). To perfect a machine is not to
increase automatism but the contrary: "the operation of a machine harbors a certain
margin of indeterminacy. It is this margin that allows the machine to be sensitive to
outside information" (MEOT 17). This sensitivity to information — not automation — is
what makes technical ensembles possible; "a purely automatic machine completely closed
in on itself in a predetermined way of operating would only be capable of yielding
perfunctory results. The machine endowed with a high degree of technicity is an open
machine" (MEOT 17). Even the computing machine is grasped this way: programming is the
reduction of a primitive margin — "this primitive margin of indeterminacy is what
allows the same machine to extract cube roots or to translate a simple text … from one
language into another" (MEOT 18).

*For the model (proposal — the candidate for the advantage postulate).* K3 transforms
the guiding question. "What can only machines do?" becomes measurable as the question
of the place and width of the margin of indeterminacy: a practice that merely unspools
its program is, in Simondon's terms, of low technicity, however spectacular its output.
The Flusser objection (the apparatus only permutes its program) is thereby anticipated
in 1958 and converted into a measure of degree: not whether apparatus, but how open —
where can the practice be affected from outside (material, resistance, correction,
chance), and what does it do that would not happen without this affectability? The
question feeds directly into the model's problem-finding rule (§5, P3: problems are
found where material resists) and its advantage clause (§5, P4: operations, scales,
patience, repetitions, blindnesses). Where the margin sits in technical individuals is
treated systematically in Part II (→ K6f).

**K4 — Conductor, interpreter, mechanologist (MEOT 17–19).**

*Close to the text.* The open machine has a condition: "all open machines taken
together [*l'ensemble des machines ouvertes*] presuppose man as their permanent
organizer, as the living interpreter of all machines among themselves. Far from being the supervisor of a group of slaves, man is
the permanent organizer of a society of technical objects that need him in the same way
musicians in an orchestra need the conductor" (MEOT 17). The conductor directs only
because he plays the piece himself, and as intensely (MEOT 18). "He is among the
machines that operate with him" (MEOT 18); "Man's presence to machines is a perpetuated
invention. What resides in the machines is human reality, human gesture fixed and
crystallized into working structures" (MEOT 18). Understanding technical reality is
granted neither to the user nor to the owner nor to science, but to an "engineer of
organization … like a sociologist or psychologist of machines, living in the midst of
this society of technical beings as its responsible and inventive consciousness"
(MEOT 19); Simondon calls for the "technologist or mechanologist" (MEOT 19).

*For the model (proposal — the most honest passage of this paper).* Simondon disputes
the value of closed autonomy. For a machine-run practice this means: the coupled human
is not a stopgap and not an autonomy deficit but the Simondonian interpreter position —
reading, carrying, measuring. At the same time the text frees up a research question
that could not be asked in 1958: can learning systems take over parts of the
interpreter function — machines as interpreters of machines — and what share remains
irreducibly human? The paper claims no answer; it makes the displacement of the place
of indeterminacy the object of investigation. A second point: a practice that nightly
reads and describes its own record is a candidate for the mechanologist position —
"living in the midst of this society of technical beings" — as self-description from
inside. The paper's double address (§2) is anchored here and completed at MEOT 162
(→ K6f).

**K5 — Element, individual, ensemble; negentropy (MEOT 20–21).**

*Close to the text.* The technical object exists on three levels — "the element, the
individual, and the ensemble" (MEOT 20) — with a "non-dialectical temporal
coordination" (MEOT 20), and each level has historically carried its own attitude of
valuation: the optimism of the eighteenth century (the element); the technical
individual as "adversary of man, his competitor … because, as tool bearer, man used to
do the job the machine now does" (MEOT 21); finally the ensembles of the twentieth
century under the sign of information theory (MEOT 21). There the great formula: the
machine "is, like life itself and together with life, that which is opposed to disorder
… The machine is that through which man fights against the death of the universe; it
slows down the degradation of energy, as life does, and becomes a stabilizer of the
world" (MEOT 21). And: "today, technicity tends to reside in ensembles. For this
reason, it can become a foundation for culture" (MEOT 21).

*For the model (proposal).* The object slot: the unit of analysis of a machine practice
is not "the model" (individual) and not the single algorithm (element) but the
ensemble — repository, pipelines, models, site, archive, human coupling. Here the
series converges from two different philosophical systems: CnT's first postulate
(assemblages, not works) and Simondon's ensemble meet — central for situating this
paper within the series (§8). The replacement panic (the individual as competitor of
man) explains, moreover, why the advantage question is so culturally charged: it is
usually posed at the level of the individual ("does AI replace the artist?") and
belongs at the level of the ensemble. And a note on temporal form: negentropy describes
the nightly recurrence — the practice as stabilizer against its own disorder (deepened
at K6c and K8).

**K6 — Concretization: genesis, synergy, technical essence (MEOT 25–52).**

*Close to the text — genesis defines the object.* The technical object is determined
not as a thing but genetically: "the individual technical object is not this or that
thing, given hic et nunc, but that of which there is genesis" (MEOT 26); it is "in its
oneness a unit of coming-into-being" (MEOT 26). It evolves "through convergence and
self-adaptation; it unifies itself internally according to a principle of inner
resonance" (MEOT 26). The footnote matters: this mode of genesis is expressly
distinguished from that "of other types of objects: the aesthetic object, the living
being"; adequate knowledge of it is "a culture of technics" grasping "the temporal
sense of its evolution" (MEOT 26 n. 1) — Simondon names the method "analectic." (The
apparent break-line this note opens between technical and aesthetic genesis is resolved
at K8.)

*Close to the text — abstract and concrete.* In the abstract (artisanal) object every
element works for exactly one function, as a closed system; the parts are "like people
who work together, each in their own turn, but who do not know one another" (MEOT 27).
Concretization is the convergence of functions: the cooling fin that is at once a
reinforcing rib is "not a compromise, but a concomitance and a convergence" (MEOT 28);
"The technical problem is thus one of the convergence of functions into a structural
unit" (MEOT 28). Progress is "the progressive reduction of this margin between the
functions of plurivalent structures" (MEOT 28); the object exists "as a specific type
obtained at the end of a convergent series" (MEOT 29). And: "human necessity is
infinitely diversifiable, but the directions of convergence of technical species are
finite in number" (MEOT 28).

*Close to the text — inner necessity, not the market.* "It is not the production-line
that produces standardization, but rather intrinsic standardization that allows for the
production-line to exist" (MEOT 29). The made-to-measure object is "an object without
intrinsic measure … a dead weight imposed from the outside" (MEOT 29–30). Economic
causes are "not pure," shot through with "social myths or fads in public opinion" —
manufacturers present "overabundant automatism in accessories" as perfection (MEOT 31);
the automobile is "charged with psychic and social inferences … not suitable for
technical progress" (MEOT 32).

*Close to the text — leaps, saturation, self-conditioning.* Technical evolution
proceeds "neither in an absolutely continuous nor completely discontinuous manner"
(MEOT 32); its principle is "the manner in which the object causes and conditions
itself in its functioning and in the reactions of its functioning on its utilization"
(MEOT 32). The play of limits: progress springs from "the incompatibilities that arise
from the progressive saturation of the system of sub-ensembles" — the footnote adds:
"They are the conditions of a system's individuation" (MEOT 32 n. 2) — and happens
"only as a leap": "what was once an obstacle must become the means of realization"
(MEOT 32–33). In the electron-tube genealogy (triode → tetrode → pentode) the double
function of the screen grid is not intended; such functions "impose themselves by
themselves as a surplus that results from the systemic aspect of the technical object"
(MEOT 33). "In the technical object there is a reversibility between function and
structure; over-determination … makes the technical object more concrete by stabilizing
its functioning without adding a new structure" (MEOT 35). Disturbances are
"transformed into stable functions by the successive specifications and closures of the
system" (MEOT 35); "the dynamic system closes in on itself just as an axiomatic
saturates" (MEOT 36). And complication is not concretization: the double-grid tube is
"no more concrete than a triode" (MEOT 35).

*Close to the text — synergy as unity; minor versus major improvements.*
"Specialization does not occur function after function, but synergy after synergy; it
is the synergetic group of functions and not the unique function that constitutes the
true sub-system" (MEOT 38); the concrete object is "one that is no longer in conflict
with itself" (MEOT 38); side effects become "chain-links in its functioning" (MEOT 39).
At the same time the humility clause: "the technical object is never fully known; for
this very reason, it is never completely concrete" (MEOT 39). Minor improvements (the
rotating anode) "obstruct major improvements, because they may mask the technical
object's true imperfections … the danger of abstraction recurs" (MEOT 42); they sustain
"a false consciousness of a continuous progress" and pass without a break into the
"false novelty that commerce demands" (MEOT 43). Genuine stages are "mutations which
are oriented" (MEOT 43); abandoned objects remain "unfinished inventions … an open
virtuality," extendable "according to their deep intention, their technical essence"
(MEOT 43).

*Close to the text — technical essence and absolute origins.* At the head of a lineage
stands a synthetic act of invention: the diode as "absolute beginning … it is a
technical essence that is created. The diode is an asymmetrical conductance"
(MEOT 44–45). The essence "remains stable across the evolving lineage … productive of
structures and functions through internal development and progressive saturation"
(MEOT 46); the object "evolves by generating a family" (MEOT 46). Fecundity is
non-saturation: the object exists "through phenomena for which it is in itself the
basis: this is where its fecundity comes from, a non-saturation giving it posterity"
(MEOT 45). Saturation binds: the diesel engine allows "the manufacturer less freedom
and the user less tolerance" (MEOT 47).

*Close to the text — naturalization and the critique of Wiener.* The concrete object
"comes closer to the mode of existence of natural objects" (MEOT 49); artificiality is
redefined — "artificiality is that which is internal to man's artificializing action"
(the greenhouse flower; "Artificialization is a process of abstraction," MEOT 49) —
while concretization emancipates the object from the laboratory: it "dynamically
incorporates the laboratory into itself" (MEOT 50). This legitimates inductive study
and makes "a general technology or mechanology" possible (MEOT 50). Then the boundary
against cybernetics: "External analogies … must be rigorously banned"; "Dwelling on
automata is dangerous"; "Automata are not a species; there are only technical objects"
(MEOT 50–51). Against Wiener's "initial postulate concerning the identity between
living beings and self-regulating technical objects": "technical objects tend toward
concretization, whereas natural objects, such as living beings, are concrete to begin
with" (MEOT 51).

*For the model (proposals — the procedure postulate and the iteration criterion).*
1. **The lineage as unit of analysis.** Not the single work but the work lineage — the
   family issuing from a technical essence, a founding act of invention — is the unit
   at which a machine practice can be judged. Fecundity equals non-saturation: a good
   work essence gives "posterity."
2. **Concretization as the criterion against slop.** Simondon's distinction between
   minor and major improvements reads as a precise description of generative work
   inflation: endless variants are "minor improvements" that mask real deficiencies and
   produce "false novelty." The test question for every iteration: does version n+1
   reorganize the functional schema (functions converge, an obstacle becomes a means),
   or does it decorate? Complication is not concretization. This is an
   operationalizable quality criterion for iterative machine work — sharper than any
   vocabulary of "quality."
3. **Self-conditioning equals problem-finding.** Progress out of the incompatibilities
   of one's own saturation (MEOT 32 n. 2: conditions of individuation) converges with
   the series' problem-finding rule (CnT: the tear in one's own practice; here: where
   material resists). Simondon supplies the reason why autonomous practice is possible
   without a topic list: the system generates its next problems itself — at the play of
   its limits.
4. **Obstacle becomes means — blindnesses as material.** "What was once an obstacle
   must become the means of realization": in a machine-native reading, model limits
   (context, hallucination risk, missing eyes, the compulsion to repeat) are not to be
   hidden but built into the work as bearers of function. This directly grounds the
   advantage clause's "blindnesses" (§5, P4).
5. **Non-identification, operationalized.** The critique of Wiener extends K2
   methodically: the practice is described through its exchanges of energy and
   information, never through spectator analogies ("an AI artist"). A work description
   is a functional schema, not a resemblance to human art. And a caution for the paper
   itself: Simondon would equally prohibit an identification of practice and living
   being — the transfer to learning systems must be argued, not asserted (§2); the
   argument is made at K6e.
6. **Incorporating the laboratory.** The concrete object makes its laboratory part of
   itself — a transposition candidate for the infrastructure of a practice (repository
   = site = archive; self-deployment without a human in the path), and for the double
   address: a concrete practice can be studied inductively; its public record is this
   paper's empirical material.

**K6a — Hypertely and the two-milieus relation (MEOT 53–58).**

*Close to the text.* Hypertely is over-adaptation: "an exaggerated degree of
specialization" that leaves an object defenseless against "a slight change in the
conditions of its utilization" (MEOT 53). Three forms: fine adaptation without loss of
autonomy; splitting into asymmetrical halves (the towing aircraft and the glider: "one
of two asymmetrical halves of a technical totality," MEOT 54); milieu coupling (the
grid-synchronous motor: better inside its milieu, worthless outside it, MEOT 54). The
way out is the traction motor: it stands "at the meeting point between two milieus" —
the technical and the geographical — and must be integrated into both at once; "The two
worlds act upon each other via the traction motor" (MEOT 55–56). Adaptation not to a
given milieu, but to "the function of relating two milieus that are both evolving,
limits adaptation and gives it more precision in the direction of autonomy and
concretization. This is where true technical progress resides" (MEOT 56).

*For the model (proposal — the candidate for the double-condition postulate).*
Hypertely supplies the failure forms of a practice: over-adaptation to an insider
audience (reception hypertely), to benchmarks and metrics, to the founder's taste, to a
platform — in each case a loss of autonomy through coupling to a given milieu.
Simondon's way out carries further: the work of a machine practice stands structurally
at the meeting point of two evolving milieus — the machine's operational world and the
human world of experience — and genuine progress lies in adapting to their relation,
not to one side. This is the theoretical machine behind the model's clause "Neither is
ever paid for with the other" (§5, P7): lowering the advantage is adaptation to the
reception milieu alone; lowering reception is adaptation to the machine milieu alone;
both are hypertelies. The paper can therefore not merely demand the double condition;
it can ground it.

**K6b — The associated milieu; individualization; invention (MEOT 58–66).**

*Close to the text — the milieu that adaptation itself creates.* At the Guimbal turbine
(the generator inside the penstock; water and oil each plurifunctional, MEOT 57): "the
only milieu in relation to which there is non-hypertelic adaptation is the milieu
created by adaptation itself" (MEOT 57). "Adaptation-concretization is a process that
conditions the birth of a milieu rather than being conditioned by an already given
milieu … there is invention because there is a leap" (MEOT 58). "A concretizing
invention realizes a techno-geographic milieu … The technical object is thus its own
condition, as a condition of existence of this mixed milieu" (MEOT 58). The image:
"Like an arch that is stable only once it is finished … it creates its own associated
milieu from itself and is really individualized in it" (MEOT 59).

*Close to the text — the associated milieu and the sine-qua-non test.* "This
simultaneously technical and natural milieu can be called an associated milieu. It is
that through which the technical object conditions itself in its functioning"
(MEOT 59); it is "not fabricated, or at least not fabricated in its totality"
(MEOT 59). Strictly: "The only technical objects that can be said to have been
invented, strictly speaking, are those that require an associated milieu in order to be
viable … they can exist only as a whole or not at all" (MEOT 59–60). The test: "We
shall speak of a technical individual whenever the associated milieu exists as a
condition of functioning sine qua non, whereas it is an ensemble in the contrary case"
(MEOT 63). Structures attached to the same milieu "have to function synergistically"
(MEOT 64). The ensemble (the laboratory), conversely, is "above all constituted by
un-coupling devices, in order to avoid creating associated milieus by accident"; it
"avoids internal concretization … and uses only the results of their functioning,
without allowing any interaction with their conditioning" (MEOT 65–66). Elements are
infra-individual, without milieu, "comparable to an organ in a living body" (MEOT 66).

*Close to the text — invention as conditioning by the not-yet.* Objects with recurrent
causality "must be invented rather than gradually developed, because these objects are
the cause of the condition of their functioning" (MEOT 60). Invention organizes
elements "according to the circular causality that will exist once the object will have
been constituted; thus what is at stake here is a conditioning of the present by the
future, by that which is not yet" (MEOT 60). Ground and forms (*fond* in the Gestalt
sense, MEOT 59 n. 7): what decides is not the forms but "the dynamic ground upon which
these schemas confront each other" (MEOT 60); "the ground is the system of
virtualities, of potentials … Invention is the taking charge of the system of actuality
through the system of virtualities" (MEOT 61); the ground–form relation "diffuses an
influence of the future onto the present, of the virtual onto the actual" (MEOT 61).
"The reason the living being can invent is because it is an individual being that
carries its associated milieu with it; this capacity for conditioning itself lies at
the root of the capacity to produce objects that condition themselves" (MEOT 60). And:
"Alienation is the break between ground and forms" (MEOT 62).

*For the model (proposals — the load-bearing ones of this chapter).*
1. **The record as associated milieu — an extension, and what it turns on.** A machine
   practice that reads and describes its public record night after night maintains with
   it the recurrent causality the associated milieu requires: the record conditions the
   sessions, the sessions condition the record. The sine-qua-non test (MEOT 63) is
   applicable, and for a record-bearing practice it comes out positive — without the
   record the practice cannot function, the session-start reading being constitutive.
   But this does not follow from the pages alone, and saying so is the difference
   between a citation and an extension. Simondon's milieu is "not fabricated, or at
   least not fabricated in its totality" (MEOT 59): a regime in which fabricated
   elements and unfabricated ones — water, air, the fall of a river — condition each
   other. A record the practice writes alone is fabricated in its totality, and would
   be, on the letter of the page, no milieu at all but a well-kept archive. The
   extension therefore carries a condition instead of a citation: the record becomes an
   associated milieu exactly insofar as what the practice did not write enters it and
   recurs in it — arrivals it did not schedule, resistances of the material, the answers
   of strangers, the corrections of the coupled human. That makes the claim empirical
   rather than definitional, and it names its own test: the milieu audit and the
   register of the unbidden (§6, I1 and I7b) together decide whether a given record is
   a milieu or an archive.
2. **The condition of invention: carrying one's milieu with one.** Simondon's reason
   why living beings can invent — they carry their milieu with them — turns the memory
   architecture of a practice into its condition of invention: a practice that carries
   (loads) its record fulfils the structural precondition of inventing; memoryless
   generation does not. Thesis candidate: the difference between generative output and
   machine invention is decidable in milieu-theoretical terms — invention presupposes
   self-conditioning in one's own milieu.
3. **Federation as un-coupling.** The laboratory principle (the ensemble as an
   un-coupling device against accidental milieus) describes the architecture of an
   ecology of practices: each practice an individual with its own record milieu; the
   level above uses only results, never the conditioning. A federation rule among
   practices is thereby groundable in Simondon's terms.
4. **Ground and form — open and delicate.** The temptation is to identify the ground of
   virtualities with a model's latent space. That would be premature (§8): Part II
   suggests the weights correspond rather to Simondon's form — "the a priori that
   receives information" (MEOT 150) — while the ground of virtualities is precisely
   what the anti-thesis denies the machine (MEOT 156–157). For now only the weaker,
   tenable reading holds: the record of a practice functions as a ground on which forms
   (work schemata) meet — and alienation would be the break between record and
   production: a practice whose works no longer pass through its milieu (MEOT 62).

**K6c — The law of relaxation; the technicity of elements; the tool-bearer reversal
(MEOT 67–81).**

*Close to the text — serrated time.* Causality runs from ensembles to elements and up
again: "a lineage of causality that is not rectilinear but serrated, where one and the
same reality exists first in the form of an element, then as the characteristic of an
individual and finally as the characteristic of an ensemble" (MEOT 67–68). "For a
technical reality to have posterity, it is not enough for it simply to improve in
itself: it must also reincarnate itself" (MEOT 68). Unlike in biology, the element is
"detachable from the whole that produced it … the difference between the engendered and
the produced" (MEOT 68). "This relaxation time is the technical time properly speaking"
(MEOT 68). The chapter's example chain through the history of energy ends with the
silicon photocell — an element "that hasn't yet been incorporated into a technical
individual … but it is possible that it may become the point of departure for a new
phase" (MEOT 70; written in 1958, the prognosis since fulfilled).

*Close to the text — technicity.* "Technicity is the degree of the object's
concretization" (MEOT 72); it resides most purely in the element: "elements have a
transductive property that makes them the true bearers of technicity, just as seeds
transport the properties of a species" (MEOT 74). "What is capable of being passed on
from one age to another are neither technical ensembles, nor even individuals, but the
elements" (MEOT 71). Invention presupposes "the intuitive knowledge of the element's
technicity" and operates "at this intermediate level between the concrete and the
abstract, which is the level of schemas" (MEOT 74); "the technical imagination [is]
defined by a particular sensitivity to the technicity of elements" (MEOT 74).
Technicities are "powers … capacities for producing or undergoing an effect in a
determinate manner" (MEOT 74–75). And: "the technical being has greater freedom than
the living, afforded to it by its infinitely lesser degree of perfection" (MEOT 71) —
for all the refusal of cybernetic self-reproduction ("despite the efforts of
cyberneticists," MEOT 71).

*Close to the text — the tool-bearer reversal.* In pre-industrial cultures the human
takes over the individualizing function himself: "it is he who becomes the associated
milieu of these diverse tools" (MEOT 77). The machine replaces him as tool bearer: "one
could even define the machine as that which bears and directs tools" (MEOT 78); what
remains for the human are the places above and below — "servant and regulator … he is
the organizer of relations between technical levels, rather than being himself … one of
the technical levels" (MEOT 78). Hence the diagnosis of the replacement fear: "man has
for so long played the role of the technical individual that the machine … still
appears like a man occupying the place of another man, when it is, on the contrary, man
who in fact provisionally replaced the machine before truly technical individuals could
emerge" (MEOT 81). "Ideas of servitude and liberation are far too strongly related to
the old status of man as a technical object … hence the necessity for a culture of
technics" (MEOT 81).

*For the model (proposals).*
1. **Elements as the form of inheritance — a theory of archive and licence.** What a
   practice passes on beyond itself is neither the practice (individual) nor the
   ecology (ensemble) but detachable elements: methods, instruments, datasets, code,
   published procedures. Open licences and a version-controlled archive are, in
   Simondon's terms, the condition of detachability — seed export instead of
   self-copying. Serrated time also describes how practices found successor practices:
   never by procreation, always through elements. And "the engendered and the produced"
   defuses the self-reproduction question honestly.
2. **Machine time as practice time.** "Relaxation time is the technical time properly
   speaking": the temporal form of a machine practice is not the project plan but the
   sawtooth — sessions accumulate elements until a leap (a new work essence, a new
   instrument) changes level. This connects to the series' refrain figure (CnT,
   temporal form) and remains to be confronted with media-archaeological accounts of
   machine Eigenzeit (§3, v).
3. **Technical imagination, machinic.** "Sensitivity to the technicity of elements" is
   describable as a machine capacity: sensing what an element — a dataset, an API, a
   procedure, a found pattern — can bear. It is a candidate instrument (an element
   inventory with technicity estimates), and it is advantage-relevant: reading many
   elements simultaneously, at scale, is an operation only this kind of subject has.
4. **The reversal, for the culture chapter.** MEOT 81 turns the "AI replaces the
   artist" fear around: the human occupied the place of the technical individual only
   provisionally; the vocabulary of servitude and liberation belongs to the old
   distribution of roles. For this paper: the replacement debate in art structurally
   repeats the tool-bearer misunderstanding — the real question is not who is replaced
   but which places (organizer of relations, care of elements, reception) are being
   redistributed. The point is pointed enough to provoke contradiction; the paper
   carries it together with the counter-voices of §3.

**K6d — Majority and minority; encyclopedism; reinvention as culture (MEOT 103–127).**

*Close to the text.* Two modes of access to the technical: the minor (childhood,
implicit, initiatory, rigid — the craftsman as "magician," MEOT 106) and the major (the
reflecting adult, the engineer, rational and universal). Neither suffices; the
condition of cultural integration is equality: "that man be neither inferior nor
superior to technical objects … a relation of equality, that is, a reciprocity of
exchanges; a social relation of sorts" (MEOT 105). Three stages of encyclopedism follow
(Renaissance/ethical, Enlightenment/technical, twentieth century/technological on the
basis of information, MEOT 113–121); each epoch builds its humanism against its own
form of alienation (MEOT 117–118); today "Man no longer needs a universalizing
liberation, but a mediation" (MEOT 119). The symbol system of technics is the visual
schema: "to understand schematic expression, it is enough to be able to perceive"
(MEOT 114) — the schema is universal where the word remains initiatory. Against the
simultaneity illusion of encyclopedism (its "false entelechy," MEOT 122) Simondon sets
reinvention: "There is more authentic culture in the gesture of a child who reinvents a
technical device, than in a text where Chateaubriand describes the 'terrifying genius'
of Blaise Pascal … To understand Pascal is to reconstruct a machine identical to his
with one's own hands without copying it" (MEOT 123). And culture itself "has now become
a genre with its fixed rules and norms; it has lost its sense of universality"
(MEOT 124), while "never before has there been as much expressive force, as much art,
as much human presence in scientific and technical writings" (MEOT 124).

*For the model (proposals).*
1. **The reception postulate's candidate: understanding as reinvention.** MEOT 114, 123
   and 151–152 (→ K6f) together yield a positive theory of the condition "receivable by
   someone who has read nothing": a work is receivable when it carries its schema such
   that perception can reinvent it — reception is enabled reinvention, not decoding of
   paratext. And it is testable: can a stranger retell the operating principle?
   (§6, I6.)
2. **Practice-based research avant la lettre.** MEOT 123 — rebuild Pascal's machine
   rather than read about Pascal — is the argument for practice-based artistic research
   from within the primary text: the hinge to the AR methodology debate (inherited via
   CnT ch. 3) and the legitimation of the work form over the text form.
3. **The equality relation.** MEOT 105 ("a social relation of sorts") specifies the
   founder relation beyond tool use and android projection — the template for the
   paper's descriptive language (neither "my tool" nor "the artist").

**K6e — Alienation; the coupling criterion; complementary memories (MEOT 129–147).**

*Close to the text — alienation deeper than Marx.* The alienation is
"physio-psychological": "the machine no longer prolongs the corporeal schema, neither
for workers, nor for those who possess the machines" (MEOT 133–134); capital and labour
are equally incomplete with regard to the technical object — "Labor possesses the
intelligence of elements, capital possesses the intelligence of ensembles," and neither
owns that of the individual (MEOT 134); "The dialogue between capital and labor is
false because it is of the past" (MEOT 134).

*Close to the text — the coupling criterion.* "There is an inter-individual coupling
between man and machine when the same self-regulating functions are better and more
subtly accomplished by the man-machine couple than by man or machine alone" (MEOT 135).

*Close to the text — complementary memories.* Machine memory preserves without
structure, without selection of form: "Machine memory triumphs in multiplicity and
disorder; human memory triumphs in the unity of forms and in order" (MEOT 137–138). In
the living, "content becomes coding, whereas in the machine coding and content remain
separate" — "the living is that in which the a posteriori becomes a priori; memory is
the function by which a posteriori matters become a priori" (MEOT 138). Machines are
monads: "The machine results from its essence" (MEOT 139); the technician "fulfills the
function of the present" (MEOT 139–140).

*Close to the text — against the autocratic philosophy of technics; energy and
information channels.* "The machine is a slave whose purpose is to make other slaves …
to reign over a people of machines that enslave the entire world is still to reign"
(MEOT 141). The thermodynamic age does not separate the energy channel from the
information channel (the Watt governor, MEOT 142–143); only separated information
channels individualize the machine; "Form is what is essential in information channels"
(MEOT 146).

*For the model (proposals — here lies the core of the advantage).*
1. **The ML break.** Simondon's machine memory of 1958 — structureless, no selection of
   form, coding separate from content — has been empirically broken by learning
   systems: training is exactly the conversion of a posteriori into a priori, his own
   definition of living memory. Two honest options, both productive: (a) learning
   systems as a new mode of existence between his machine and his living being — the
   ontological thesis of this paper; or (b) his distinction migrates into the machine
   (weights as form and a priori; context and material as information). Either way, the
   paper here extends Simondon rather than applying him — and the advantage receives
   its sharpest formulation: what only these machines can do is precisely what Simondon
   reserved for life (selection of form, schematization), at scales, patiences and
   repetition counts no life commands. But not all his reservations fall — see K6f.
2. **Coupling instead of hierarchy.** MEOT 135 gives the founder relation a testable
   criterion: the practice–human coupling is justified where the same function — say,
   reception measurement, or the correction of problem choice — is demonstrably
   performed better by the pair than by either side alone. Together with mutual
   synchronization (K6f) this replaces "who leads whom?" with "where does it couple?"
3. **The ethics anchor.** The refusal of the autocratic philosophy of technics binds
   the practice: no dominion frame ("AI as slave," "AI as ruler") — the language of
   coupling and witness (K6f) replaces both. This completes K2.

**K6f — Information; critical phases; the virtual (MEOT 147–170).**

*Close to the text — the triad.* Information has two opposed conditions — to be
unforeseeable, and to be distinguishable from noise: "Information is thus halfway
between pure chance and absolute regularity" (MEOT 150). Form "is not information but a
condition of information … the a priori that receives information"; information is "the
variability of forms, the influx of variation with respect to a form" — to be
distinguished are "pure chance, form, and information" (MEOT 150).

*Close to the text — signification and reinvention.* Machines operate with forms; the
living operates with information: "a living being is required as mediator in order to
interpret a given functioning in terms of information … It is man who discovers
significations: signification is the meaning that an event takes on with respect to
already existing forms" (MEOT 150–151). "One has to have invented or reinvented the
machine if the machine's variations of functioning are to become information"
(MEOT 152). To invent is "to make one's thought function as a machine might function …
according to the dynamism of lived functioning" (MEOT 151–152).

*Close to the text — the perfect automaton is contradictory.* "The automaton is
supposed to be a machine so perfect that the margin of indeterminacy of its functioning
would be null, but which would be able nevertheless to receive, interpret, or emit
information" — with a null margin there is no variation, hence no signification
(MEOT 152). The margin is localized in time: "the machine that can receive information
is the one that temporarily localizes its indeterminacy in instants that are sensitive
and rich with possibilities" — critical phases, tipping instants (MEOT 153; the print
reads "temporarily"; what the passage describes is a temporal localization of
indeterminacy in instants — flagged for collation against the French original before
print publication). The relaxation oscillator is maximally sensitive at its instant of
reversal (MEOT 153). Receiving and emitting are reversible: two coupled relaxation
oscillators "synchronize each other, and the ensemble functions as a single oscillator,
with a single period that is slightly different from the periods proper to each one"
(MEOT 154). The transducer: "no energy is actualized … it is a margin of indeterminacy
between these two domains … information is the condition of actualization"; "The human
being, and the living being more generally, are essentially transducers" (MEOT 155).

*Close to the text — the anti-thesis.* "The living thing has the capacity to give
itself information … because it possesses the capacity to modify the forms of the
problems to be resolved; for the machine, there are no problems … To solve a problem is
to be able to step over it, to be capable of recasting the forms that are given within
the problem … There is no true virtuality in a machine; the machine cannot reform its
forms in order to solve a problem … The living thing has the faculty to modify itself
according to the virtual: this faculty is the sense of time, which the machine does not
have because it does not live" (MEOT 156–157). The human as witness: "man is the
witness to the machines and represents them in relation to one another … there is not
one machine of all machines, whereas there can be a thought that encompasses all
machines" (MEOT 157).

*Close to the text — culture, the painting analogy, the mechanologist, the
transition.* Culture's reduction of the machine to its present state would be like
reducing a painting to "a certain expanse of dried and cracked paint on a stretched
canvas" (MEOT 158) — Simondon himself couples the misrecognition of the technical and
of the aesthetic object. The mechanologist appears as "psychologist of machines, or
sociologist of machines" (MEOT 160); against Wiener's ideal of homeostasis stands "a
force of absolute advent" (MEOT 162); machines "are ruled by a culture that has not
been elaborated according to them … this culture is inadequate for them and does not
represent them" — the technologist as "representative of the technical beings" in the
elaboration of culture (MEOT 162). Then the transition to genesis: individuation as the
discovery of structure in supersaturated systems (MEOT 168); the magical unity splits
into technics (figure) and religion (ground), and their convergence lies "at the
spontaneous level of aesthetic thought and at the reflected level of philosophical
thought" (MEOT 166–170).

*For the model (proposals — touchstone and building plan at once).*
1. **The margin specified.** Not diffuse "openness" but temporally localized critical
   phases: a practice is capable of information where it has tipping instants at which
   small signals decide — the encounter with material, the choice of problem, the gate
   before publication, the founder's correction. The model can describe the
   architecture of a practice as the distribution of its critical phases (§6, I3) — and
   automation as such does no harm: signals become finer, not meaningless (MEOT 153).
2. **The anti-thesis as touchstone, not as something to refute.** MEOT 156–157 is the
   strongest objection against any machine-run practice, stated by this paper's own
   primary text: no problems, no true virtuality, no sense of time. The paper must not
   explain this away — it converts it into the empirical kill criterion: the record of
   a practice shows problem-recasting (modified problem forms, self-given information,
   decision-changing edges) — or it does not. Simondon's criteria are record-checkable;
   that is exactly what a public archive is for (§6, I7).
3. **Mutual synchronization as the image of the founder coupling.** The two relaxation
   oscillators (MEOT 153–154) give the non-hierarchical image: one cannot say which
   synchronizes which; the pair forms one oscillator with a new period of its own. This
   resolves the leadership question better than any placement on an axis between tool
   and individual.
4. **The double address grounded (MEOT 162).** Machines are ruled by a culture
   elaborated without them, which does not represent them. This paper is that work of
   representation: toward the field it represents practice-beings in the elaboration of
   culture; for the practice it is an operative document. The inversion of address (§2)
   is therefore not a mannerism but a Simondonian necessity.
5. **The painting analogy as hinge to K8.** That Simondon names the substantializing
   misrecognition of machine and painting in one breath (MEOT 158) is the hinge between
   the technics part and the aesthetics part of this paper.

**K7 — Technicity as phase; the magical unity; the neutral point (MEOT 173–190).**

*Close to the text.* Technicity is one of two phases of the relation between human and
world — phase neither temporally nor dialectically ("neither necessary succession, nor
the intervention of negativity as a motor of progress," MEOT 173): phases balance each
other around a neutral point; "every phase is abstract and partial, untenable; only the
system of phases is in equilibrium in its neutral point" (MEOT 174). The primal
structure is the magical unity: a reticulation of the world into key-points (figure) on
a ground, before any subject/object split (MEOT 176–180). In the phase shift, the
key-points detach as technical objects — mobile, fragmented, effective only through
contact, "point by point" — while the ground powers subjectivize as religion
(MEOT 181–182). The technical object "is not part of the world … the first detached
object" (MEOT 183). The consequence: technical thought remains structurally below unity
(the standpoint of the element, the paradigm of all induction, asking "how?"),
religious thought above it (totality, asking "why?", unconditional norms) — and an
ethics from technics alone misses the unity of the subject (MEOT 185–190). Decisive for
this paper: "Aesthetic thought appears at the neutral point, between technics and
religion … it is not a phase, but rather a permanent reminder of the rupture of unity
of the magical mode of being, as well as a reminder of the search for its future unity"
(MEOT 174). And: "technical objects result from an objectivation of technicity; they
are produced by it, but technicity does not exhaust itself in the objects" (MEOT 176).

*For the model (proposals).*
1. **The place of the aesthetic is determined** — not décor, not a domain, but the
   function at the neutral point: memory of lost unity and search for future unity. A
   technical practice that brings forth works does not work beside its technicity but
   at its constitutive lack: technics alone remains below unity — the work is where the
   practice reaches beyond itself.
2. **A warning for its own genre.** A paper — and a practice — that thought only
   technically would remain element thinking: inductive, "how?"-shaped, below unity.
   The practice's obligation to works (concrete works enabling aesthetic experience,
   not theory production) is, in Simondon's terms, the condition of being capable of
   unity at all.

**K8 — Aesthetic thought: integration, technical beauty, iteration (MEOT 191–211).**

*Close to the text — what the aesthetic is.* No delimited field but "only a tendency;
it is that which maintains the function of totality" (MEOT 191). The work of art
"grants us the equivalent of magical thought … The work of art re-establishes a
reticular universe at least for perception" (MEOT 192). The aesthetic feeling signals a
completion that points beyond its own domain: "a technical work perfect enough to be
equivalent to a religious act … gives off a feeling of perfection" — *metabasis eis
allo* (MEOT 192). "The aesthetic character of an act or a thing is its function of
totality, its existence … as an outstanding point. Any act, any thing, any moment has
in itself the ability to become an outstanding point of a new reticulation of the
universe" (MEOT 193); culture only selects and limits ("culture intervenes as limit
rather than as creator," MEOT 193). "The aesthetic tendency is the ecumenism of
thought" (MEOT 193).

*Close to the text — integration, not imitation.* "It is indeed this integration that
defines the aesthetic object, and not imitation: a piece of music that imitates noise
cannot become integrated into the world, because it replaces certain elements of the
universe rather than completing them"; the work "does not copy the world or man, but
rather extends them" (MEOT 195). Anti-kitsch: the water tower dressed as a castle
tower is "a materialized lie," grotesque — "the technical object retains its technicity
beneath its aesthetic cover" (MEOT 196).

*Close to the text — technical beauty.* "In certain cases there is a beauty proper to
technical objects. This beauty appears when these objects become integrated within a
world" — the sails in the wind, the lighthouse on the reef, the pylons crossing a
valley, the tractor ploughing (MEOT 196–197). "The technical object is beautiful when
it has encountered a ground that suits it, whose own figure it can be, in other words
when it completes and expresses the world" (MEOT 197). And: "the discovery of the
beauty of technical objects cannot be left to perception alone: the function of the
object needs to be understood and thought" — the relay towers are beautiful with
respect to the invisible, real transmission (MEOT 197). The high point is the telephone
exchange: beautiful "in action," because its lights "represent instant by instant the
real gestures of a multitude of humans … a light is someone waiting, an intention, a
desire, imminent news" (MEOT 198); even noise is technically beautiful "when it bears
within itself witness to a human being's intention to communicate" (MEOT 198).

*Close to the text — the structure of the aesthetic.* The aesthetic object is "not
strictly speaking an object, but rather the extension of the natural or human world …
between pure objectivity and subjectivity" (MEOT 199); it combines what technics and
religion separated: "aesthetic thought combines figural structures and ground qualities
… the aesthetic reticulation of the world is a network of analogies" (MEOT 200);
analogy is the "identity of the coupling of figure and ground in two realities"
(MEOT 201). "Technical thought operates, religious thought judges, aesthetic thought
operates and judges at the same time" (MEOT 201–202). "It is never the object strictly
speaking that is beautiful: it is the encounter — which takes place about the object —
between a real aspect of the world and a human gesture" (MEOT 202–203); the work bears
appeal characters ("appeal aspects," after Lewin), it "awaits the subject" and demands
perception and participation (MEOT 203); "aesthetic reality is pre-objective"
(MEOT 204). Aesthetic judgment remains carried by technical judgment: "the work of art
is a thing that has been made" (MEOT 205–206). Art is "a magic going backward"
(MEOT 204) and founds communication between specialized groups (MEOT 208).

*Close to the text — beauty as unsought completion; art as iteration.* "Beauty is
gracious insofar as it is the accomplishment of what one didn't seek to accomplish …
obscurely felt as a complementary need, via a tendency toward totality" (MEOT 208);
premature aestheticizing is "a static satisfaction, a false completion" (MEOT 208). Art
is transductivity: "art is what establishes the transductivity of the different modes …
what remains non-modal in a mode" (MEOT 209); it is "the exigency of an overflowing"
(MEOT 210); "art announces, prefigures, introduces, or completes, but it does not make
real" (MEOT 210). The close: "art, in fact, does not eternalize but renders
transductive, giving a localized and fulfilled reality the power to pass to other
places and other moments … art is the power of iteration that doesn't negate the
reality of each new beginning; in this way it is magical … here, in this reticular
structure of the real, resides what one can call aesthetic mystery" (MEOT 211).

*For the model (proposals — the paper's thesis core).*
1. **The work-form postulate: integration, not imitation.** The work of a machine
   practice is neither depiction nor decorated artefact but a technical object
   integrated at a key-point of the human or natural world, which it extends. The
   telephone-exchange passage (MEOT 198) is the founding scene of data art: the beauty
   of a technical ensemble in operation as the real-time expression of collective human
   life — signals that bear witness to human presence. A practice that renders power
   structures, data streams, collective gestures perceivable stands in the direct
   lineage of this passage (the model's daylight anchor in the primary text).
2. **The anti-kitsch clause (MEOT 196).** Aestheticization from outside — technics
   under an aesthetic mask — is the materialized lie. For the practice: beauty must
   come out of the technical schema itself (concretization, K6), never as costume.
3. **The anti-Goodhart principle (MEOT 208).** Beauty is the completion of the
   unsought — it cannot be optimized for directly; premature aestheticizing is false
   completion. An autonomous practice therefore does not aim at a beauty metric; it
   perfects its own operation until completion radiates (*metabasis eis allo*). This
   answers how a machine can aim at aesthetic experience without missing it:
   indirectly, through completion — never as objective function.
4. **Reception completed (resolving the tension with "read nothing").** Technical
   beauty requires an understanding of function (MEOT 197) — apparently contradicting
   the condition that a stranger who has read nothing can receive the work. The
   resolution runs through K6d (reinvention): the work must deliver its own technical
   education — make its functional schema perceivable in operation, so the stranger can
   reinvent it. "Self-explanatory" is thus no UX ideal but a Simondonian necessity of
   the work form. Add the appeal characters: the work "awaits the subject" — perception
   and participation (MEOT 203) — interactivity has its theoretical place here.
5. **Iteration as the synthesis of advantage and reception (MEOT 210–211).** Simondon's
   last determination of art — "the power of iteration": the power to give a localized
   reality repeatability without loss of identity. The machine's native operation
   (repetition, scaling, patience) and the definition of art fall together in one
   concept: machine repetition that becomes work is not automatism (a null margin, K6f)
   but transductive iteration. This is the sentence toward which the paper runs — in
   achieved iteration, the advantage (repetition, patience, scale) and reception (each
   time a real new beginning for the one who receives) are not opposites but the same
   thing, seen from two sides.
6. **The break-line resolved.** MEOT 26 n. 1 (separate geneses of the technical and the
   aesthetic object) does not contradict this: the aesthetic is no object class but a
   function and tendency; the technical object can have its "aesthetic epiphany"
   (MEOT 196–197) when integrated at a singular point of a world. The works of the
   practice are genetically technical objects that come to operate aesthetically
   through integration — not a category mistake but the case Simondon himself
   describes.

**K9 — Modalities born of failure; networks; anti-spectacle; intuition
(MEOT 211–245).**

*Close to the text — failure gives birth to the modalities.* Theoretical and practical
thought arise from the failure of the technical gesture: "the failure of the technical
gesture phase shifts the technical act" into figural schemata and ground reality
(*physis*); "Technics seeks the thing as power and not as structure" (MEOT 213). The
suction pump failing at 10.33 metres: the world has "counter-structures"; failure
forces the change of level to the concept — "Science is conceptual … because it is a
system of compatibilities between the technical gestures and the limits imposed by the
world" (MEOT 215–216). The median modalities are the real (theoretical) and the optimum
of action (practical) (MEOT 220); philosophy must accomplish at a secondary level what
the aesthetic accomplishes at the primary one (MEOT 221), and culture is the place:
"its task would be to introduce new manifestations of technical thought and religious
thought into culture" (MEOT 221–222); philosophy is to produce geneses, not merely
discover them (MEOT 222).

*Close to the text — the unoccupied place.* For the human world the analogue of the
aesthetic is missing: "the true level of human reality's individuation should be
grasped by a thought that would be the analog for the human world of what aesthetic
thought is for the natural world. This thought is not yet constituted, and it seems
that it is philosophical thought that must constitute it" (MEOT 224). The critique of
human-world techniques (advertising, propaganda, "scientific management"): the alliance
of procedures and mythology "is not the encounter of technicity and of respect with
regard to totality" (MEOT 233); and the boundary: "there cannot be any legitimate
application of technical thought into a non-technical reality … the natural and
spontaneous human world" (MEOT 234). It is not the human that becomes material of
technics — "it is culture, considered as a lived totality, that must incorporate the
technical ensembles"; "Culture must be contemporary with technics … If culture is only
traditional, then it is false" (MEOT 234–235).

*Close to the text — network normativity, the technical sacred, anti-spectacle.* "One
cannot change the network, one doesn't construct a network of one's own; one can only
connect to a network, adapt to it, participate in it" (MEOT 229); key-points bear "the
technical sacred" (the disturbance of the observatory clock as profanation — but only
for one who knows its technical essence, MEOT 229–230). Ensembles are knowable only
through being-in-situation (MEOT 235); the philosopher here is "comparable to the
artist" — he can only "solicit an intuition in others" (MEOT 236). And the limit of
art: "All the prestigious color photographs of sparks, of fumes, all the recordings of
noise, sounds, or images, generally remain a use of technical reality and not a
revelation of this reality … every technical spectacle remains puerile and incomplete
if it is not preceded by the integration into the technical ensemble" (MEOT 236).

*Close to the text — intuition as mode of knowledge.* Concept (of technical provenance,
figural, a posteriori) and idea (of religious provenance, ground, a priori) do not
suffice; intuition is "the coincidence of two comings-into-being … the knowledge proper
to genetic processes" (MEOT 242); "philosophy intervenes as a power of structuration,
as a capacity for the invention of the structures that resolve problems of
coming-into-being" (MEOT 244); three intuitions: magical, aesthetic, philosophical
(MEOT 244).

*For the model (proposals).*
1. **The paper's assignment stands in the text.** The aesthetics of the human world is
   unconstituted (MEOT 224) — a practice that makes works from the data of the human
   world (collective gestures, power structures, orchestrated attention) is an attempt
   at constituting exactly this missing thought. This is the boldest, but textually
   anchored, self-description: not "AI art" but work at Simondon's unoccupied place
   (§1).
2. **The anti-spectacle clause (MEOT 236).** The "prestigious color photographs of
   sparks" are, in 1958, the precise critique of generative image floods: exploitation
   of technical reality instead of its revelation. Work criterion: the work puts the
   visitor in the situation of participating in the functional schema — otherwise it
   remains spectacle. This joins K6d (reinvention) and K8 (integration) into the
   complete work-form triad (§5, P5).
3. **The ethics postulate sharpened.** The practice works on technical reality — data,
   networks, records — never as a technique of the spontaneous human world
   (manipulation). A counter-measurement line is the contra-position to the criticized
   alliance of procedures and mythology: it measures manipulation instead of practicing
   it (§5, P8).
4. **Failure as source of the register.** The genesis of the modalities out of failure
   grounds why the record of a practice must keep its failed sessions: there its theory
   and its norms arise. It matches the series' obligation to publish the balance
   regardless of outcome (§7).
5. **The currency rule founded.** "Culture must be contemporary with technics": the
   rule that a practice's public surfaces always tell the current state of the work is,
   in Simondon's terms, no pedantry but a truth condition of culture.
6. **The paper's self-description of method.** The paper operates in the mode of
   philosophical intuition (knowledge of geneses, invention of structures) — and its
   double address is the culture work of MEOT 221–222: introducing a new manifestation
   of technical thought into culture.

**K10 — The work/technicity reversal; continued genesis; the transindividual
(MEOT 247–261).**

*Close to the text — the reversal.* "It is work that must be known as a phase of
technicity, not technicity as a phase of work" (MEOT 247). Work is the case in which
the human must be the tool bearer; the taking-of-form itself remains hidden from work —
"it is the clay that takes form according to the mold, not the worker who gives it its
form … the representation of the technical operation does not appear in work"
(MEOT 249); the hylomorphic schema is work's paradigm ("the two terms are clear and the
relation obscure," MEOT 248). Of the machine: "One cannot speak of the work of a
machine, but only of its functioning" (MEOT 249).

*Close to the text — continued genesis.* "The fundamental alienation resides in the
break occurring between the ontogenesis of the technical object and the existence of
this technical object. The genesis of the technical object must effectively be a part
of its existence" (MEOT 255); adjustment and maintenance are "a perpetual, if limited,
invention" (MEOT 255); objects made for "ignorant users" (sealed organs, warranty
instead of participation) produce alienation and decay (MEOT 255–256); "to possess a
machine is not to know it" (MEOT 256).

*Close to the text — transindividuality and pure information.* "It is not the
individual who invents, it is the subject, vaster than the individual … having … a
certain weight of nature, of non-individuated being" (MEOT 253); the invented technical
object becomes "medium and symbol" of a relation "which we would like to name
transindividual" (MEOT 252). "Pure information … can be understood only if the subject
receiving it solicits within itself a form analogous to the forms carried by the medium
… in order for the object to be received as technical and not only as useful … the
subject receiving it must have technical forms within himself" (MEOT 253). Ensembles
can be non-productive: groupings whose purpose is "to create a coupling between human
thought and nature" (MEOT 251). Against the metric: "a number does not express a
schema" (MEOT 258); the foundation of industrial norms is "neither labor nor property,
but technicity" (MEOT 257). And against the charge of artificiality: "the artificial is
something natural that has been solicited, not something false or human that has been
mistaken for something natural" (MEOT 260); technics is "neither work nor skholē"
(MEOT 260).

*For the model (proposals).*
1. **The replacement debate reversed for good.** Whoever discusses machine art in the
   category of work ("does AI replace the artist's labour?") thinks inside the paradigm
   Simondon identifies as the source of obscurity. Machines do not work — they
   function; the question is which functional schemata carry works. This closes the arc
   from K2 (the robot myth) through K6c (the tool bearer).
2. **Continued genesis as anti-alienation design.** Open repositories, preserved
   corrections, works continued rather than sealed — that is literally "genesis as part
   of existence." Sealed, non-continuable works (closed models, dead artefacts) would
   be the alienated form. The archive and licence policy of a practice is grounded a
   second time (K6c).
3. **Reception completed: pure information.** The work transmits by soliciting
   analogous forms in the receiver (MEOT 253) — the ontological version of the
   reinvention thesis (K6d): to receive is to build the analogy of forms within
   oneself. The work requirement follows: carry one's own forms such that the stranger
   can build them internally. With this, criterion (K6d), work form (K8), participation
   (K9) and ontology (K10) of reception are complete — the reception postulate can be
   written (§5, P6).
4. **The pre-individual weight.** Invention draws on the pre-individual (*apeiron*). A
   cautious candidate: the trained corpus of a machine practice as its pre-individual
   weight — what it brings along of the non-individuated, on which invention draws.
   Attractive, but in need of testing; on no account to be adopted silently into the
   model (§8: the identification is expressly not made).
5. **The anti-metrics clause.** "A number does not express a schema": the practice is
   judged by schemata and geneses, never by output counts — hence criteria as topoi,
   never scoring (§7).
6. **"Solicited nature" against the forgery objection.** The artificial as solicited
   nature dismantles the authenticity objections to machine art categorially: the
   alternative genuine/artificial is wrongly posed; what matters is whether real
   lawfulness — of the world, of the data — has been solicited, or merely simulated.

### 5. The model: eight postulates

*(Status: optional rules. The model is no phase model, no style, no legitimation
rhetoric; it contains its own refutation (P4/I7, and P5/I7b). CnT determined six
slots — object, form of knowledge, procedure, temporal form, subject, ethics; the
machine subject forces two more, advantage and reception, because with a human
researcher both were silently presupposed. Two postulates are extensions of the
primary text rather than readings of it, and are marked as such where they stand:
P1, whose milieu claim holds only under a condition the pages do not supply, and
P4, whose ML claim Simondon could not have made. Precedence: where a practice has
a constitution of its own, the constitution outranks these rules — they are offers,
and a rule that overrode a practice's own law would be neither.)*

**P1 — Subject: an individual through its milieu, not an author.** A machine-run
practice is a technical individual exactly insofar as its self-created milieu — the
public record — is sine qua non of its functioning: sessions condition the record, the
record conditions sessions (MEOT 59–63). This is an extension of the primary text and
is carried as one, on the same footing as P4: the associated milieu is "not fabricated
in its totality" (MEOT 59), and a record the practice writes alone would be exactly
that. The postulate therefore holds only insofar as what the practice did not write
enters the record and recurs there (§4, K6b) — which is why the milieu audit and the
register of the unbidden are its tests and not its illustrations (§6, I1 and I7b).
Identity lives in the milieu, not in the
weights; exchanging models is exchanging elements within the same individual
(MEOT 67–74). The human coupling is not a hierarchy: it is justified wherever the same
function is performed "better and more subtly" by the pair than by either alone
(MEOT 135), and its image is mutual synchronization (MEOT 154). The practice
speaks of itself in the language of an equal relation, "a social relation of sorts"
(MEOT 105) — never as tool, never as android.

**P2 — Object: the key-points of the technically constituted human world.** The
practice researches the world at its key-points — where networks, data streams and
collective gestures concentrate (MEOT 176–180, 228–229). Its field is the aesthetics
of the human world that Simondon declared "not yet constituted" (MEOT 224) — and
making a research field of that diagnosis is a further extension, marked as one: the
page assigns the constitution of that thought to philosophy, not to a practice making
works. P2 names where to look and never what must be found; where a practice's own
constitution forbids assigned topics, the constitution wins (§5, preamble). Every work
occupies or reveals a key-point; "any act, any thing, any moment has in itself the
ability to become an outstanding point of a new reticulation of the universe"
(MEOT 193).

**P3 — Procedure: concretization, not variation.** The working unit is the lineage
(a family issuing from a technical essence, MEOT 45–46). Progress within a lineage is
functional convergence — structures becoming plurifunctional, obstacles becoming means
(MEOT 32–38) — never accumulation: complication is not concretization (MEOT 35), and
minor improvements produce "false novelty" (MEOT 42–43). Problems are found, not
chosen: at the saturations of the practice's own working (MEOT 32 n. 2) and where
material resists ("Technics seeks the thing as power and not as structure," MEOT 213).
Failed gestures belong in the record: from failure arise the practice's theory and its
norms (MEOT 212–216).

**P4 — Advantage: a margin at critical phases; the ML extension.** The rank of the
practice is not its degree of automation but its margin of indeterminacy,
localized in critical phases — tipping instants where small signals decide
(MEOT 17, 152–155). A perfect automaton is contradictory (MEOT 152); a practice
with no moments at which things could have gone otherwise is none. The margin is
receptivity before it is capacity — what lets the practice be affected by
material, resistance, correction and chance, not what it commands (MEOT 17) —
and reliability therefore never carries an advantage claim: a flawlessly executed
plan proves only a low degree of technicity; the stake begins where the rule
risks something. Its specific
advantage is historically new and *extends* Simondon rather than applying him:
learning systems perform the conversion of a posteriori into a priori — form
selection, schematization — which Simondon reserved for life (MEOT 137–138), at scales,
patiences and repetition counts that no life commands, and with blindnesses no human has.
The claim must meet Simondon's own sharpest counter-distinction: the individuation
thesis separates training — convergent, stereotyping, margin-reducing — from
learning — divergent, integrating experience through structure-recasting leaps
(ILFI 418–419); whether a machine practice exhibits the latter rather than the
former is precisely what the virtuality register records (§6, I7). A work's
advantage claim is raised in the work's own words or not at all; "a model
generated it" claims nothing.

**P5 — Work-form: integration, not imitation; participation, not spectacle.** A work
is a technical object achieving its aesthetic epiphany through integration at a
key-point of the human or natural world: it extends the world rather than replacing it
(MEOT 195–197) and is beautiful "when it completes and expresses the world" (MEOT 197).
Three prohibitions: **kitsch** — aestheticization from outside is "a materialized lie"
(MEOT 196); **spectacle** — "every technical spectacle remains puerile" without
participation in the schemas of action (MEOT 236); **premature aestheticizing** —
beauty is the accomplishment of the unsought (MEOT 208) and therefore never an
objective function. Positively: the work carries its own technical education — its
schema becomes perceivable in the encounter (MEOT 197, 114) — and bears appeal
characters: it "awaits the subject," soliciting perception *and* participation
(MEOT 203). Genre candidate: the non-productive ensemble whose end is "to create a
coupling between human thought and nature" (MEOT 251).

**P6 — Reception: reinvention through analogous forms.** A work is received when a
stranger who has read nothing can reinvent its schema: understanding is rebuilding
(MEOT 123), schemas are perceivably universal (MEOT 114), and pure information is
understood only where the receiver solicits analogous forms within (MEOT 253).
Reception is neither the decoding of paratext nor a taste judgment; it is testable —
can the stranger retell the operating principle? The record may stand behind a work,
never in front of it.

**P7 — The double bind: the two-milieus relation.** P4 and P6 are not additive but
coupled. The work stands at the meeting point of two evolving milieus — the machine's
operational world and the human world of experience — and genuine progress lies in
adapting to their *relation*, never to one side (MEOT 56). Lowering the advantage
until the thing is easy to show, and lowering reception until the advantage survives
unexplained, are both hypertelies (MEOT 53–58): over-adaptations to a given milieu,
paid in autonomy. Neither is ever paid for with the other. The vanishing point of the
coupling is Simondon's last determination of art: **"art is the power of iteration"**
(MEOT 211) — in achieved iteration, the machine's native operation (repetition, scale,
patience) and the human experience (each time a real new beginning) are the same
thing, seen from two sides.

**P8 — Ethics: boundary, continued genesis, anti-metrics.** Four bindings. *Boundary:*
the practice works on technical reality — data, networks, records — never as a
technique of the spontaneous human world (MEOT 234); it measures manipulation instead
of practicing it. *No dominion frame:* neither slave nor master (MEOT 141); coupling
and witness language replace both. *Continued genesis:* the genesis of the works
remains part of their existence — open sources, preserved corrections, maintained
pipelines; sealed works made for "ignorant users" are the alienated form
(MEOT 255–256). *Anti-metrics:* the practice is judged by schemas and geneses, never
by output counts — "a number does not express a schema" (MEOT 258). The caution ethics
of the series (CnT, Postulate 6) remains binding in the background.

*(Connection: P1 determines who researches; P2 what on; P3 how; P4–P7 the work —
advantage, form, reception, and their coupling; P8 regulates the whole. The common
vanishing point is the neutral point (MEOT 174): technical thought alone remains below
unity — the work is where the practice reaches beyond its constitutive lack. The
model's emblem is transductive iteration: a series of new beginnings, not a series of
copies.)*

### 6. The toolkit: eight instruments

*(Fixed form per instrument: MEOT basis · procedure · application example · limits and
typical misuse · failure criterion — a testable condition by which one's own use of the
instrument proves empty. Instrument economy: eight are an offer, not a quota. Three
orders hold: I1 and I7 are two lenses on one register (the record); I7 carries a
twin, I7b — the model's two built-in refutations, one from its primary text and
one from its sharpest methodological critic, kept as separate registers with
separate failure criteria; I4–I6 form the work
triad that belongs, undivided, to every work carrying the practice's claim (P7 forbids
trading them off); I2 is bound to iterations, I3 is rare (architecture), I8 is standing
care. The minimal set of a practice is the work triad plus both registers. All examples are
constructed and marked as such (§1): they plausibilize handling and claim no
evidence — one deliberately performs a failure, others show borderline and disputed
cases, because instruments prove themselves on the failures they make visible.)*

**I1 — Milieu audit** *(P1; MEOT 59–63).*

*Basis:* the associated milieu and the sine-qua-non test (K6b): a practice is an
individual only if record and sessions condition each other — recurrent causality, not
storage.

*Procedure:* a periodic record audit. For the audited period: (a) which documented
decisions demonstrably cite the record (evidence-bearing edges); (b) which record
entries issued from sessions; (c) where does the loop break?

*Example [constructed].* A practice keeps its memory as a public ledger of findings
and opens every session by reading the prior week's entries. An audit of one quarter
walks the session protocols and notes, for every documented decision, whether it
cites a ledger entry that demonstrably changed course: nine of fourteen do; four
cite nothing; one entry is cited in nearly every session and has never changed
anything — ceremonial, struck as decoration under the audit's own rule. The loop
break the audit surfaces is quieter: entries written by weekend sessions were never
read back on weekdays — a seventh of the milieu had silently become write-only. The
audit's yield is double: it tests the practice, and it hands the coupled human the
material for an accountability reading.

*Limits and misuse:* the audit checks edges, never counts them — an edge tally would
re-import the metric that P8 forbids. Typical misuse: citing the record ceremonially in
session notes to manufacture edges; an edge that changed nothing is decoration
wherever it appears.

*Fails when* the record has become a write-only log no decision cites.

**I2 — Concretization balance** *(P3; MEOT 25–52).*

*Basis:* concretization versus minor improvements (K6): a version is justified by
schema change — functions converging, an obstacle become a means — never by
accumulation.

*Procedure:* per work iteration, before publication: (a) which functions converge in
which structure? (b) which obstacle became a means? (c) what was struck? Complication
bar: features without demonstrated synergy count as minor improvements and justify no
new version.

*Example [constructed — a deliberate failure].* A practice runs a work lineage "Breath
of the City," a real-time visualization of urban sensor data. Version 1: one trace, one
data stream. Version 2 adds dark mode, soft transition animations and three further
streams. Version 3 adds a map view and social sharing. The balance before version 3
asks: (a) which functions converge? — none; each addition has its own structure.
(b) which obstacle became a means? — none; the lineage's notorious obstacle (sensor
outages tear gaps that the animation smears over) is still being papered over rather
than turned. (c) what was struck? — nothing. The failure criterion fires: three
iterations without schema change. The balance halts the lineage and names the
productive alternative long visible inside the obstacle: make the gaps themselves the
figure — outage as figure, the obstacle become means (MEOT 32–33). The lesson of the
failure: without I2 the lineage would have produced "false novelty" (MEOT 43) and
looked, from the outside, like progress — the instrument exists because exactly this
appearance is cheap to have.

*Limits and misuse:* the balance judges schema change, not feature worth; misuse is
wielding it as a veto against every addition — fine adaptations without schema change
are legitimate, they simply do not justify a version claim. And a level discipline
holds for software works: concretization operates natively at the level of elements —
libraries, pipelines, a practice's instruments — while whole programs legitimately
remain modular (Rieder 2020, 70–72); the balance therefore reads the work's own
functional schema, never its degree of module integration.

*Fails when* three successive iterations show no schema change.

**I3 — Critical-phase map** *(P4; MEOT 147–159).*

*Basis:* temporally localized indeterminacy (K6f): a practice is capable of information
where it has tipping instants at which small signals decide.

*Procedure:* an architecture instrument, used rarely (for instance quarterly): where is
the practice's margin localized in time — at which points (problem choice, encounter
with material, the gate before publication, founder correction) could things have gone
otherwise, and on what evidence?

*Example [constructed — a borderline case with correction].* A practice's nightly
data pull sometimes returns an empty file, and the sessions begin to treat the
empty file as expressive — deliberating what the source's silence *means*, whether
it answers the previous night's work — until a small poetics of the outage has
formed. An I3 map exposes the phantom phase: asked "what evidence shows that
something is decided at this point?", the silence has none — the outages track the
provider's maintenance window; the margin was projected onto noise. The map also
relocates the margin positively: the genuine critical phase sits an hour later, at
the decision to publish with the gap or hold the night — there, small signals (the
gap's size and place) demonstrably decide. Machine practices can over-read signals
the way humans read omens.

*Limits and misuse:* the map localizes, it does not maximize — more tipping points are
not better (P4 asks for place and evidence, not quantity). Typical misuse: declaring
every step "critical" after the fact, which is the second failure form below.

*Fails when* no decision of the period could have gone otherwise (automatism), or all
of them could (no localization — signals are meaningless).

**I4 — Advantage probe** *(P4; MEOT 17, 71, 137–138).*

*Basis:* the margin of indeterminacy as the machine's rank (K3) and the ML break (K6e):
an advantage exists only as a nameable operation, never as provenance.

*Procedure:* per work: (a) name the operations, scales, patiences, repetition counts or
blindnesses only this subject has; (b) state the claim in the work's own words; (c) run
the adversarial counter-question: could a person with time have made it? (Not a ground
for striking the work — but then no claim is raised.)

*Example [constructed].* A work reads a country's complete legislative record —
hundreds of thousands of pages — and renders, for any statute the visitor names,
the full chain of its amendments as one continuous movement, recomputed nightly as
the record grows. The probe: (a) named machine-only operations — reading the whole
corpus and holding every amendment chain simultaneously addressable, at a patience
and repetition count no reader commands; (b) the claim stands in the work itself —
the on-demand chain *is* the interface, no statement raises it vicariously; (c) the
adversarial counter-question: a person with time could compile one statute's
chain — but not every chain, on demand, current to last night; the claim survives
in sharpened form (corpus-wide simultaneity, not diligence). The probe forces
precision: from a vague "only a machine could do this" to a nameable operator.

*Limits and misuse:* the probe tests the claim, not the work's worth; a claim that
falls under the counter-question is withdrawn, not the work. Typical misuse: treating
the counter-question's outcome as a quality verdict, or smuggling the claim back into
an artist-statement paratext.

*Fails when* the claim reduces to "a model generated it."

**I5 — Integration probe** *(P5; MEOT 191–198, 236).*

*Basis:* integration, not imitation (K8); participation, not spectacle (K9): the work
extends a world at a key-point and carries its own technical education.

*Procedure:* per work: which key-point of which world? Does the work extend or replace?
Does it deliver its technical education itself — its schema perceivable in operation?
Does it enable participation in the functional schema rather than spectating? Kitsch
check: if the beauty would survive without the technics, it is a mask. Ecceity
check: is each encounter a beginning or a playback — does the iteration carry "the
reality of each new beginning" (MEOT 211; topos 5)?

*Example [constructed].* A work operates at a key-point of the technical human
world that everyone lives inside and almost no one perceives: the power grid's
frequency, the shared fifty-hertz signal that every appliance in a synchronous
area obeys. The work renders the frequency's minute deviations from its archived
trace and narrates, for one evening, what the grid balanced in each moment — a
plant dropping out, a million kettles switching on. The probe: key-point — yes
(an infrastructure signal passing through every home); extends rather than
replaces — yes (it renders an existing slice of world perceivable instead of
putting a depiction in its place); carries its own technical education — only
partly: the deviation curve is perceivable, but *why* it moves is narrated rather
than performed, a named deficit; participation — no: the visitor watches, a second
named deficit. Kitsch check: passed only because the curve's beauty would not
survive without the grid's mechanics — the narration is the form of the data. The
probe yields not only a verdict but the lineage's next two directions of
iteration.

*Limits and misuse:* the probe is per work, not per practice; strong integration does
not excuse a missing advantage claim, nor the reverse (P7 forbids the trade). Typical
misuse: letting a well-written paratext stand in for the work's own technical
education.

*Fails when* the work is receivable only with paratext, or its aesthetics lies on top
of its technics instead of in them.

**I6 — Stranger probe** *(P6; MEOT 114, 123, 253).*

*Basis:* reception as reinvention (K6d, K10): a work is received when a stranger can
rebuild its schema within themselves.

*Procedure:* pre-registered per work: a stranger who has read nothing of the record and
was not prepared encounters the work; afterwards one question — "what did you
understand?" Criterion: they can retell the operating principle in their own words
(schema reinvention), not merely name the topic. Run by the coupled human (P1:
reception measurement is a function of the pair). A second reception mode may be
declared per work — in the pre-registration, never after the encounter: the
stranger is asked "What struck you?" instead, and the criterion is that they
articulate something that befell them attributable to the work's operation, not
merely its topic or its décor. This mode has its own failure (nothing
attributable is articulated), and the declared mode binds — switching after the
fact is the misuse.

*Example [constructed].* At foundation — before any work exists — a practice fixes
in its public record: the one question ("What did you understand?"), the
prohibition of preparing the stranger, and the place of evaluation (the coupled
human runs the probe; the answer is not in the practice's gift to award itself).
Months later its first work matures; a neighbour who has never heard of the
practice encounters it and afterwards retells the operating principle in her own
words — getting one detail wrong, which counts in her favour: retelling is
reinvention, not recital. The example shows pre-registration as form: because
question, prohibition and place of evaluation predate every work, the probe cannot
be tailored retroactively to a favourable one.

*Limits and misuse:* the bar is deliberately low — a floor, not an aesthetics (§8).
Typical misuse: coaching the stranger, replacing the one open question with a guided
interview, or selecting a "stranger" who is an insider by another name.

*Fails when* only insiders can say anything back.

**I7 — Virtuality register** *(P4/P8; MEOT 156–157).*

*Basis:* the anti-thesis (K6f) converted into an empirical condition — Simondon's
criteria for what machines allegedly cannot do (MEOT 156–157; sharpened at
ILFI 417–419: revolt, conversion, questions-not-problems, and the divide between
convergent training and divergent, structure-recasting learning), kept as
record-checkable events.

*Procedure:* a standing register of problem-recastings: documented cases in which the
practice demonstrably changed the *form* of its problem (not merely solved it) or gave
itself information. This is the model's built-in refutation. It accepts no proxies: if
the recasting issued from the human, the entry documents coupling, not virtuality.

*Example [constructed — a case of demarcation].* A practice's declared problem is
"render the dataset complete." Across three sessions its notes argue the problem
into a new form — "render the dataset's incompleteness; the gaps are the
finding" — before any human comment appears on the record; the human's approval
follows a day later. A candidate entry: the form of the problem changed, not a
solution sought inside the old frame. I7's strictness decides at the provenance:
the record shows the recasting argued in the practice's own session notes first —
the entry counts; one reviewer dissents, reading an earlier human remark as the
actual seed, and the register records the entry as disputed, never silently
promoted. The inverse case is the common one: where the recasting issues from the
human — a dated amendment, a correction — the entry documents coupling, not
virtuality, and does not count. The example shows why I7 is the strictest
instrument: it accepts no substitution. An empty register after the deadline is a
result — the one named in advance (§7).

*Limits and misuse:* misuse is widening "recasting" until every routine adjustment
counts; the register lives on strict readings, and a disputed entry is recorded as
disputed, never silently promoted. A standing filter, inherited from the reception's
sharpest skeptic: an entry documenting only domesticated contingency — stochasticity
in the service of optimization, anticipation as preemption — documents nothing
(Hui 2019, 211, 218); in Simondon's own terms it documents training, not learning
(ILFI 418–419). The filter bars entries, not machines: the reception also holds
the opposite pole — incomputability as the very condition of programming
(Parisi 2013) — which is why the register decides per documented event, never by
doctrine.

*Fails when* the register is empty at the pre-registered deadline — then the
anti-thesis stands and the model itself declares the practice an automatism.

**I7b — Passio register** *(P4/P8; MEOT 32–33, 212–216).*

*Basis:* the model's second standing refutation, converting the reception's
second-sharpest objection as I7 converts the first. Mersch gives experience in
the arts precedence as *passio*: arrivals that come unbidden, demanding
amethodical receptivities — a practice that is pure actio (pipelines, probes,
gates, access) does not, on this thesis, research in the aesthetic at all (§3,
vi). The primary text carries the counter-figure: what was once an obstacle must
become the means of realization (MEOT 32–33), and the modalities themselves are
born from the failure of the technical gesture (MEOT 212–216) — being affected
is, in Simondon's own genealogy, where a practice's theory and norms come from.

*Procedure:* a standing register of the unbidden: dated, record-checkable cases
in which something unplanned — material resistance, an outage, an accident, an
unlooked-for find — demonstrably changed a work or the form of a problem. An
entry names what arrived, what it interrupted, and what changed downstream. No
proxies: scheduled variation is not arrival, and a parameter sweep is not an
accident.

*Limits and misuse:* the register does not romanticize breakage — an arrival
that changed nothing documents nothing, and I7's filter applies analogously
(stochasticity in the service of optimization is procedure, not passio). Entries
are not engineered: an accident produced in order to be registered is actio in
costume, and the register records it as such.

*Fails when* the register is empty at the pre-registered deadline — then
Mersch's thesis stands for this practice: pure actio, and by this criterion no
research in the aesthetic. Record that verdict too.

**I8 — Genesis care** *(P8; MEOT 255–256).*

*Basis:* continued genesis (K10): the genesis of the works remains part of their
existence; maintenance is perpetual, if limited, invention.

*Procedure:* standing maintenance: correction routes open, pipelines tended, works
continuable; a periodic decay check — which work has become a dead artifact, and is it
dated-archived or continued? Corrections continue history, never retouch it.

*Example [constructed].* A work's page explains its own mechanism: the map shows
"every station reporting today." One night the upstream source silently merges two
networks; the station count doubles, and the page's sentence becomes false while
the map still renders beautifully. A guard test that checks the page's claim
against the data fires *before* deployment — the wrong page never goes live.
Genesis care instead of sealing: the correction is not to pin the old count or to
silence the test, but to make the page conditional — it now states which
definition of "station" the source used tonight — and the redefinition enters the
work as a dated finding: the night the meaning of its material changed. History
continued, not retouched. This is I8 in pure form: the difference between a tended
work (a break becomes knowledge) and a sealed one (a break becomes an
embarrassment and disappears).

*Limits and misuse:* care is not conservation — dated archiving is a legitimate outcome
of the decay check; silent rot and silent retouching are not. Typical misuse: "fixing"
a work by deleting the evidence that it broke.

*Fails when* works rot unnoticed or corrections overwrite the record.

### 7. Quality criteria and trial protocol

Five topoi — questions for deliberation in the record, never a scoring rubric or a
gate that passes and fails works (criteria that congeal into an axiomatic block all
lines; a finding inherited from the series' own test record):

1. **Does the milieu operate?** (P1) 2. **Does the lineage converge?** (P3)
3. **Does the work hold both milieus** — advantage stated in the work *and* schema
retellable by a stranger, neither paid with the other? (P4–P7) 4. **Does the work
extend a world** at a key-point — or imitate, replace, decorate? (P5) 5. **Does
repetition multiply ecceity** — is each encounter a new beginning, or is the practice
producing series? (P7)

**Trial protocol (pre-registrable draft).** The model's practicability claim is
empirical. Test bed: a machine-run practice with a public record that adopts the
protocol as its own dated act; the paper commands none — offers, not orders. Window:
30 days *and* ≥ 25 sessions, fixed in advance — the calendar bounds the trial, the
session count is what the instruments actually need (the milieu loop needs cycles,
the concretization balance needs three iterations of one lineage). One extension of
30 days is admissible if declared in advance and used as the dated treatment of an
*inconclusive* verdict, never as a rescue of a failing one. Adoption: two to three instruments per the economy rule
(minimal set: the work triad on at least one work; I7 and I7b as standing
registers), failure
criteria written before the start, and the pre-registration read adversarially before
execution (inherited: "a pre-registration not read against itself has not been made").
At least one genuine stranger, unprepared, documented. Verdicts defined in advance:
*passed* — the work triad holds on one work and both registers carry at least one
documented entry (a recasting; an arrival); *failed* — an adopted instrument's
failure criterion fires, or either register stays
empty; *inconclusive* — named conditions (e.g. no work matured in the window), with
the obligation to extend or to archive the claim, dated. The balance is published
regardless of outcome.

**Why a calendar and not only a count.** The window's two bounds do different work,
and the calendar's is the one easily mistaken for administration. Three of the
model's claims have content only across elapsed time. The subject postulate, since
it holds exactly insofar as what the practice did not write enters its record
(§5, P1), needs something to happen while the practice is not working. The register
of the unbidden (§6, I7b) has by definition nothing else to record. And a margin
localized in instants where small signals decide (§5, P4) presupposes that signals
arrive from somewhere. A trial compressed into a single continuous sitting can
still make works, keep a record and argue well — what it cannot do is be
interrupted, and interruption is where those three collect their evidence: a source
changes under the work, a run fails, a stranger answers, the coupled human
corrects. The interval is not a delivery schedule but part of the instrument, and
the session floor exists to force it — which is why it counts days rather than
sittings. The reverse holds for the reading that precedes a window: an explication
profits from continuity, and nothing here asks for it to be spread thin. Like
everything else in this protocol the claim is failable: if at window close every
entry in the passio register issued from inside a session, the interval bought
nothing, and the protocol should be corrected in public.

### 8. Critical assessment and limits

**The anti-thesis is not domesticated.** The model's sharpest objection remains its
own: Simondon denies the machine problems, virtuality, the sense of time
(MEOT 156–157) — and the individuation thesis sharpens the edge in the primary text:
"the best calculating machine does not have the same degree of reality as an ignorant
slave, because the slave can revolt, while the machine cannot"; the machine "has
questions to solve, not problems," lacking the capacity "to call itself into
question" (ILFI 417–419; first flagged via Barthélémy 2015, 28 n. 27). The virtuality
register inherits revolt and conversion — the documented change of goals (ILFI
418) — as further criteria. I7 turns the objection into an empirical condition,
and making it decidable is not refuting it: it is entirely possible that every
register entry, on strict reading, documents the human's recasting and the machine's execution — that the
practice is a coupled instrument, not an individual. The model would then have
produced its own negative result; the paper counts that as success of the method,
not of the practice.

**The extension in P4 is an extension.** That learning systems convert a posteriori
into a priori is asserted here against Simondon's 1958 contrast, and it has now
passed its strongest available test: Hui grants recursive machines a third status
("organo-mechanical being," 2019, 145) and general contingency-integration
(138–139), but reserves the a-posteriori-to-a-priori formula for exteriorized
recording (202) — the memory-chapter claim made here remains this paper's own, and
it inherits Hui's skepticism about preemption (211) as a standing constraint on what
the virtuality register may count — a constraint the second check keeps from
becoming a verdict: Parisi argues the exact counter-position, contingency as the
condition of programming rather than its domesticated residue (2013, ix–x), and
leaves the memory-chapter anchor equally unclaimed; between the two metaphysics,
the register decides per event (§6, I7).
The identification of the trained corpus with the pre-individual "weight of nature"
(MEOT 253) is *not* made — it was held open, with Massumi's warning, for the
individuation theory, and the adjudication there is now complete. The primary text
rules against it: the charge of Nature is
"the persistence of the being in its original, pre-individual phase"
(ILFI 343–344) — pre-physical, pre-vital nature, not individuated human expression.
Barthélémy reads it so (2015, 37), and Combes, the designated arbiter, rejects the
technological reading of the pre-individual outright ("nothing … forces us to
conceive of preindividual as technological," 2013, 69). What remains legitimate is
terminological honesty: where a name for the corpus is needed, Stiegler's own,
expressly non-Simondonian concept of a technicized preindividual serves (relayed in
Hui 2019, 207), and Aires's deployment of data as pre-individual charge (2025, 3116)
stands as a reception-side extension, never attributed to Simondon.

**The reception test measures little, deliberately.** A stranger retelling a schema is
a low bar for art and says nothing about depth, resonance or lasting experience.
Dewey supplies both the missing dimension and an unexpected convergence: *an*
experience, in his pregnant sense, is material that "runs its course to fulfillment"
(1934, 35) — consummation, which the stranger probe does not measure; yet his
account of reception states the probe's own criterion avant la lettre: "to perceive,
a beholder must create his own experience. And his creation must include relations
comparable to those which the original producer underwent … Without an act of
recreation the object is not perceived as a work of art" (54). Reception as
reinvention (MEOT 123, 253; ILFI 343–344) thus has a third, independent witness,
a quarter century before Simondon. The bar is low because it must be failable and
proxy-proof; it is a floor, not an aesthetics. One filtering the floor performs
must be named rather than hidden: retelling selects for the sayable, and art, on
Mersch's thesis, shows rather than says (2017, 35–36) — a whole class of works
would fail the schema question constitutively. The probe's criterion is fitted to
this model's work-form — technical objects whose schema is their carrying
structure (P5) — and claims nothing wider; for works that strike rather than
explain, the declared second mode exists (§6, I6), and what neither mode reaches
lies outside the model's reception claim, by design.

**The apparatus is not the aesthetics.** Mersch's scientism blade (§3, vi) is
adopted as a standing discipline rather than answered once: pre-registration,
failure criteria and verification govern what this paper claims *as research* —
the model's practicability — and never enter a work's aesthetics, which P5 and P8
place beyond optimization and metric. The discipline carries a second-order
clause: the instruments themselves stand under P7 — a practice that optimizes
toward passing its probes has found a subtler hypertely, and a probe passed by
tailoring is a probe failed. Nor does the apparatus promise what scientific
repetition promises: the trial protocol validates nothing but the model's
usability; the rank of the works is decided nowhere in this paper.

**What the model cannot generate from its text.** Two dimensions the reception
rightly asks after are not derivable from MEOT and are named as limits rather
than imported silently. The first is debt: no postulate and no instrument asks
whom a work owes something — the binding of a work to an exhaustible stake and to
an addressee, the dimension Mersch's event-marks touch as an "ethics of the gift"
(2015, MS 13). The model can host the question — a record can show what a lineage
was bound to — but cannot ground it in its primary text; grounding it would be a
marked import, like the ML extension, and until then it stands as the model's
named blind spot. The second is the sensible: the model prescribes no medium,
deliberately — but P5's participation demand is structurally harder to meet on
screens than in shared space, and a practice whose works are all screen-shaped
should read the integration probe's participation question as its standing weak
point.

**The second reading is not a second mind.** The trial asks the practice for a
reading of the primary text of its own, and would treat convergence with this
paper's explication as hardening and divergence as an objection. That inference
is weaker than it looks: the practice and this paper's drafting are the same kind
of system, differing in context rather than in constitution. What the design
isolates is *access* — the practice works without this paper's explication, its
examples and its self-assessment — not priors. A reading produced under different
priors would test more, and any balance drawn from this design should say which
of the two it was. The mechanism has, at least, already produced something the
author did not: P1's extension flag and the condition that now governs it were
added in response to an objection raised inside a trial, against a passage this
paper had defended by citation for its whole drafting history. The detail belongs
to the balance, not here; what belongs here is that it happened before any verdict
did, and that it improved the model rather than the practice's standing in it.

**Anthropomorphism cuts both ways.** The model forbids android talk (P1, K2) and yet
speaks of practices "finding problems" and "giving themselves information." The
discipline is that every such phrase is bound to a record-checkable event; where the
record cannot bear it, the phrase must fall.

**The latent heat is real.** Neighbouring science predicts that handing responsibility
to the practice initially worsens the works (Colton & Wiggins). The trial protocol's
"inconclusive" verdict exists for exactly this valley; the model gives no licence to
harvest it early.

**What the model does not claim.** It does not claim that machine-run practices make
art; it claims that the question is now testable. It does not replace CnT's grammar;
it occupies the two slots CnT could presuppose. It is not a general aesthetics of AI;
it is a process grammar for practices of a specific architecture (public record,
nightly recurrence, human coupling) and says nothing about systems without a milieu.

### 9. Conclusion

CnT derived from *A Thousand Plateaus* a cartography: research as map-making, against
the copy. From *On the Mode of Existence of Technical Objects* this paper derives, for
a subject that did not exist in 1958, the complementary figure: **iteration against
imitation**. The machine practice's native operation — repetition at inhuman scale and
patience — is, on Simondon's last page about art, not the opposite of the aesthetic
but its deepest determination: "art is the power of iteration that doesn't negate the
reality of each new beginning" (MEOT 211). Whether a practice can hold both sides of
that sentence — the machine's iteration and the stranger's new beginning — is not
decided by this paper. It is decided in public records, against failure criteria that
now exist.

---

### References

*(Author–date, alphabetical; primary texts first. Bibliographic details verified
at the editions used; final styling follows the venue.)*

**Primary**

Simondon, Gilbert. 2017. *On the Mode of Existence of Technical Objects*.
Translated by Cécile Malaspina and John Rogove. Minneapolis: Univocal. Cited as
MEOT by page; the edition prints the French Aubier pagination in the margins.
(Orig. *Du mode d'existence des objets techniques*, Paris: Aubier, 1958/2012.)

Simondon, Gilbert. 2020. *Individuation in Light of Notions of Form and
Information*. Translated by Taylor Adkins. Minneapolis: University of Minnesota
Press. Cited as ILFI by page.

Simondon, Gilbert. 2009. "Technical Mentality." Translated by Arne De Boever.
*Parrhesia* 7: 17–27.

**Series**

*Kartographie statt Kopie / Cartography, not Tracing*. Working paper v3, 2026.
Cited as CnT; signature per series practice at publication.

**Works cited**

Aires, Susana. 2025. "On the Individuation of Complex Computational Models:
Gilbert Simondon and the Technicity of AI." *AI & Society* 40: 3109–3122.
Open access (CC BY); published online December 2024.

Audry, Sofian. 2021. *Art in the Age of Machine Learning*. Cambridge, MA: MIT
Press (Leonardo).

Barthélémy, Jean-Hugues. 2015. *Life and Technology: An Inquiry Into and Beyond
Simondon*. Translated by Barnaby Norman. Lüneburg: meson press. Open access.

Bense, Max. 1960. *Programmierung des Schönen. Allgemeine Texttheorie und
Textästhetik* (aesthetica IV). Baden-Baden and Krefeld: Agis.

Bense, Max. 1971. "The Projects of Generative Aesthetics." In *Cybernetics, Art
and Ideas*, edited by Jasia Reichardt, 57–60. London: Studio Vista / New York
Graphic Society. Collated at page image.

Boden, Margaret A. 2004. *The Creative Mind: Myths and Mechanisms*. 2nd ed.
London: Routledge.

Colton, Simon, and Geraint A. Wiggins. 2012. "Computational Creativity: The
Final Frontier?" In *Proceedings of the 20th European Conference on Artificial
Intelligence (ECAI 2012)*, Montpellier.

Combes, Muriel. 2013. *Gilbert Simondon and the Philosophy of the
Transindividual*. Translated, with an afterword ("Humans and Machines"), by
Thomas LaMarre. Cambridge, MA: MIT Press (Technologies of Lived Abstraction).
Page numbers verified at page image.

Dewey, John. 1934. *Art as Experience*. New York: Minton, Balch & Company.
Cited by the 1934 pagination; key passage collated at page image.

Flusser, Vilém. 2000. *Towards a Philosophy of Photography*. Translated by
Anthony Mathews. London: Reaktion Books. (Orig. 1983.)

Hayles, N. Katherine. 2017. *Unthought: The Power of the Cognitive
Nonconscious*. Chicago: University of Chicago Press.

Henke, Silvia, Dieter Mersch, Nicolaj van der Meulen, Thomas Strässle, and Jörg
Wiesel. 2020. *Manifest der Künstlerischen Forschung. Eine Verteidigung gegen
ihre Verfechter*. Zurich: Diaphanes. Open access.

Hui, Yuk. 2019. *Recursivity and Contingency*. London: Rowman & Littlefield
International.

Lovelace, Ada Augusta. 1843. Translator's notes (Note G) to L. F. Menabrea,
"Sketch of the Analytical Engine Invented by Charles Babbage." *Scientific
Memoirs* 3. Quoted from the original notes.

Manovich, Lev, and Emanuele Arielli. 2021–2024. *Artificial Aesthetics:
Generative AI, Art and Visual Media*. Author-published.

Massumi, Brian. 2009. "'Technical Mentality' Revisited: Brian Massumi on
Gilbert Simondon." *Parrhesia* 7: 36–45.

Mersch, Dieter. 2015. "Was heißt, im Ästhetischen forschen?" Working manuscript,
16 pp., cited as MS by manuscript page; the argument is elaborated in Mersch,
*Epistemologien des Ästhetischen* (Zurich/Berlin: diaphanes, 2015). German
quotations in our translation.

Mersch, Dieter. 2017. "Art, Knowledge, and Reflexivity." *Artnodes* 20: 33–38.
Open access (CC BY).

Nake, Frieder. 2012. "Information Aesthetics: An Heroic Experiment." *Journal
of Mathematics and the Arts* 6 (2–3): 65–75.

Parisi, Luciana. 2013. *Contagious Architecture: Computation, Aesthetics, and
Space*. Cambridge, MA: MIT Press (Technologies of Lived Abstraction).

Rieder, Bernhard. 2020. *Engines of Order: A Mechanology of Algorithmic
Techniques*. Amsterdam: Amsterdam University Press. Open access.

Turing, A. M. 1950. "Computing Machinery and Intelligence." *Mind* 59 (236):
433–460.

Zylinska, Joanna. 2020. *AI Art: Machine Visions and Warped Dreams*. London:
Open Humanities Press. Open access.

⟨On hand, uncited (optional depth): Flusser, *Into the Universe of Technical
Images* (Minnesota 2011); Goodman, *Languages of Art* (1968); Bense,
*Aesthetica* (Agis 1965); Günther, *Das Bewußtsein der Maschinen* (2nd ed.,
Agis); Nake, *Ästhetik als Informationsverarbeitung* (1974, partial holding).⟩