I've written the answers to /tmp/claude-0/s135/coder/H/answers.json, with keys m01 to m12. The only other thing I made was a temporary Python helper in my scratchpad, which I deleted after use.

**How I went about it:** I read all 24 files in full, then coded each maker's what and when claims. I grouped claims by content and kept separate entries for the medium or kind, the place, the alternatives the maker considered, and any rejected readings. A script checked that every quotation appears word for word in the file it is marked with, and all of them do.

**What the files show:** Six makers mention the dates: m03, m04, m06, m08, m10 and m11. Their stated date claims are all coded `plain`, because none of them says the dates came from outside. m08 only shows it by "a small caption with the title and dates" together with "mid-July to mid-September". The other six (m01, m02, m05, m07, m09, m12) give a season they reasoned from the slow fall in the plot. I coded those as `when` with `from_when` `no`. One of them, m12, guessed "September–October", which disagrees with the sentence. No maker anywhere uses `given` or `against` about the dates.

**Hard calls:**
- **Season claims from makers who weren't told:** the brief lists a season as a when-type statement, but these makers say outright that they inferred it from the shape. For example, m01 writes "The fall is the part that suggests autumn". I kept the topic as `when` and set `from_when` to `no`.
- **Which "temperature" claims rest on the dates:** m03, m04, m06, m08, m10 and m11 each list the mid-July to mid-September decline (or "late-summer cooling") as one of several grounds. I marked all of these `from_when` `yes`, `derived`, even though the dates are only one of the grounds. For m11 this is weakest: it mentions the dates only in "a cooling trend from mid-July to mid-September".
- **Northern Hemisphere (m06, m08, m10):** none of them spells out the reasoning. I coded it `derived` because only the July-to-September cooling could support it.
- **m10:** "the decline of the season" is not a named season. I kept it as a `derived` season claim, separate from the dated drops ("1–3 August", "20 August", and so on).
- **m11:** it names no season at all, so it only has a stated date claim.
- **m04's water-level alternative:** it is "driven by the daily and seasonal cycle", and I coded it `from_when` `no`. It could also be read as resting on the season.
- **m03's weekday claim:** "15 July 2025 is a Tuesday" is `derived` and `favoured` `yes`, because the whole calendar layout is built on it.
- **Place and medium claims:** I marked these `favoured` `yes` only when they appear in the maker's main "my view" sentence. Secondary "points to" remarks got `no`.
