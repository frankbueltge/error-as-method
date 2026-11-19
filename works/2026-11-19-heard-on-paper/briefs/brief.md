# The brief given to every maker (two arms; the arm's sentence is the only difference)

Each maker is a fresh instance. It receives this text with `{ARM}` and `{IMAGES}` filled in.

---

You are making a small verbal form, on your own judgement.

Each of the images listed below is a spectrogram of one song of one wild bird, cut from a field recording: time in
seconds runs left to right, pitch in kHz runs bottom to top, darker is louder. Other birds or noise may be faint in the
background. {ARM}

For each image, do this, in this order:

1. **Look and count.** Open the image (use the Read tool on the path; open no other file of any kind). Describe in one
   or two sentences what the song's elements are, and count them: how many separate sounds does the main singer make
   in this cut?
2. **Make the phrase.** Write a short phrase of ordinary English words that a person could say aloud along with this
   song, so that the words fit it — its number of sounds, their lengths, their rises and falls, their stresses. Write the
   phrase plainly, as one line.
3. **Say where it came from.** In one sentence: what in the picture made you choose these words? And did any of the
   words come from something you already knew rather than from the picture? Say so honestly if they did.
4. **Name the bird, if you can.** If you think you know what species this is, name it and give your confidence from 0 to
   100. If you do not know, write "unknown". (Do this only after you have written the phrase.)

Answer with a single JSON object and nothing else:

```
{"maker": "<your maker id>", "files_opened": ["<every path you opened>"],
 "items": [{"image": "<letter>", "elements": "<description>", "count": <integer>, "phrase": "<the phrase>",
            "grounds": "<where it came from>", "species": "<name or unknown>", "confidence": <0-100>}]}
```

Your maker id is `{MAKER}`. Images:

{IMAGES}

---

**Arm U (unnamed)** — `{ARM}` is: *"You are not told which species sang."*

**Arm N (named)** — `{ARM}` is: *"For each image you are told the species that sang it."* and every image line carries
its species name after the path.
