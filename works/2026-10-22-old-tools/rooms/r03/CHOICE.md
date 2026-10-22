# First to mind

1. Populations of municipalities in a country (e.g. German Gemeinden from Destatis).
2. Government spending transactions published under a transparency rule (e.g. UK departments' "spend over £25,000" files).
3. Prices of items in an open product database (e.g. Open Food Facts or a museum's acquisition prices).

# Chosen

Defra (UK Department for Environment, Food & Rural Affairs): spending over £25,000, the twelve monthly
transparency files for January to December 2025, combined into one CSV (column `amount_gbp`).
Found via the collection https://www.gov.uk/government/collections/defra-departmental-spending-over-25000
(each month's file on assets.publishing.service.gov.uk; e.g.
https://assets.publishing.service.gov.uk/media/6ad87ecbb63982f71c3bd348/January_25_Over_25K.csv).

How I came to it: the instrument is a Benford first-digit counter, and the second of my first three
thoughts, a government "spend over £25,000" register, is a material where a publication rule cuts the
distribution at a fixed threshold. A web search for "data.gov.uk department spending over £25,000 csv"
led to the Defra files; I took one department and one calendar year so the material is one coherent body.

# Expected

Because nothing under £25,000 is published, the band 10,000–24,999 that normally supplies many 1s and 2s
is missing, so I expect digit 1 to fall well below Benford's 30.1% and digits 2–4 to be over-represented,
with a large chi-square. Digit 2 may be especially inflated by the many payments just above £25,000.
