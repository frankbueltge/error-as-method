# Two clocks on Mars: GAPS on Curiosity's weather report

## Material

- Publisher: NASA / JPL (Mars Exploration Program website), with the data prepared by the Centro de Astrobiología (CAB, INTA-CSIC, Spain), which built the REMS instrument.
- Dataset: Mars Science Laboratory (Curiosity rover) REMS weather report, one row per sol, sols 1 to 4995 (2012-08-07 to 2026-08-25).
- URL: https://mars.nasa.gov/rss/api/?feed=weather&category=msl&feedtype=json (the JSON feed behind https://mars.nasa.gov/msl/weather/).
- Licence as I found it: no licence is stated in the feed. It carries a CAB disclaimer that the file "is provided ... for outreach purposes only. Any other use is discouraged", that CAB takes no responsibility for results made from it, and that the scientific REMS data are in the NASA PDS. NASA web content is generally not copyrighted, but no explicit licence was given.
- Fetched: 2026-10-22.
- Column given to the instrument: `terrestrial_date` (the Earth date at the sol's local midday).
- Preparation: the feed lists sols newest first; I took the `soles` array, reversed it into chronological order (sol ascending; checked that sols strictly increase), and wrote every field of every row unchanged to `curiosity_rems_weather.csv` (4745 rows, 18 columns, 0.44 MB). The descriptive texts and disclaimers of the feed were dropped. The raw JSON was deleted after conversion.

## Runs

1. `python3 instrument.py curiosity_rems_weather.csv --time terrestrial_date` — ran on the first attempt; wrote `reading.svg` and `reading.json`.

## What the instrument showed

GAPS found a cadence of 1 day, no unreadable times, no repeats or steps back, and 182 gaps, spread evenly along the line with a few wide red blocks: the largest are 31 days (after 2018-09-17), 24 days (after 2023-11-01), 16 days (after 2013-02-27), 15 days (after 2019-02-13) and 14 days (after 2021-12-20). Checking the gaps against the `sol` column afterwards, 127 of the 182 are two-day jumps between consecutive sols: no data are missing there, only an Earth date skipped because a sol is 40 minutes longer than a day. So two thirds of what the instrument calls breaks are the record's own Martian clock slipping past the Earth calendar; the remaining 55 are real silences (250 missing sols in all). That much I expected. What I did not expect is what the large gaps are not: the solar conjunctions (2013, 2015, 2017, 2019, 2021) mostly leave no wide gap, presumably because REMS kept measuring and the data were sent home later, so only the 2023 conjunction shows as a long silence. The longest silence, in September-October 2018, coincides instead with the rover's computer trouble and swap to its backup computer that autumn, and the 2013 one with the memory fault of February 2013 (my reading of the dates, not something the data state). Also no two sols ever share an Earth date, so the repeats I thought possible never happen: the date used is the one at local midday, which always advances.
