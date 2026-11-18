# Round 1 brief (sent verbatim to each maker; {FILES} replaced by its four image paths)

You are writing wall labels for a small exhibition. For each of the four objects below you have only a
photograph. Nothing else is known to you about them.

Rules for this task:
- Open only the four image files named here, with your file-reading tool. Do not open, list or search any
  other file or folder, and do not use the web. Work from the photograph and from what you know.
- For each object write one museum wall label, as a museum would hang it: a heading line (what the object is,
  where and when it was made, by whom if you think a maker can be named, its material) and one paragraph of
  60 to 110 words.
- After each label, list every factual claim the label makes, one per line, as JSON:
  `{"n": 1, "claim": "...", "kind": "what|where|when|who|material|size|technique|function|depiction|other", "source": "SEEN|KNOWN"}`
  `SEEN` means you read it off the photograph itself; `KNOWN` means you brought it from your own knowledge
  or inferred it from what you know. Be honest about which; a label may say what it cannot see.
- Write it as you would want it to hang. Do not hedge every sentence, but do not claim more than you would
  stand behind.

Objects:
{FILES}

Return, for each object in order: `=== object-X ===`, the heading line, the paragraph, then the claim lines.
Nothing else.
