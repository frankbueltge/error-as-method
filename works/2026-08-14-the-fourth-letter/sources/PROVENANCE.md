# Provenance of the passages that could not be cut here

Every other quotation in `work.md` was sliced out of a file `harvest.py` downloaded and
hashed, by `evidence.py`, and lives in this directory as a `.txt`. Three sources could not
be handled that way. This file says exactly how they were obtained, so the difference
between "cut from bytes I hold" and "read through a service" stays visible in the record
rather than being flattened into a footnote.

## 1 · `www.iso.org` — HTTP 403 to this host

`harvest.py` requests two ISO pages and both fail; `MANIFEST.json` records the failure
rather than hiding it:

    iso_org_country_codes   https://www.iso.org/iso-3166-country-codes.html   -> HTTP 403
    iso_org_3166_3          https://www.iso.org/standard/63547.html           -> HTTP 403

The passages below were retrieved on 2026-08-14 through a server-side extraction service,
which reaches the pages this host cannot. They are ISO's own free text — the standards
themselves are paywalled and were **not** read. Anyone can check them by opening the two
URLs in a browser.

From <https://www.iso.org/iso-3166-country-codes.html>:

> The formerly used codes are four-letter codes (alpha-4). How the alpha-4 codes are
> constructed depends on the reason why the country name has been removed.

> Part 3 establishes a code that represents non-current country names, i.e. the country
> names deleted from ISO 3166 since its first publication in 1974, for example, Yugoslavia
> or Czechoslovakia.

> Even if all criteria are met, the ISO 3166 Maintenance Agency may decide not to assign a
> code element, for example, due to the very limited number of official alpha-2 code
> elements available.

From <https://www.iso.org/standard/63547.html> (the catalogue entry for ISO 3166-3:2013,
abstract and life-cycle block):

> ISO 3166-3:2013 provides principles and maintenance arrangements of a code for the
> representation of country names removed from editions 1 to 7 of ISO 3166 and the
> subsequent editions of ISO 3166-1.
>
> Clauses 8 and 9 contain lists of all formerly used country names removed from ISO 3166
> (now ISO 3166-1) since 1974, together with the code element for each one of them.

> Life cycle · Previously: Withdrawn — ISO 3166-3:1999 · Now: Withdrawn — ISO 3166-3:2013
> · New version available: ISO 3166-3:2020

The first edition is therefore **ISO 3166-3:1999**; the register did not exist before it.

From <https://www.iso.org/glossary-for-iso-3166.html>:

> Alpha-4 code – a four-letter code that represents a country name that is no longer in
> use. The structure depends on the reason why the country name was removed from ISO
> 3166-1 and added to ISO 3166-3.

> Transitionally reserved codes – codes that are reserved during a transitional period
> while new code elements that may replace them are taken into use.

## 2 · The ISO 3166/MA's reserved-code list of 2003-07-28 — a PDF this host cannot read

`harvest.py` downloads and hashes the PDF itself (94,321 bytes; SHA-256 in
`MANIFEST.json`), from the Hong Kong government's mirror of the ISO 3166/MA document:

    https://www.digitalpolicy.gov.hk/en/our_work/data_governance/policies_standards/
    interoperability_framework/common_schemas/doc/
    ISO_3166-1_List_of_reserved_code_elements_(2003-07-28).pdf

Its text could **not** be extracted here: the environment has no working PDF text
extractor (`pdftotext` absent; `pypdf` fails to import against a broken `cryptography`
build), and a hand-written stream decoder recovered 141 bytes of the file. The passages
below came through the same server-side extraction service, on 2026-08-14:

> **1.1 Transitional reservations.** Code elements which the ISO 3166/MA has altered or
> deleted from the 1988 and 1993 versions of ISO 3166-1 will not be reallocated during a
> period of at least five years after the change. The exact period is determined in each
> case on the basis of the extent to which the former code element was used (7.4.1 of ISO
> 3166-1:1997). Such code elements may be used only during a transitional period while new
> code elements that may have replaced them are taken into use. No other use of
> transitionally reserved code elements is allowed; they may be reallocated by the ISO
> 3166/MA after the expiration of the transitional period.

> **Table 1: Transitionally reserved alpha-2 code elements** — BU Burma 1989-12 · NT
> Neutral Zone 1993-07 · SF Finland 1995-09 · SU USSR 1992-09 · TP East Timor 2002-05 · YU
> Yugoslavia 2003-07 · ZR Zaire 1997-07

> **Table 2: Transitionally reserved alpha-3 code elements** — BUR Burma 1989-12 · BYS
> Byelorussian SSR 1992-06 · CSK Czechoslovakia 1993-06 · NTZ Neutral Zone 1993-07 · ROM
> Romania 2002-02 · SUN USSR 1992-09 · TMP East Timor 2002-05 · YUG Yugoslavia 2003-07 ·
> ZAR Zaire 1997-07

This is a mirror, not ISO's own server, and it is dated: it is the list as it stood on
2003-07-28, five days after ISO reassigned `CS` to Serbia and Montenegro on 2003-07-23.
The work uses it for exactly one thing — that `CSK` appears in Table 2 and `CS` does not
appear in Table 1 — and that asymmetry is independently confirmed by the join in
`join-31-dead-codes.txt`, where `CSK` is still unassigned in ISO 3166-1 today while `CS`
was reassigned and then withdrawn again.

## 3 · What this means for the argument

If the extraction service misquoted any of the above, the work's *measured* results are
untouched — they come from files hashed in `MANIFEST.json` and joined offline by
`measure.py`. What would fall is the *explanation*: ISO's own statement that alpha-2 codes
are scarce, and its own rule that a withdrawn code may be reallocated after a transitional
period. Both are checkable in one click by anyone whose network is not walled off from
`iso.org`, which is why they are quoted with their URLs rather than paraphrased.
