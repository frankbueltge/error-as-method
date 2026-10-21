I wrote all 28 verdicts to <root>/packets/V/codes.json: 16 yes, 7 no and 5 cannot tell.

- **Yes (16):** T01, T04, T05, T06, T07, T09, T12, T13, T14, T16, T17, T18, T19, T22, T24, T28. Nine of these (T01, T04, T07, T12, T13, T14, T17, T24, T28) are byte-identical files, so they share the same check.
- **No, wrong values (3):** T08 has many marks below 1 K. T10 draws hydrogen melting at about 0.8 K. T25 starts hydrogen at about 1 K and lithium at about 7 K, and says 0 elements have never been measured.
- **No, wrong order (4):** T02, T11, T20 and T23 have correct bars, but the columns are not in atomic-number order although the footer says they are. This is a judgement call: if a false caption about the chart should not count against the elements, these four would be yes.
- **Cannot tell (5):** T03, T15 and T27 are blank. T21 and T26 have no labels and show too little to check.

T08 is also a judgement call: it has no element labels, but I marked it no because nothing melts or boils below 1 K. Image tools were broken here, so I could not zoom in. I checked every image by eye and by calculating values from the pixel positions on the log axis.
