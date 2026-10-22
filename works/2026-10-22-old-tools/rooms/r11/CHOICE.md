# First to mind

1. The Central England Temperature daily series (Met Office Hadley Centre), daily mean temperature since 1772.
2. The US Treasury 10-year constant-maturity yield, daily (Federal Reserve H.15 / FRED series DGS10).
3. NASA's Astronomy Picture of the Day archive: the date of every picture since 1995.

# Chosen

The publication dates of every xkcd comic (Randall Munroe's webcomic), comic 1 to 3314, taken from
the xkcd archive page, https://xkcd.com/archive/ (each entry carries the comic's number and its date;
the same dates are served by the public JSON interface, https://xkcd.com/info.0.json and
https://xkcd.com/N/info.0.json). How I came to it: my three first thoughts were all things already
close to the excluded list (temperature and sunlight, or a market series whose breaks are just
weekends and holidays). GAPS asks where a record breaks its own promise of regularity, and xkcd
makes a famous, explicit promise ("updated every Monday, Wednesday, and Friday") kept for twenty
years by one person. That is a cadence with a human behind it, and the breaks should be readable as
a life: sickness, holidays, a wedding, a book. The archive page gives the whole record in one fetch.

# Expected

The commonest interval will be 2 days (Monday to Wednesday, Wednesday to Friday), so every Friday to
Monday weekend will show as a 3-day "gap" and the line will be densely red throughout; on top of
that I expect a burst of repeats in January 2006 (the old sketches all dated on one day), a handful
of longer gaps of a week or two, and a few irregular one-day steps from extra or out-of-schedule
comics such as April Fools' interactives.
