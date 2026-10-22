# The week of New York's noise complaints

## Material

- Publisher: City of New York, NYC 311 (via NYC Open Data, Office of Technology and Innovation)
- Dataset: "311 Service Requests from 2020 to Present" (Socrata id erm2-nwe9)
- URL: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2020-to-Present/erm2-nwe9
- Licence as found: the dataset metadata names no licence (licence field empty, attribution "311"); NYC Open Data is published under the NYC Open Data Terms of Use, free for public use.
- Fetched: 2026-10-22
- Column given to the instrument: `complaints`
- Preparation: I queried the Socrata API for complaints whose `complaint_type` begins with "Noise" (Noise - Residential, Noise - Street/Sidewalk, Noise - Commercial, Noise - Vehicle, etc.), grouped by the calendar day of `created_date`, counted per day (server-side). The result runs 2020-01-01 to 2026-10-21; I dropped 2026-10-21 because it was only partly recorded, checked that no day was missing between 2020-01-01 and 2026-10-20 (none was), and wrote `noise_311_daily.csv` with columns `date, complaints` (2485 rows, one per day).

## Runs

1. `python3 instrument.py noise_311_daily.csv --column complaints --step "day"` — succeeded; 2485 values, no blocking. Strongest periods: 7.0 days (20% of power), 355 days (8%), 3.5 days (4%).

## What it showed

The week, not the year, is New York's loudest rhythm: the 7-day period carries a fifth of all the power, more than twice the annual cycle (read as 355 days, the nearest whole-record harmonic to a year), and the week's 3.5-day harmonic comes third, a sign that the weekly shape is sharp-edged — complaints pile up on weekend nights rather than swelling gently. I expected all three periods but in the other order: I thought the summer swing would dominate over less than seven years of record. That it does not says that the calendar of work and leisure governs when New Yorkers lose patience with their neighbours more strongly than the season does.
