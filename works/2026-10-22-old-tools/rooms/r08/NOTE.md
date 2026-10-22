# The Hot 100 keeps its week

## Material

- Publisher: UT Data (School of Journalism and Media, University of Texas at Austin), archive project "rwd-billboard-data", compiled from the Billboard Hot 100 charts.
- Dataset: `hot-100-current.csv`, every entry of every Billboard Hot 100 chart, 1958-08-04 to 2026-10-24.
- URL: https://raw.githubusercontent.com/utdata/rwd-billboard-data/main/data-out/hot-100-current.csv (project: https://github.com/utdata/rwd-billboard-data)
- Licence as found: MIT License (LICENSE file in the repository, "Copyright (c) 2019 UT Data"). The chart data itself originates with Billboard.
- Fetched: 2026-10-22.
- Column given to the instrument: `chart_week`.
- Preparation: the download (about 20 MB, one row per song per week, not in date order) was reduced to the distinct values of `chart_week`, sorted ascending, and written as a single column to `hot100_chart_weeks.csv` (3,560 rows, 43 KB). The full download was then deleted. Because the dates were deduplicated and sorted, the instrument cannot see repeats or steps back that may exist in the original row order; it reads only the sequence of chart dates.

## Runs

1. `python3 instrument.py hot100_chart_weeks.csv --time chart_week` (the only run; it succeeded).

## What the instrument showed

The cadence is 7 days, and in 68 years and 3,560 charts it is broken only three times. The first is a 12-day gap from Monday 1961-12-25 to Saturday 1962-01-06: the moment Billboard moved the chart's dating from Mondays to Saturdays, which I expected, though I expected it as an "irregular" step rather than a gap. The other two I did not know: an 8-day gap followed by a 6-day irregular step around Sunday 1976-07-04, a single chart dated on the Bicentennial Independence Day instead of Saturday July 3, after which the record returns to its Saturday beat. There are no missing weeks at all, and no holiday gaps, so the record is more perfectly kept than I expected; its only departures are the one deliberate change of weekday and one patriotic exception.
