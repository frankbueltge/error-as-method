# Sixty-eight years of Saturdays, and one Monday that ran long

## Material

- Publisher: "Historic Billboard Hot 100 Data", a community-maintained GitHub repository by mhollingshead,
  which crawls Billboard's Hot 100 charts daily (the chart itself is published by Billboard).
- Dataset: `valid_dates.json`, the issue date of every Hot 100 chart in history (3,560 charts, 1958-08-04 to 2026-10-24).
- URL: https://raw.githubusercontent.com/mhollingshead/billboard-hot-100/main/valid_dates.json
  (repository: https://github.com/mhollingshead/billboard-hot-100)
- Licence: none found. The repository has no LICENSE file and the README states no licence; the data is
  published openly for anyone to download, and the chart content belongs to Billboard.
- Fetched: 2026-10-22.
- Column given to the instrument: `chart_date`.
- Preparation: converted the JSON array of date strings to a CSV, `hot100_chart_dates.csv`, with two columns,
  `chart_index` (1 to 3560, in the file's order) and `chart_date` (the date string unchanged). Nothing was
  removed, sorted or altered. The downloaded JSON was then deleted; only the CSV is kept.

## Runs

1. `python3 instrument.py hot100_chart_dates.csv --time chart_date` — succeeded on the first run.
   Cadence 7 days, 0 unreadable times, 1 break: a gap of 12 days after CSV row 179.

## What the instrument showed

The Hot 100 has kept its seven-day cadence for 3,559 consecutive intervals with exactly one exception: the
chart dated Monday 1961-12-25 is followed by one dated Saturday 1962-01-06, twelve days later. That is the
moment Billboard switched its issue dating from Mondays to Saturdays, which it has used ever since. I
expected the weekday change and expected no real gaps, so the overall picture matched; what I did not expect
is its form. I guessed the switch would show as a short, irregular step (moving Monday back to the preceding
Saturday, two days early); instead Billboard moved forward, stretching one week to twelve days, so the
record's only break is a gap rather than a short step. Across 68 years, no week was skipped, repeated or
doubled anywhere else.
