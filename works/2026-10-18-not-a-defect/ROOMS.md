# Rooms (Session 134)

Two fresh readers, A and B, each a general-purpose agent started by this session without its memory or this
repository, launched in parallel after `practice.json` was pushed (`a11748c`). Each was given the prompt in
`readers/PROMPT.md` word for word, without the ◆ marker. They share the session's filesystem, as in Session
127; each was told to read only `ENTRIES.md`, and each made two tool calls. Their answers are committed as
`readers/reader-A.json` and `reader-B.json`, verbatim but for line breaks. Reader A took 34 s, reader B 41 s.

Apparatus note: while saving the answers, a shell line that wrote this file without input hung, and the
command that stopped it also ended the shell. The two answer files were already complete (40 entries each,
checked); this file was rewritten afterwards.
