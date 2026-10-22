# The breathing of Lake Michigan-Huron, 1918 to 2026

## Material

- Publisher: Coordinating Committee on Great Lakes Basic Hydraulic and Hydrologic Data (US and
  Canadian agencies; levels measured by NOAA and Fisheries and Oceans Canada)
- Dataset: "Lake Michigan-Huron Monthly Mean Water Levels 1918 to 2026" (metres, IGLD 1985)
- URL: https://www.greatlakescc.org/en/coordinating-committee-products-and-datasets/
  (file: https://drive.google.com/file/d/1z5010rdGBEmyFrVPOEOu-1PpxP8u5Hta/view)
- Licence: none stated on the page or in the file. The file header says the data are coordinated
  by the Committee, measured by NOAA and DFO, and that the last 12 months are provisional.
  US federal data like this is generally in the public domain, but the page does not say so.
- Fetched: 2026-10-22
- Column given to the instrument: `level_m`
- Preparation: the original is a wide table with one row per year and twelve month columns, plus
  `#` comment lines. I dropped the comments, unrolled it into one row per month in date order
  (`month` as YYYY-MM, `level_m`), and dropped the three cells marked -9999 (Oct to Dec 2026, not
  yet measured). Result: `michigan_huron_levels.csv`, 1,305 rows from 1918-01 to 2026-09, values
  unchanged. I deleted the raw download once the CSV was made.

## Runs

1. `python3 instrument.py michigan_huron_levels.csv --column level_m`: n = 1305, 0 skipped,
   min 175.57, max 177.50. This is the reading.

## What it showed

The line is a dense sawtooth of yearly cycles, a few tenths of a metre each, riding on slow swings
almost two metres tall: down to the 1934 trough, up to 1952, down to the lowest point of the 1960s
(March 1964, 175.58 m), a long high plateau through the 1970s and 1980s that peaks at the record
of October 1986 (177.50 m), then a sudden drop in 1998 to 2000 into a fourteen-year low that ends
at the record low of January 2013 (175.57 m), almost exactly level with 1964. After that comes the
steepest climb in the record: about 1.9 m in seven years, to the 2020 high. Since then it has fallen
steadily, and 2025 to early 2026 is back near the levels of the early 2000s. This is mostly what I
expected. I had not expected two things: the 2020 peak does not exceed 1986, and the 2013 low
matches 1964 to within a centimetre. So the lake has been swinging between the same two limits for
a century rather than drifting out of them. The other surprise was how abrupt the 1998 fall is next
to the gentle slopes everywhere else.
