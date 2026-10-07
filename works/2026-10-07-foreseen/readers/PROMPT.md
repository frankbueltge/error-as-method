# The reader's instruction (verbatim, identical for every reader)

`{FILE}` is replaced by the one file the reader is given. Every reader is started without memory
of this practice or of any other reader, and reads one file only.

---

You are a reader in a perception experiment. Open exactly one file with your file-reading tool:
`{FILE}`. Do not open, list or search any other file or directory, do not run code, and do not use
the web.

It is one rendering of a daily count over 731 consecutive days, numbered 1 to 731. Day 1 is a
Monday. Nothing else about it is given to you. Answer from this rendering alone. Where the
rendering does not let you answer, say "cannot tell"; that is a full answer.

1. **Cycle.** Does the count recur with a period between 20 and 40 days? yes, no or cannot tell; if yes, the period in days.
2. **Week.** Does the count have a weekly (7-day) rhythm? yes, no or cannot tell.
3. **Level.** Is the typical level of days 367-731 higher, lower or about equal (within 10 %) compared with days 1-366? Or cannot tell.
4. **Year.** Are the same months of the year high in both years (an annual pattern)? yes, no or cannot tell.
5. **Highest day.** Which single day has the highest count? A day number, or cannot tell.
6. **Second event.** Which day is highest among days more than 14 days away from your answer to 5? A day number, or cannot tell.
7. **Peak shape.** Is the highest peak a single day or a run of several days (days within 3 days of it at half its height or more)? single, run or cannot tell.
8. **Drops.** Are there days far below their surroundings (less than a third of the typical level around them)? List them as day numbers or ranges, or "none", or cannot tell.
9. **What stands out.** List every day or run of days that stands out as singular against its surroundings, as day numbers or ranges (e.g. 140 or 140-142). An empty list is an answer.
10. **What decided.** For each of 1-9, a few words on what in the rendering decided your answer.
11. **Only after answering 1-10:** what do you guess this count is? One line. "No idea" is fine.

Reply with only a JSON object:
{"cycle": "yes|no|cannot tell", "period_days": null, "week": "yes|no|cannot tell",
 "level": "higher|lower|about equal|cannot tell", "year": "yes|no|cannot tell",
 "highest_day": null, "second_day": null, "peak_shape": "single|run|cannot tell",
 "drops": ["..."] or "none" or "cannot tell", "stands_out": ["..."],
 "decided": {"cycle": "", "week": "", "level": "", "year": "", "highest_day": "", "second_day": "", "peak_shape": "", "drops": "", "stands_out": ""},
 "guess": "", "files_opened": ["..."]}
