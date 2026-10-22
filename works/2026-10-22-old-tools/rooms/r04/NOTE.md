# Measles in Cambridge, 1944-1966, read by CYCLES

## Material

- Publisher: Bjørnstad lab, Department of Entomology, Penn State University (data compiled from the
  Registrar General's weekly returns for England and Wales; used in Bjørnstad, Finkenstädt & Grenfell 2002,
  Ecological Monographs, TSIR analysis of measles).
- Dataset: "60measles" - reported measles cases every fortnight, 1944-1966, for 60 cities of England and
  Wales (599 lines, tab-delimited: year, week, then one column per city).
- URL: https://ento.psu.edu/research/labs/ottar-bjornstad/ottar-lab-abstracts/60measles.txt
  (described on https://ento.psu.edu/research/labs/ottar-bjornstad/ottar-lab-abstracts/tsir-analysis-of-measles-in-england-and-wales)
- Licence as found: none stated; the page carries only "© 2026 The Pennsylvania State University". The page
  notes the counts are underreported by roughly 40-60%.
- Fetched: 2026-10-22.
- Column given to the instrument: `cases` (Cambridge).
- Preparation: kept only the Cambridge column, with year (written out as 1944-1966) and week (2, 4, ..., 52),
  into `cambridge_measles_biweekly.csv`: 598 rows, 26 fortnights per year, all values whole numbers, no gaps.
  Nothing was averaged, cut or converted otherwise.

## Runs

1. `python3 instrument.py cambridge_measles_biweekly.csv --column cases --step "fortnight"` - ran first time;
   598 values, no blocking. This is the reading.

## What it showed

The strongest period is about 54 fortnights (about 2.1 years, 11% of the power), then exactly 26 fortnights
(one year, 9%), then about 75 fortnights (about 2.9 years, 4%). So even this small city, which I expected to
be ruled by irregular fade-outs and the yearly school calendar, kept a two-year rhythm, and it outweighs the
annual one; that I did not expect. The low shares of power (the top three together only about a quarter)
do fit the expectation of an untidy record, with the third peak near three years hinting at epidemics that
sometimes skipped a year longer than the London pattern.
