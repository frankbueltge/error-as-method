# First to mind

1. Daily weather reports from the Curiosity rover on Mars (REMS instrument), dated by Earth date and by sol.
2. Bitcoin block timestamps (a ledger whose clock is allowed to run backwards).
3. The Central England Temperature daily series.

# Chosen

The Mars weather report of NASA's Curiosity rover: one row per sol from the REMS (Rover Environmental Monitoring Station) instrument, prepared by the Centro de Astrobiología (CAB, Spain) and published by NASA as a JSON feed at https://mars.nasa.gov/rss/api/?feed=weather&category=msl&feedtype=json (the feed behind the "Mars Weather" page at https://mars.nasa.gov/msl/weather/).
I came to it from the first item on my list: I wanted a record kept on one clock (Martian sols) but dated on another (Earth days). A sol is about 24 h 40 min, so a row per sol written down by Earth date cannot keep a one-day cadence for long, and the rover also falls silent for conjunctions, safe modes and instrument trouble. The feed was the first place I fetched, and it answered with the whole mission (sols 1 to 4995).

# Expected

I expect a cadence of 1 day with a steady sprinkle of 2-day "gaps" roughly every 36-37 rows, where an Earth date is skipped because a sol is longer than a day, plus a few longer gaps for solar conjunctions (about every 26 months) and rover safe modes; possibly some "repeats" where two sols carry the same Earth date.
