You start without any history. Do not use any tool except reading the file named below.

`{FILE}` holds sixteen cases. In each, someone chose a dataset and, before running a small measuring
program (an "instrument") on it, wrote what they expected the instrument to show. Then the instrument
ran, and its output is given (JSON).

For every case, give:
- "met": MET if the output shows what was expected, in the respects the expectation names; PARTLY if
  some named respects are shown and some are not; NOT_MET if the output contradicts the expectation or
  shows none of what it named.
- "specific": YES if the expectation names something the output can check exactly (a number, a period,
  a digit, a date, a direction of departure), NO if it is only general.
- "reason": one sentence.

Judge only from the expectation and the output, not from what you know about the data.

Answer only with JSON: a list of objects {"id": ..., "met": ..., "specific": ..., "reason": ...}, in order.
