# The two that beats the one: first digits of house prices in England and Wales

## Material

- Publisher: HM Land Registry
- Dataset: Price Paid Data, monthly update file ("new version" format), England and Wales
- URL: http://prod.publicdata.landregistry.gov.uk.s3-website-eu-west-1.amazonaws.com/pp-monthly-update-new-version.csv
  (download page: https://www.gov.uk/government/statistical-data-sets/price-paid-data-downloads)
- Licence: Open Government Licence v3.0, as given for Price Paid Data on the GOV.UK download page
  (the CSV itself carries no licence text; I did not re-open the page on the day of fetching)
- Fetched: 2026-10-22
- Column given to the instrument: `price_gbp`
- Preparation: the file has no header and 90,867 rows (transaction dates 1995-01-12 to 2026-08-28,
  mostly 2026). I kept only records with status `A` (added; dropped 3,095 `C` changes and 1,488 `D`
  deletions), and of each record only price, date (day part), property type, new-build flag, tenure,
  PPD category and record status; addresses, postcodes and transaction IDs were dropped. Result:
  `price_paid.csv`, 86,284 rows, 2.5 MB. The original download was deleted afterwards.

## Runs

1. `python3 instrument.py price_paid.csv --column price_gbp` — succeeded; wrote reading.svg and reading.json.

## What the instrument showed

All 86,284 prices were read. The first digits are far from Benford (chi-square 10,363 with 8 df, mean
absolute deviation 0.035): 2 is the most common first digit (25.6%, Benford 17.6%), narrowly ahead of 1
(24.6%, which is *below* Benford's 30.1%), and 3 is in clear excess (18.6% against 12.5%); from 5 upward
every digit is under-represented, 9 at about half its expected share. This is roughly what I expected: the
prices live mostly within one decade (median £290,000), so the digits of that decade's bulk, 2 and 3,
take over. What I had not quite anticipated is that 1 actually falls short of Benford even though the
counts of all digits from 1 to 4 are inflated as a group; the shape is a hump over 2 rather than a steeper
Benford curve.
