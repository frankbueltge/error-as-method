# Twenty years of Monday, Wednesday, Friday

## Material

- Publisher: Randall Munroe, xkcd (xkcd.com).
- Dataset: the xkcd archive, i.e. the number, publication date and title of every comic, 1 to 3314
  (comic 404 does not exist, by design, so 3313 rows).
- URL: https://xkcd.com/archive/ (the same dates are available per comic from the public JSON
  interface, https://xkcd.com/N/info.0.json).
- Licence as I found it: the site states its comics are under Creative Commons
  Attribution-NonCommercial 2.5 (https://xkcd.com/license.html); the JSON interface is offered openly
  for anyone to use. Only dates, numbers and titles are kept here, no images.
- Fetched: 2026-10-22.
- Column given to the instrument: `date`.
- Preparation: one fetch of the archive page; with a regular expression I took every link of the form
  `<a href="/N/" title="Y-M-D">Title</a>`, zero-padded the dates to ISO 8601 (YYYY-MM-DD), sorted
  the rows by comic number (the record's own order, not by date) and wrote `xkcd.csv` with columns
  `num,date,title`. Nothing was removed or added. The HTML page was then deleted.

## Runs

1. `python3 -I instrument.py xkcd.csv --time date` (from inside the folder): succeeded at once,
   wrote `reading.svg` and `reading.json`. This is the only run.

## What the instrument showed

Cadence 2 days; 1098 gaps, 46 repeats, 40 irregular steps, no steps back and no unreadable dates. As
expected the line is red from end to end, because every Friday-to-Monday weekend is a 3-day "gap"
against a 2-day cadence, and the 44 back-catalogue sketches all dated 1 January 2006 make a blue
knot at the very start. What I did not expect is how short the longest break is: in twenty years and
over 3300 comics the largest gap is 5 days (Wednesday 30 March to Monday 4 April 2016, a single
skipped Friday, April Fools' Day), and the next ones are only 4 days, almost all of them a Thursday
comic followed by the normal Monday. There is no week off, no holiday, no illness visible anywhere;
there are no steps back, so comic numbers never once ran against the calendar. The grey irregular
marks are the opposite of absence: clusters of daily comics (the weeks of 15 August 2006, 28 October 2008, 5 May 2009
and 23 November 2010) and single comics moved a day to meet news, such
as Gravitational Waves on Thursday 11 February 2016. The record breaks its cadence over a thousand
times, but nearly every break is the weekend; the promise itself was almost never broken.
