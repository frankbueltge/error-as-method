# The neighbours' clock: residential noise complaints in New York, hour by hour

## Material

- Publisher: City of New York, NYC Open Data (311 Customer Service Center / DoITT)
- Dataset: 311 Service Requests from 2010 to Present (id erm2-nwe9)
- URL: https://data.cityofnewyork.us/Social-Services/311-Service-Requests-from-2010-to-Present/erm2-nwe9
  (queried through https://data.cityofnewyork.us/resource/erm2-nwe9.csv)
- Licence as found: NYC Open Data, published under the NYC Open Data Terms of Use (public, free to
  use); I did not see a separate licence named in the API response.
- Fetched: 2026-10-22
- Column given to the instrument: `complaints`
- Preparation: one SoQL query on the API selected only rows with complaint_type = "Noise - Residential"
  and created_date from 2025-05-05T00:00 to before 2025-10-20T00:00 (New York local time), grouped by
  calendar day and hour of created_date, and counted them. That gave 4032 rows, every hour of 24 whole
  weeks (Monday to Sunday) with none missing; the window lies between the spring and autumn
  daylight-saving changes, so the hours are evenly spaced. I joined day and hour into one `hour`
  column (e.g. 2025-05-05T00:00) and kept the count as `complaints`. File:
  `nyc311_noise_residential_hourly.csv` (85 KB, 187,937 complaints in total).

## Runs

1. `python3 instrument.py nyc311_noise_residential_hourly.csv --column complaints --step "1 hour"` -
   ran first time; 4032 values, no blocking. This is the reading.

(Before that, one API query failed because SoQL has no `date_trunc_ymdh`; I regrouped by day and hour.
The instrument was not run on that.)

## What the instrument showed

The day dominates: a 24-hour period holds 22% of the power, then the week (168 hours, 9%), then the
12-hour harmonic (8%), exactly the order I expected. The complaints trough around 6 a.m. (about 16
an hour across the city) and peak around 10-11 p.m. and midnight (about 125 an hour), and weekend
days carry roughly twice the complaints of midweek days. What I did not know is in the weights: even
though Saturdays and Sundays are twice as loud as Tuesdays to Thursdays, the week holds less than half
the power of the day, because the weekend excess is a taller version of the same night-time peak and
so largely feeds the daily line. Counting by the calendar also shows the party spilling over midnight:
Sunday (which collects Saturday's small hours) has more complaints than Saturday, and Monday more than
Friday.
