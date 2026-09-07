#!/usr/bin/env python3
"""The hand verdicts.  Every one is mine, entered by reading the row's text in full.

The labels and their definitions were fixed in PREDICTIONS.md §4 before audit.py drew a single
row.  That is the only thing tonight repairs about Session 82's open thread 3; the deeper problem
it names -- one adjudicator -- is not repaired and is declared again in the work.

Borderline rules applied, and both were needed:

  Sample B, on `expected`.  "X is expected to Y" reporting a state of affairs or a forecast is
  NOT_EXHORTATION_DESCRIPTIVE.  "can/may/could reasonably be expected to" forming a standard of
  knowledge, capacity or foreseeability is NOT_EXHORTATION_OTHER, because there the pattern has
  misread a legal test as a directive.  The line between them is stated here rather than left to
  the reader to reconstruct.

  Sample A, on generosity.  PREDICTIONS.md §6.5 declared REASONED deliberately easy to satisfy,
  because 10.5.2's bar is *without giving reasons for them* and not *without giving good reasons*.
  It was applied that way throughout, including where the ground is a purpose clause attached to
  only one of several measures in the recital.  The consequence is in the work: the near-unanimity
  of the result is partly a property of that choice, and P6 was closer to unfailable than I saw
  when I set it.
"""

# ---- Sample A: the 10.5.2 audit.  REASONED | BARE | NO_MEASURE ----------------------------------
SAMPLE_A = {
    "A-32014L0024-r20": ("REASONED", "purpose clause 'For the purposes of estimating the value'; the subdivision rule is grounded on 'objective reasons' and illustrated"),
    "A-32013R1308-r123": ("REASONED", "'For a better management of wine-growing potential'"),
    "A-32017R0625-r10": ("REASONED", "legal premise: the two named acts authorise GMOs irrespective of basis, so the same control rules follow"),
    "A-32013R1308-r178": ("REASONED", "'Due to the specific economic situation of the production and marketing of reindeer'"),
    "A-32023R2854-r46": ("REASONED", "'In order to promote continued investment ... while avoiding excessive burdens'"),
    "A-32022R2065-r44": ("REASONED", "'That obligation should allow for the effective oversight and, where necessary, enforcement'"),
    "A-32021R0241-r69": ("REASONED", "'in order to ensure uniform conditions for the implementation'"),
    "A-32014L0024-r90": ("REASONED", "'with a view to ensuring an objective comparison of the relative value of the tenders'"),
    "A-32017R0625-r91": ("REASONED", "problem stated: 'whistleblowing could be deterred by the lack of clear procedures or for fear of retaliation'"),
    "A-32014L0024-r121": ("REASONED", "empirical premise: 'The evaluation has shown that there is still considerable room for improvement'"),
    "A-32024R1689-r8": ("REASONED", "'A Union legal framework ... is therefore needed to foster the development, use and uptake of AI'"),
    "A-32024R0900-r42": ("REASONED", "'are by virtue of this role in a position to ensure ... Those service providers should therefore'"),
    "A-32018R1725-r35": ("REASONED", "'The principles of fair and transparent processing require that the data subject be informed'"),
    "A-32013R0575-r69": ("REASONED", "closest call in the sample; the ground is carried by 'in line with the actual risk of the position', and the generous rule of §6.5 takes it"),
    "A-32014L0024-r56": ("REASONED", "grounds are the costs 'in particular in terms of adaptations to existing e-procurement solutions' and 'how well it has worked'"),
    "A-32013R1308-r44": ("REASONED", "'on account of their positive structural effects on the wine sector'"),
    "A-32016L0680-r88": ("REASONED", "'in the light of the case-law ... in a manner which fully reflects the objectives of this Directive'"),
    "A-32024R1689-r161": ("REASONED", "'To avoid overlapping competences'"),
    "A-32018R1725-r72": ("REASONED", "'is an essential component of the protection of natural persons'"),
    "A-32023R2854-r54": ("REASONED", "'To avoid cases in which two or more dispute settlement bodies are seized for the same dispute'"),
    "A-32024R1689-r140": ("REASONED", "'for developing certain AI systems in the public interest'; and 'to adequately mitigate any identified significant risks'"),
    "A-32023R2854-r68": ("REASONED", "'For the exercise of their tasks in the areas of prevention, investigation, detection or prosecution'"),
    "A-32015L2366-r8": ("REASONED", "'in order to avoid divergent approaches across Member States to the detriment of consumers'"),
    "A-32019R0881-r100": ("REASONED", "borderline; the objective is carried by 'whether the bodies concerned carry out their tasks in a harmonised way'"),
    "A-32016R0679-r64": ("BARE", "TWO directives -- verify identity, do not retain for the sole purpose of replying -- and no ground of any kind stated for either.  The one BARE in the sample, and it is in the GDPR"),
    "A-32009R1223-r59": ("REASONED", "'in order to facilitate the consistent implementation of this Regulation'"),
    "A-32014L0024-r67": ("REASONED", "'because only the elements suitable for automatic evaluation ... may be the object of electronic auctions'"),
    "A-32016R0679-r62": ("REASONED", "grounds enumerated: already possesses, laid down by law, impossible or disproportionate effort"),
    "A-32023R2854-r47": ("REASONED", "'Costs ... are either specific to a particular request or shared with other requests.  In the latter case ...'"),
    "A-32022R1925-r77": ("REASONED", "'The services in the digital sector ... can change quickly'; 'To ensure that this Regulation remains up to date'"),
    "A-32024R0900-r89": ("REASONED", "'in order to allow for the effective oversight of this Regulation'"),
    "A-32024R0900-r62": ("REASONED", "'to raise user awareness and help the clear identification' -- though the seven-year retention period in the last sentence is itself given no ground"),
    "A-32022R2065-r58": ("REASONED", "'Recipients ... should be able to easily and effectively contest ... Therefore, providers ... should be required'"),
    "A-32012L0027-r49": ("REASONED", "'has the potential to contribute to economic growth, employment, innovation ... and therefore makes a positive contribution'; this recital is also a Family A exhortation, which is a consistency check rather than a problem"),
    "A-32013R0575-r60": ("REASONED", "'particular prudence is necessary'; 'This is especially important in the case of large exposures'"),
    "A-32011L0083-r27": ("REASONED", "'as it is already subject to other Union legislation or ... to regulation at national level'"),
    "A-32012R0648-r11": ("REASONED", "'Consequently, and in order to prevent the possible creation of parallel sets of rules'"),
    "A-32021R1119-r9": ("REASONED", "'In light of this' resuming the aims set out in the first sentence"),
    "A-32009R1223-r26": ("REASONED", "'in order to be allowed for these uses'; and the general principle of manufacturer responsibility as the premise"),
    "A-32013R1308-r77": ("REASONED", "'In order to adapt the definitions and sales descriptions ... to needs resulting from evolving consumer demands'"),
}

# ---- Sample B: Family A precision.  EXHORTATION | DESCRIPTIVE | OTHER ----------------------------
SAMPLE_B = {
    "B-13": ("DESCRIPTIVE", "'would be expected to be considered assets of extremely high liquidity' -- a forecast, no party urged"),
    "B-50": ("DESCRIPTIVE", "'a high number of connected digital devices are expected to be deployed' -- a forecast about the world"),
    "B-48": ("EXHORTATION", "'Data controllers should be encouraged to develop interoperable formats'"),
    "B-14": ("EXHORTATION", "'the Commission ... is invited to make a legislative proposal' -- and it is in an ARTICLE, not a recital"),
    "B-03": ("OTHER", "'could reasonably be expected to foresee' -- a foreseeability standard"),
    "B-75": ("OTHER", "inside a definition: 'the maximum amount that is expected to be paid on average'"),
    "B-33": ("OTHER", "'can reasonably be expected to be able to have a significant effect' -- a capacity standard"),
    "B-101": ("OTHER", "procedural provision on harmonised standards; the pattern has misread it"),
    "B-76": ("EXHORTATION", "'public sector bodies are encouraged to develop a harmonised approach'"),
    "B-11": ("EXHORTATION", "'Institutions should be encouraged to move towards the more risk-sensitive approaches'"),
    "B-71": ("DESCRIPTIVE", "'Actions under the CAP are expected to contribute 40 %' -- a stated expectation, not an urging"),
    "B-12": ("DESCRIPTIVE", "'The Basel III framework is expected to significantly increase the own fund requirements'"),
    "B-27": ("OTHER", "'the number of suitable candidates to be invited to participate' -- an infinitive inside a noun phrase"),
    "B-43": ("OTHER", "'person who can reasonably be expected to possess' -- a knowledge standard"),
    "B-94": ("OTHER", "'The data holder cannot be expected to store the data indefinitely' -- negated, and the stop list did not catch it because \\bnot\\b does not match inside 'cannot'"),
    "B-20": ("EXHORTATION", "'contracting authorities should be encouraged to appoint a project leader'"),
    "B-28": ("OTHER", "same construction as B-27"),
    "B-41": ("EXHORTATION", "'competent authorities should be encouraged to ensure that the rating is based on the outcome of several official controls'"),
    "B-05": ("OTHER", "'can reasonably be expected to have been aware of' -- a knowledge standard"),
    "B-68": ("DESCRIPTIVE", "'emissions that are expected to be emitted in that period' -- a projection"),
    "B-62": ("DESCRIPTIVE", "'whether the plan is expected to contribute' -- an assessment criterion phrased as a forecast"),
    "B-35": ("OTHER", "'may reasonably be expected to come into existence' -- part of the definition of precise information"),
    "B-107": ("EXHORTATION", "'The providers however are encouraged to consider such additional training measures'"),
    "B-37": ("EXHORTATION", "'Data controllers should be encouraged to develop interoperable formats' -- GDPR r68"),
    "B-56": ("EXHORTATION", "'Member States should be encouraged to foster synergies with recovery and resilience plans of other Member States'"),
    "B-51": ("EXHORTATION", "'Organisations, manufacturers or providers ... should be encouraged to implement measures' -- the extracted addressee 'ICT processes should' is WRONG"),
    "B-22": ("EXHORTATION", "'Contracting authorities should be encouraged to make use of the Code of Best Practices'"),
    "B-102": ("OTHER", "same construction as B-101"),
    "B-106": ("EXHORTATION", "'All stakeholders, including industry, academia, civil society and standardisation organisations, are encouraged to take into account ... the ethical principles' -- the purest political exhortation in the sample"),
    "B-40": ("EXHORTATION", "'Controllers and processors should be encouraged to provide additional safeguards' -- extracted addressee 'processors should' drops 'Controllers and'"),
    "B-00": ("OTHER", "'may reasonably be expected to be known to him' -- a knowledge standard"),
    "B-99": ("DESCRIPTIVE", "'when the data are expected to be erased' -- a forecast inside a disclosure duty"),
    "B-34": ("OTHER", "same as B-35"),
    "B-67": ("DESCRIPTIVE", "'whether the arrangements ... are expected to prevent, detect and correct corruption'"),
    "B-44": ("OTHER", "same knowledge standard as B-43"),
    "B-82": ("EXHORTATION", "'it should be encouraged to accept orders in the same language' -- extracted addressee is the bare pronoun 'it should'"),
    "B-66": ("DESCRIPTIVE", "'whether the arrangements ... are expected to ensure an effective monitoring'"),
    "B-115": ("EXHORTATION", "'Providers of high-risk AI systems are encouraged to start to comply, on a voluntary basis'"),
    "B-47": ("OTHER", "'the Executive Director may be invited to make a statement' -- a competence provision, not an urging"),
    "B-45": ("OTHER", "'the candidate ... shall be invited to make a statement' -- an ENACTED obligation, which §4b excludes by definition"),
}

# Attribution: among the EXHORTATION rows, is the addressee the instrument extracted the right one?
ATTRIBUTION_WRONG = {
    "B-14": "extracted a 62-word run-up ending 'and'; the party is the Commission",
    "B-51": "extracted 'ICT processes should'; the party is organisations, manufacturers or providers",
    "B-40": "extracted 'processors should'; the party is controllers AND processors",
    "B-82": "extracted the bare pronoun 'it should'; the party is the provider of intermediary services",
}

# ---- Sample C: recall.  MISSED | CLEAN -----------------------------------------------------------
SAMPLE_C = {
    "C-32014L0024-r35": ("MISSED", "'The co-financing of research and development (R&D) programmes by industry sources should be encouraged.' -- an exhortation with NO addressee and no infinitive, so Family A, which requires 'encouraged to', cannot see it"),
}
SAMPLE_C_DEFAULT = ("CLEAN", "no modal-free exhortation; the normative content present carries should/shall/may or is a statement of fact, a definition or a legal premise")

# Observations recorded during sample C that are NOT verdict changes, because the pre-registered
# verdict asks only about exhortation.  They are the reason the work reports a residue probe.
SAMPLE_C_NOTES = {
    "C-32010L0075-r28": "'it is necessary for the Commission to review the need to establish the most suitable controls' -- modal-free DIRECTED normative content with a named party.  Not exhortation, so CLEAN, but it is the class Session 82's rule and tonight's Family A both miss.",
    "C-32014L0024-r123": "'environmental, social and innovation procurement will also have to play its part' -- hortatory in tone, but 'have to' is a deontic expression, so it is outside the modal-free class by the definition fixed in advance.",
    "C-32023R2854-r111": "'the Commission should develop and recommend non-binding model contractual terms' -- an instruction to produce a non-binding instrument, which is a third thing again.",
}
