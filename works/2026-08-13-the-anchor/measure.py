#!/usr/bin/env python3
"""
The Anchor — measurement script.

Reads only the files committed under ./sources/ (harvested 2026-08-13, SHA-256 in
MANIFEST.json). No network access at run time. No randomness, therefore no seed.
Standard library only.

WHAT THIS MEASURES.  The night's question is where an institution that repairs its
norm in place nevertheless freezes.  The WHATWG publishes Living Standards: no
version numbers, no errata list, corrections applied to the normative text itself.
Chapter 16 of the HTML Living Standard is the place where that institution keeps
what it has judged wrong.  The script counts that population and, separately,
counts the freeze mechanisms the WHATWG's own policy documents install and the
external attachment each one names.

THE LEDGER.  Predictions are written below, before the first execution, in the
house form.  Two kinds are distinguished, because honesty about which is which is
the point of keeping a ledger at all:

  OBSERVED DURING HARVEST — facts already seen while deciding whether the source
  was worth committing.  These are NOT predictions and are not scored.  Recording
  them as predictions would be the defect session 48 confessed to: an apparatus
  emitting well-formed output with nothing under it.

  PREDICTED — not computed before the run.  These are scored.

P1  Of the 28 non-conforming elements listed in section 16.2, at least 24 are
    named again in section 16.3 with normative requirements addressed to
    implementations.                                                    [scored]
P2  Section 16.3 (Requirements for implementations) exceeds sections 16.1 and
    16.2 combined, in words, by a factor of at least 2.                 [scored]
P3  At least 15 distinct IDL interface definitions are preserved in chapter 16
    for features the same chapter forbids.                              [scored]
P4  In chapter 16, tokens of preservation-for-the-outside ("historical",
    "legacy", "compatibility", "compat") outnumber occurrences of the phrase
    "must not be used by authors".                                      [scored]
P5  At least 25 of the 28 obsolete elements carry a stated successor — either a
    "Use X instead" in 16.2 or a "in a manner equivalent to X" in 16.3. [scored]
P6  THE SECOND REPRESENTATION.  Session 49 concluded that the only error
    detector this practice has found that works is the same fact printed twice
    in two notations.  So: the count of obsolete elements taken from 16.2's
    definition list, and the count taken independently from the IDL interface
    blocks and implementation sentences of 16.3, differ by no more than 4.
    A larger gap means one of the two parses is wrong and the chapter's own
    structure says so.                                                  [scored]
P7  In the W3C Process Document, at least 2 of the 4 withdrawal statuses
    (rescind, obsolete, supersede, restore) are defined in a passage that also
    names the Patent Policy or what implementers may rely on.           [scored]

P8  ADDED AFTER THE FIRST RUN, AND WRITTEN BEFORE THE PAGES IT TESTS WERE
    FETCHED.  The first run refuted P1: only 9 of the 28 condemned elements are
    named again in section 16.3.  That leaves 19 the chapter forbids without
    specifying anything for implementations — which would mean the WHATWG really
    does remove, and that the residue of a removal is a prohibition rather than
    a preserved specification.  Before believing that, the claim has to be
    checked against the rest of the standard, because chapter 16 is not the
    standard.  So, predicted before `rendering.html` and `parsing.html` were
    harvested: at least 15 of those 19 receive normative treatment somewhere in
    the rendering or parsing sections, i.e. "unspecified" is a property of the
    chapter and not of the standard.                                    [scored]

THE ERROR IN THE FIRST RUN, kept rather than tidied away.  The first execution
reported P5 REFUTED at 13 of 28.  That was my parser, not the document: this
definition list groups several <dt> terms under one shared <dd> (basefont, big,
blink, center, font, marquee, multicol, nobr and spacer all share a single "Use
CSS instead"), and `dl_pairs` attached the definition only to the last term of
each group.  Corrected below by grouping consecutive terms; the wrong first
figure is recorded here rather than replaced silently.  It was catchable only
because the list of elements *without* a successor was printed next to the list
of elements *with* one, and reading the two together made the grouping visible —
the same detector as P6, and the same one session 49 ended on.

A THIRD DISAGREEMENT BETWEEN TWO REPRESENTATIONS, resolved by looking.  P8's six
elements are reported here as absent from the rendering and parsing sections.  A
raw substring grep of the same two files disagrees: it finds `blink` twice in the
parsing section and `multicol` three times in the rendering section.  Inspected:
every one of those five hits is inside markup rather than prose — `class=
"edge_blink"` in a browser-support widget, and the URL `drafts.csswg.org/
css-multicol/` in a citation of a CSS property.  `strip_tags` removes attribute
values, so the count computed here is the count of occurrences in normative text,
which is what the claim is about, and the raw grep is the misleading one.  Stated
rather than left implicit, because the two numbers differ and a reader is owed
the reason.

OBSERVED DURING HARVEST, not scored: the count 28 for obsolete elements and 143
for obsolete attributes; the byte offset of section 16.3; the review-draft
directory listing and its cadence.  All are recomputed here so the numbers in the
work are produced by this script and not by a shell session, but they are marked
`observed` in results.json and no credit is claimed for them.
"""

import hashlib
import html
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "sources")

OBSOLETE = "html_spec_whatwg_org_multipage_obsolete_html.html"
FAQ = "whatwg_org_faq.html"
WORKING_MODE = "whatwg_org_working-mode.html"
WORKSTREAM = "whatwg_org_workstream-policy.html"
DRAFTS = "html_spec_whatwg_org_review-drafts-index.html"
W3C_PROCESS = "www_w3_org_policies_process-index.html"
RENDERING = "html_spec_whatwg_org_multipage_rendering_html.html"
PARSING = "html_spec_whatwg_org_multipage_parsing_html.html"


def read(name):
    with open(os.path.join(SRC, name), encoding="utf-8", errors="replace") as f:
        return f.read()


def sha256(name):
    with open(os.path.join(SRC, name), "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def strip_tags(s):
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s))).strip()


def words(s):
    return len(strip_tags(s).split())


# ---------------------------------------------------------------- chapter 16

def sections(doc):
    """Split the obsolete-features chapter at its three published section ids."""
    ids = [
        "obsolete-but-conforming-features",
        "non-conforming-features",
        "requirements-for-implementations",
    ]
    pos = [doc.find("id=" + i) for i in ids]
    if min(pos) < 0:
        raise SystemExit("section anchors not found — the page structure changed")
    if pos != sorted(pos):
        raise SystemExit("sections out of document order — parse assumption broken")
    return {
        "16.1": doc[pos[0]:pos[1]],
        "16.2": doc[pos[1]:pos[2]],
        "16.3": doc[pos[2]:],
    }


def dl_after(doc, phrase):
    """Return the <dt> terms of the first definition list following `phrase`."""
    i = doc.find(phrase)
    if i < 0:
        raise SystemExit("phrase not found: " + phrase)
    m = re.search(r"<dl>(.*?)</dl>", doc[i:], re.S)
    terms = re.findall(r"<dt>(.*?)(?=<dt>|<dd>|</dl>)", m.group(1), re.S)
    return [strip_tags(t) for t in terms]


def dl_pairs(doc, phrase):
    """Return (term, definition) pairs of the first definition list after `phrase`.

    Consecutive <dt> terms share the <dd> block that follows them — the first
    version of this function did not, and reported 13 of 28 elements as having no
    stated successor when the true figure is larger (see the note in the module
    docstring).  Terms are accumulated until a definition appears, then the
    definition is attached to every term in the group.
    """
    i = doc.find(phrase)
    m = re.search(r"<dl>(.*?)</dl>", doc[i:], re.S)
    body = m.group(1)
    tokens = re.findall(r"<(dt|dd)>(.*?)(?=<dt>|<dd>|</dl>|$)", body, re.S)
    out, pending = [], []
    for kind, text in tokens:
        if kind == "dt":
            pending.append(strip_tags(text))
        else:
            definition = strip_tags(text)
            for term in pending:
                out.append((term, definition))
            pending = []
    for term in pending:                      # trailing terms with no definition
        out.append((term, ""))
    return out


def main():
    obsolete = read(OBSOLETE)
    sec = sections(obsolete)

    # --- the condemned population (observed during harvest, recomputed here)
    elements = dl_after(obsolete, "Elements in the following list are entirely obsolete")
    element_pairs = dl_pairs(obsolete, "Elements in the following list are entirely obsolete")
    attributes = dl_after(obsolete, "The following attributes are obsolete")

    # --- P1: how many of the condemned elements are still specified to implementers
    s3 = sec["16.3"]
    s3_text = strip_tags(s3)
    named_in_163 = []
    for e in elements:
        # the element name as a standalone token in the implementation section
        if re.search(r"\b" + re.escape(e) + r"\b", s3_text):
            named_in_163.append(e)

    # --- P2: the word shares of the three sections
    w1, w2, w3 = words(sec["16.1"]), words(sec["16.2"]), words(sec["16.3"])

    # --- P3: IDL interfaces preserved in the chapter
    idl = sorted(set(re.findall(r"interface\s+(HTML[A-Za-z]*Element|[A-Z][A-Za-z]+)\s*[:{]",
                                strip_tags(obsolete))))
    idl_partial = sorted(set(re.findall(r"partial interface\s+([A-Za-z]+)", strip_tags(obsolete))))

    # --- P4: the vocabulary of preservation
    chap_text = strip_tags(obsolete)
    keep_tokens = {t: len(re.findall(t, chap_text, re.I))
                   for t in ["historical", "legacy", "compatibilit", "compat"]}
    forbid_phrase = len(re.findall(r"must not be used by authors", chap_text))

    # --- P5: does the chapter name a successor for each condemned element
    with_successor = [e for e, d in element_pairs
                      if re.search(r"\bUse\b|\binstead\b|\bequivalent to\b", d)]

    # --- P6: the second representation. Count the obsolete elements a second way,
    #         from the implementation section's own structure, and compare.
    #     Route B: element names that carry a preserved IDL interface or an explicit
    #     "User agents must treat X elements" sentence in 16.3.
    ua_treat = sorted(set(re.findall(r"User agents must treat ([a-z0-9]+) elements", s3_text)))
    idl_elements = sorted(set(re.findall(r"interface HTML([A-Za-z]+)Element", strip_tags(obsolete))))
    route_b = sorted(set(ua_treat) | {e for e in elements
                                      if e.capitalize() in [i for i in idl_elements]})
    # the honest comparison is between the two element counts
    route_a_n, route_b_n = len(elements), len(set(ua_treat) | set(named_in_163))

    # --- P8: the second apparatus. Chapter 16 is not the standard. Do the elements
    #     the chapter forbids without specifying get specified anywhere else?
    unspecified_in_16_3 = [e for e in elements if e not in named_in_163]
    rendering_t = strip_tags(read(RENDERING))
    parsing_t = strip_tags(read(PARSING))
    elsewhere = {}
    for e in unspecified_in_16_3:
        pat = r"\b" + re.escape(e) + r"\b"
        elsewhere[e] = {
            "rendering": len(re.findall(pat, rendering_t)),
            "parsing": len(re.findall(pat, parsing_t)),
        }
    specified_elsewhere = [e for e, c in elsewhere.items()
                           if c["rendering"] + c["parsing"] > 0]
    truly_absent = [e for e in unspecified_in_16_3 if e not in specified_elsewhere]

    # --- the freeze census: mechanisms and the outside each one names
    faq, wm, wsp = read(FAQ), read(WORKING_MODE), read(WORKSTREAM)
    faq_t, wm_t, wsp_t = strip_tags(faq), strip_tags(wm), strip_tags(wsp)

    def find_sentence(text, needle, before=0, after=340):
        i = text.find(needle)
        return text[max(0, i - before):i + after] if i >= 0 else None

    freeze = [
        {
            "mechanism": "Review Draft",
            "cadence": "roughly every six months",
            "outside_it_serves": "patent review by Workstream Participants",
            "evidence": find_sentence(faq_t, "roughly every six months"),
            "source": "whatwg.org/faq",
        },
        {
            "mechanism": "commit snapshot",
            "cadence": "one per change to the standard",
            "outside_it_serves": "implementers documenting what they implemented from",
            "evidence": find_sentence(faq_t, "each change to the standard"),
            "source": "whatwg.org/faq",
        },
        {
            "mechanism": "anchor permanence",
            "cadence": "continuous",
            "outside_it_serves": "other standards referencing parts of the standard",
            "evidence": find_sentence(wm_t, "Often other standards want to reference"),
            "source": "whatwg.org/working-mode",
        },
    ]
    discouragement = find_sentence(
        wm_t, "other standards organizations are discouraged", before=200)
    draft_notice = find_sentence(
        wsp_t, "This is the Review Draft.", after=430)
    repair_stance = find_sentence(
        faq_t, "Instead of ignoring what the browsers do", after=120)
    stability = find_sentence(
        faq_t, "they endeavor to eliminate all of their bugs", before=260, after=90)

    # --- the review-draft series
    drafts = sorted(set(re.findall(r"(20\d\d-\d\d)/", read(DRAFTS))))
    off_cadence = [d for d in drafts if d.split("-")[1] not in ("01", "07")]

    # --- P7: W3C withdrawal statuses and what defines them
    w3c = strip_tags(read(W3C_PROCESS))
    statuses = {}
    for word in ["rescind", "obsolete", "supersede", "restor"]:
        hits = [m.start() for m in re.finditer(word, w3c, re.I)]
        tied = 0
        for h in hits:
            window = w3c[max(0, h - 400):h + 400]
            if re.search(r"Patent Policy|licens", window, re.I):
                tied += 1
        statuses[word] = {"mentions": len(hits), "within_400ch_of_patent_or_licence": tied}
    tied_statuses = sum(1 for v in statuses.values()
                        if v["within_400ch_of_patent_or_licence"] > 0)
    rescind_rule = None
    i = w3c.find("only rescinds, supersedes, or obsoletes entire Recommendations")
    if i >= 0:
        rescind_rule = w3c[i - 10:i + 260]

    # ---------------------------------------------------------------- ledger
    ledger = [
        ("P1", "≥ 24 of the 28 condemned elements are named again in 16.3",
         len(named_in_163) >= 24, f"{len(named_in_163)} of {len(elements)}"),
        ("P2", "16.3 exceeds 16.1+16.2 in words by a factor of ≥ 2",
         w3 >= 2 * (w1 + w2), f"{w3} vs {w1 + w2} — factor {w3 / max(1, w1 + w2):.2f}"),
        ("P3", "≥ 15 distinct IDL interfaces preserved in chapter 16",
         len(idl) + len(idl_partial) >= 15,
         f"{len(idl)} full + {len(idl_partial)} partial = {len(idl) + len(idl_partial)}"),
        ("P4", "preservation vocabulary outnumbers 'must not be used by authors'",
         sum(keep_tokens.values()) > forbid_phrase,
         f"{sum(keep_tokens.values())} vs {forbid_phrase}"),
        ("P5", "≥ 25 of 28 condemned elements carry a stated successor",
         len(with_successor) >= 25, f"{len(with_successor)} of {len(elements)}"),
        ("P6", "the two independent element counts differ by ≤ 4",
         abs(route_a_n - route_b_n) <= 4,
         f"route A (16.2 list) {route_a_n}; route B (16.3 structure) {route_b_n}; "
         f"gap {abs(route_a_n - route_b_n)}"),
        ("P7", "≥ 2 of 4 W3C withdrawal statuses sit within 400 characters of "
               "the Patent Policy or of licensing",
         tied_statuses >= 2, f"{tied_statuses} of 4"),
        ("P8", "≥ 15 of the elements unspecified in 16.3 are specified in the "
               "rendering or parsing sections instead",
         len(specified_elsewhere) >= 15,
         f"{len(specified_elsewhere)} of {len(unspecified_in_16_3)}; "
         f"absent from all three sections: {truly_absent or 'none'}"),
    ]

    print("=" * 78)
    print("THE ANCHOR — measurement, 2026-08-13")
    print("=" * 78)
    print("\nSOURCES (SHA-256 of the committed copy)")
    manifest = {}
    for n in [OBSOLETE, FAQ, WORKING_MODE, WORKSTREAM, DRAFTS, W3C_PROCESS,
              RENDERING, PARSING]:
        h = sha256(n)
        manifest[n] = h
        print(f"  {h[:16]}…  {n}")

    print("\n1. THE CONDEMNED POPULATION (observed during harvest, recomputed here)")
    print(f"  elements entirely obsolete, 'must not be used by authors' : {len(elements)}")
    print(f"  attributes obsolete, elements still in the language       : {len(attributes)}")
    print(f"  total features the standard judges wrong and keeps        : "
          f"{len(elements) + len(attributes)}")

    print("\n2. WHAT THE CHAPTER SPENDS ITS WORDS ON")
    tot = w1 + w2 + w3
    for k, w in (("16.1 obsolete but conforming", w1),
                 ("16.2 non-conforming (the prohibition)", w2),
                 ("16.3 requirements for implementations", w3)):
        print(f"  {k:<42} {w:>7} words  {100 * w / tot:5.1f}%")

    print("\n3. THE FREEZE CENSUS — mechanism : the outside it serves")
    for f in freeze:
        print(f"  {f['mechanism']:<20} : {f['outside_it_serves']}")
    print(f"  review drafts published: {len(drafts)}  "
          f"({drafts[0]} … {drafts[-1]}), off-cadence: {off_cadence or 'none'}")

    print("\n4. LEDGER")
    confirmed = 0
    for tag, claim, ok, detail in ledger:
        print(f"  {tag} {'CONFIRMED' if ok else 'REFUTED  '}  {claim}")
        print(f"      {detail}")
        confirmed += bool(ok)
    print(f"\n  {confirmed} confirmed, {len(ledger) - confirmed} refuted, of {len(ledger)}")

    results = {
        "date": "2026-08-13",
        "work": "The Anchor",
        "no_network_at_run_time": True,
        "no_randomness_therefore_no_seed": True,
        "manifest_sha256": manifest,
        "observed_during_harvest_not_scored": {
            "obsolete_elements": len(elements),
            "obsolete_attributes": len(attributes),
            "review_drafts": len(drafts),
            "review_draft_range": [drafts[0], drafts[-1]] if drafts else [],
            "review_drafts_off_cadence": off_cadence,
        },
        "section_words": {"16.1": w1, "16.2": w2, "16.3": w3},
        "elements": elements,
        "elements_named_in_16_3": named_in_163,
        "elements_with_successor": with_successor,
        "attributes": attributes,
        "idl_interfaces": idl,
        "idl_partial_interfaces": idl_partial,
        "preservation_vocabulary": keep_tokens,
        "must_not_be_used_by_authors_occurrences": forbid_phrase,
        "second_representation": {
            "route_a_from_16_2_list": route_a_n,
            "route_b_from_16_3_structure": route_b_n,
            "gap": abs(route_a_n - route_b_n),
            "ua_must_treat": ua_treat,
        },
        "freeze_census": freeze,
        "quotations": {
            "repair_stance": repair_stance,
            "stability": stability,
            "snapshots_discouraged": discouragement,
            "review_draft_notice": draft_notice,
            "w3c_rescind_rule": rescind_rule,
        },
        "w3c_withdrawal_statuses": statuses,
        "elements_unspecified_in_16_3": unspecified_in_16_3,
        "elements_specified_elsewhere": elsewhere,
        "elements_absent_from_all_three_sections": truly_absent,
        "ledger": [{"id": t, "claim": c, "confirmed": bool(o), "detail": d}
                   for t, c, o, d in ledger],
    }
    with open(os.path.join(HERE, "results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print("\nwrote results.json")


if __name__ == "__main__":
    main()
