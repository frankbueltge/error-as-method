# The missing tens of thousands: Defra's £25,000 register against Benford

## Material

- Publisher: Department for Environment, Food & Rural Affairs (Defra), UK Government, on GOV.UK.
- Dataset: "Defra: spending over £25,000", the twelve monthly transparency CSVs for January–December 2025.
- URL: https://www.gov.uk/government/collections/defra-departmental-spending-over-25000
  (file URLs found through the GOV.UK content API, e.g.
  https://assets.publishing.service.gov.uk/media/6ad87ecbb63982f71c3bd348/January_25_Over_25K.csv ...
  https://assets.publishing.service.gov.uk/media/6ac6233ce635a394acb92388/Over__25K_Dec_25.csv).
- Licence: Open Government Licence v3.0, as GOV.UK states for its content "except where otherwise stated";
  the publication pages state nothing otherwise.
- Fetched: 2026-10-22.
- Column given to the instrument: `amount_gbp`.
- Preparation: read each monthly file as Windows-1252 (the £ sign is byte 0xA3); fixed the January
  header's first cell ("DEFRApartment"); December has an extra leading "Comments" column, so columns were
  taken by name. Kept month, entity, date, expense type, supplier and amount; stripped "£" and thousands
  separators from Amount and turned leading "-" or brackets into a negative sign. All 14,268 rows
  parsed; nothing else was removed. Result: `defra_spend_over_25k_2025.csv` (1.7 MB). The raw downloads
  were deleted after combining.

## Runs

1. `python3 instrument.py defra_spend_over_25k_2025.csv --column amount_gbp` — succeeded; 14,264
   numbers, 4 skipped (zero amounts). MAD 0.0209, chi-square 666.5 (8 df).

## What the instrument showed

The first digit 1 falls to 22.4% against Benford's 30.1%, and the shortfall is taken up mostly by 3
(16.9% vs 12.5%) and 4 (12.1% vs 9.7%), with 5 also above; 7, 8 and 9 sit slightly below. That the 1s
collapse was what I expected from the £25,000 cut, which removes the 10,000–24,999 band. What I did not
expect is that 2 is barely raised (18.3% vs 17.6%): the payments just above the threshold do not pile up
the way I guessed (25,000–29,999 holds only 9.9% of amounts), and the excess sits instead in the 30,000s
and 40,000s. The register is unmistakably non-Benford (chi-square 666), but the deviation is a clean
signature of the publication rule rather than of anything in the payments themselves.
