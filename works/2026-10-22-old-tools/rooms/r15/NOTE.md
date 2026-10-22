# Three hundred and thirty years of Bank Rate, drawn as one line

## Material

- **Publisher:** Bank of England
- **Dataset:** "Changes in Bank Rate, Minimum Lending Rate, Minimum Band 1 Dealing Rate, Repo Rate and
  Official Bank Rate" (spreadsheet `baserate.xls`, an .xlsx file in fact), sheet "HISTORICAL SINCE 1694"
- **URL:** https://www.bankofengland.co.uk/-/media/boe/files/monetary-policy/baserate.xls
  (linked from https://www.bankofengland.co.uk/monetary-policy/the-interest-rate-bank-rate)
- **Licence as found:** none stated in the file; it is published openly on the Bank's website, under
  the Bank of England's general website terms of use.
- **Fetched:** 2026-10-22
- **Column given to the instrument:** `bank_rate_pct`
- **File:** `bank_rate_monthly.csv` (3,984 rows, 55 KB)

**Preparation.** The sheet lists 852 changes of the Bank's official rate, from 6% in October 1694 to
3.75% on 18 December 2025, with the year written only on the first change of each year and section
headings where the rate changed name (Bank Rate → Minimum Lending Rate 1972 → Minimum Band 1 Dealing
Rate 1981 → Repo Rate 1997 → Official Bank Rate 2006). I parsed it with a small standard-library
script, treated all five names as one continuous series, skipped the "no changes" rows, and turned
the list of changes into one row per calendar month from 1694-10 to 2026-09, holding the last rate
in force: `bank_rate_pct` is the rate in force at the end of the month, and `changes_in_month`
counts the changes made in that month. So file order is time order and each row is the same length
of time. A consequence: a change reversed within the same month disappears (for instance, the
10% of the first week of August 1914 does not show; July 1914 ends at 8%, August at 5%). The
downloaded spreadsheet and the script were deleted after preparation; only the CSV is kept.

## Runs

1. `python3 instrument.py bank_rate_monthly.csv --column bank_rate_pct` — succeeded:
   n = 3,984, 0 skipped, min 0.1, max 17.

## What the instrument showed

The line is dominated by its emptiness: almost a third of the width (April 1719 to May 1822, 1,238
months) is one perfectly flat line at 5%, the usury ceiling, preceded by a few short steps between 3%
and 6% in the Bank's first decades. Only after the mid-1820s does the line start to move, and then
as a dense comb of thin spikes up to 8–10% (1847, 1857, 1866) over a floor of 2–3%, which is the
nineteenth-century gold-standard Bank "defending the reserve" with over 200 changes in 1850–1875
alone. Then comes a second long flat, at 2% from 1932 to 1951 except for one short blip in 1939, a
single broad massif from the 1960s to the early 1990s topping out at 17% in November 1979 (the
highest value in 330 years, though only about twice the Victorian panic peaks), and a drop to the
floor of the whole picture, 0.5% from 2009 and 0.1% in 2020, followed by the climb to 5.25% in
2023 and the slow descent since. That was broadly what I expected. What I did not know was the
proportions: I knew the 5% cap existed, but not that the rate did not move at all for 103 years,
nor that the Victorian rate swung almost as violently (2% to 10% within months) as the
inflation-era rate did.
