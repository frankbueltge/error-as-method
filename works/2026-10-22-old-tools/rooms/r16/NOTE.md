# A Lake's Winters, One After Another

## Material

- **Publisher:** Wisconsin State Climatology Office, Nelson Institute for Environmental Studies, University of Wisconsin-Madison (the same record is kept by the North Temperate Lakes LTER and published on the Environmental Data Initiative portal, which refused public download when I tried).
- **Dataset:** History of Ice Freezing and Thawing on Lake Mendota, winters 1852-53 to 2025-26 (freeze-over date, thaw date, days of ice cover).
- **URL:** https://climatology.nelson.wisc.edu/first-order-station-climate-data/madison-climate/lake-ice/history-of-ice-freezing-and-thawing-on-lake-mendota/
- **Licence:** none stated on the page as I found it; it is a public web page of a state university office.
- **Fetched:** 2026-10-22.
- **Column given to the instrument:** `ice_days` (days of ice cover in the winter).
- **Preparation:** I extracted the HTML table (182 rows: Winter, Freeze-Over Date, Thaw Date, Days of Ice Cover) into `mendota_ice.csv` with columns `winter, freeze_over, thaw, ice_days`. The page lists newest winter first; I reversed the row order so the file runs from 1852-53 to 2025-26. Dashes for missing dates were replaced by empty cells. Winters in which the lake froze and opened more than once have several rows; the page gives the winter's total days on only one of them, so the other rows have an empty `ice_days` and are skipped by the instrument (as are the early winters with no total). Nothing else was changed.

## Runs

1. `python3 instrument.py mendota_ice.csv --column ice_days` -> n = 171, 11 cells skipped, min 21, max 161. This is the reading.

## What it showed

The line is one long, ragged sawtooth of 171 winters between 21 and 161 days. The decline I expected is there, but not as a steady drift: the first twenty-odd winters (1850s-1870s) are high and wild, including the 161-day winter of 1880-81 at the top; then for roughly a century, from the 1880s to the 1970s, the line wanders around a level of about 100-106 days with no clear slope at all; only in the last fifth of the file does the floor drop, with the low spikes clustering at the right (1982-83, 1997-98, 1999-00, the 21-day minimum of 2001-02, 2011-12, and 44 days in 2023-24). So it was partly what I expected: the direction and the minimum were right, but what I did not know was the shape - a long flat middle and a decline concentrated after about 1975, rather than a gentle slide across the whole record.
