# Thirty-six years at the pump

## Material

- Publisher: U.S. Energy Information Administration (EIA), Gasoline and Diesel Fuel Update; republished by
  the Federal Reserve Bank of St. Louis in FRED.
- Dataset: "US Regular All Formulations Gas Price", series GASREGW, weekly, dollars per gallon, not seasonally adjusted.
- URL: https://fred.stlouisfed.org/series/GASREGW (file fetched from https://fred.stlouisfed.org/graph/fredgraph.csv?id=GASREGW)
- Licence as found: FRED marks the series "Public Domain: Citation Requested".
- Fetched: 2026-10-22.
- Column given to the instrument: `GASREGW`.
- Preparation: none. The FRED CSV (columns `observation_date`, `GASREGW`; 1,888 weekly rows from
  1990-08-20 to 2026-10-19) is kept unchanged as `gasoline_weekly.csv`. It has six empty cells
  (1990-12-10 to 1991-01-14), which the instrument skips. I first tried the EIA's own .xls download,
  but could not read the old Excel format here, so I used the FRED copy of the same series.

## Runs

1. `python3 instrument.py gasoline_weekly.csv --column GASREGW` -> n = 1882, skipped 6, min 0.907, max 5.006. This is the reading.

## What the instrument showed

The line looks the way I expected through 2022. It sits near a dollar for the 1990s, with the floor
(0.907) in February 1999. It climbs to the 2008 peak and drops off a cliff at the end of that year. There
is a high plateau from 2011 to 2014, a slide in 2015 and 2016, the 2020 trough, and the summit of 5.006 in
June 2022. I did not expect the end of the line. After falling to about $2.80 at the end of 2025, the price
jumps by about a dollar in four weeks of March 2026 (3.02 on 2 March, 3.99 on 30 March). It reaches 4.50
in May and is still around $4.28–4.35 in October 2026. That puts the last stretch of the picture almost as
high as 2022, not on the gentle $3 plateau I had guessed. The series alone does not say why. Note that the
instrument draws the values in file order without a time axis, so the six skipped cells in 1990–91 are
simply joined over.
