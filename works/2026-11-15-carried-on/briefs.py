"""Write the brief every maker gets. The parallel makers and chain link 1 get the four
sources; chain link k>1 gets link k-1's four versions in the same frame.

Run: python3 -I briefs.py            -> briefs/source.txt
     python3 -I briefs.py chain K    -> briefs/chain-K.txt from makings/chain-(K-1).txt
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from melody import parse_text, to_text

HERE = os.path.dirname(os.path.abspath(__file__))
plan = json.load(open(os.path.join(HERE, 'plan.json')))
SONGS = ['A', 'B', 'C', 'D']

FRAME = """Below are the melodies of four songs, A to D. They are songs that people pass on by singing them.

Each melody is written one note per token, as PITCH:DURATION. PITCH is a note name with its octave (C4 is middle C, F#4 the F sharp above it). DURATION is in quarter notes (1 is a quarter note, 1/2 an eighth, 3/2 a dotted quarter). A bar line | marks the end of a phrase. The first words give the meter.

Make your own version of each song, the way it would come out if you carried it on.

Answer with exactly four lines and nothing else, one per song, in the same notation, each starting with its letter and a colon:
A: meter ...: ...
B: meter ...: ...
C: meter ...: ...
D: meter ...: ...

Do not use any tools, files or searches. Answer from this message alone.

{songs}
"""


def frame(texts):
    return FRAME.format(songs='\n'.join(f'{k}: {t}' for k, t in zip(SONGS, texts)))


def parse_answer(path):
    """Return {letter: (meter, text)} from a maker's four lines."""
    out = {}
    for line in open(path):
        line = line.strip()
        if len(line) > 2 and line[0] in SONGS and line[1] == ':':
            body = line[2:].strip()
            meter = body.split(':')[0].replace('meter', '').strip() if body.startswith('meter') else None
            out[line[0]] = (meter, body)
    return out


if __name__ == '__main__':
    os.makedirs(os.path.join(HERE, 'briefs'), exist_ok=True)
    if len(sys.argv) == 1:
        texts = [f['text'] for f in plan['families']]
        open(os.path.join(HERE, 'briefs/source.txt'), 'w').write(frame(texts))
    else:
        k = int(sys.argv[2])
        prev = parse_answer(os.path.join(HERE, f'makings/chain-{k-1}.txt'))
        texts = []
        for s in SONGS:
            meter, body = prev[s]
            texts.append(to_text(parse_text(body), meter))  # re-written in canonical form
        open(os.path.join(HERE, f'briefs/chain-{k}.txt'), 'w').write(frame(texts))
