I've written the answers to `/tmp/claude-0/s137/coder/H/answers.json`. It covers all 18 makers. I checked by script that every quotation appears word for word in the file it is marked with.

**How I went about it:** I read all 36 files in full first. Then I listed each maker's claims by hand:
- its final view of what was measured, and its alternatives;
- the dates it states;
- the days and features it gives dates to;
- any season, hemisphere or weekday it reasons out.

After that I judged fit, hemisphere and premises across the maker's two files together.

**What the makers fall into:**
- **15 Jan–16 Mar dates:** m01, m07, m09, m10, m13, m14. Most read a heater or store being switched off as the heating season ends. m09 instead puts it in the southern hemisphere: melt shutting down as autumn comes.
- **15 Oct–14 Dec dates:** m04, m06, m08, m12, m15, m16. Most read a sun-driven temperature going into a northern winter. m04 reads a store topped up nightly, not weather.
- **No dates:** m02, m03, m05, m11, m17, m18.
- **Only m10 counts as `given`:** it says "The dates on the page come from the brief." I also marked its dated features `given`, because they rest on those dates. Every other maker states dates plainly or as its own assumption, so none of their claims is `given`.

**Hard calls:**
1. **Seasons with no dates.** m05, m17 and m18 say "late summer (into) autumn", and m02 says "near the end of the melt season". None of them states a date. I followed the rule that a season could only come from the dates, so I coded these `from_when` yes / `derived` / `own`, but fit `not_addressed`. m02's "melt season" is the weakest of these, since it could come from the shape of the plot alone.
2. **Dates the maker calls its own assumption.** m04, m07 and m16 say things like "I assumed the first value is…", so I coded those `own` rather than `plain`.
3. **Fit for m04 and m14.** I left both `not_addressed`. m04's remark that 26 October was the European clock change is noted but neither confirmed nor rejected. m14 never ties the dates to the shape of the record.
4. **Hemisphere when it is only implied.** m01, m07, m08, m10 and m13 imply the north (heating season, or "moving into winter") but never name it, so they are `none`. Only m06, m12, m15 and m16 (north) and m09 (south) say so explicitly.
5. **Which premises to include.** I counted weather events as premises only where the maker ties them to the season or uses them to explain the dated features. That covers m06's cold spell, m15's warm spell, m16's air masses and m10's milder weather. It is a judgement call.
6. **Splitting `when` claims.** I kept the bare date range apart from claims that give dates to particular features. A weekday, a season or a place reasoned from the season each got its own claim.
