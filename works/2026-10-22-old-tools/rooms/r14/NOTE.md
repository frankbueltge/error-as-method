# The flu year, measured from the clinic waiting room

## Material

- Publisher: US Centers for Disease Control and Prevention (CDC), ILINet / FluView outpatient
  influenza-like illness surveillance; served by the Delphi Epidata API, Delphi group, Carnegie Mellon University.
- Dataset: FluView, region `nat` (US national), weekly by MMWR epiweek.
- URL: https://api.delphi.cmu.edu/epidata/fluview/?regions=nat&epiweeks=199740-202640
- Licence as I found it: not stated in the API response. CDC FluView data are US federal government
  public-domain works; Delphi's documentation states that data it redistributes from public sources
  remain under their original terms (I did not see a separate licence for this endpoint).
- Fetched: 2026-10-22.
- Column given to the instrument: `wili` (weighted percentage of outpatient visits for influenza-like
  illness, weighted by state population).
- Preparation: fetched as JSON (1420 weeks, 1997w40 to 2026w40). Before 2002/03 ILINet reported only
  October to May, so the record has summer gaps; I kept only epiweek 200240 onward, which is a
  continuous run of 1254 weeks (checked: no missing weeks, no missing `wili`) ending 2026w40. Converted
  to `ili_weekly.csv` with columns epiweek, wili, ili, num_ili, num_patients, num_providers, issue
  (the most recent revision of each week, as the API returns by default). No other changes.
  Weeks are MMWR epiweeks, so 53-week years occur occasionally; I treated each row as one even step.

## Runs

1. `python3 instrument.py ili_weekly.csv --column wili --step "week"` (the only run; succeeded).

## What it showed

The annual flu season stands out alone: a peak at 52.25 weeks holding 33% of the power, with nothing
else above 3%. That much I expected, and also the harmonic near 26 weeks (2%). What I did not expect
is that the second-strongest peak is not the half-year harmonic but a period of about 90 weeks
(1.7 years, 2.7% of power), and that the annual peak, dominant as it is, holds only a third of the
power: the rest is spread across long periods and sidebands rather than concentrated in a neat
yearly comb. The flu year is regular in its timing but irregular in its size, and the irregular
seasons (the 2009 pandemic wave, the almost absent 2020/21 season, the large 2017/18 and 2024/25
seasons) appear to the instrument as a slow beat beside the year rather than as multi-year cycles
of their own. Partly what I expected; the 90-week peak was the surprise.
