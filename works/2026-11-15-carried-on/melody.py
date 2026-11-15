"""Shared melody code for Carried On (Session 178).

A melody is a list of notes (midi pitch, duration in quarter notes, phrase end flag).
The notation handed to makers is plain text: one token per note, NAME+OCTAVE:DURATION,
with ' | ' after a phrase end. Example:  G4:1/3 F#4:1/3 G4:1/3 A4:1 | ...

The distance is an alignment (Needleman-Wunsch) between two melodies after two
normalisations that let a sung variant in another key or another note value count as
the same tune: pitch is taken relative to the melody's last note (the final), and
duration relative to the melody's median duration. Substitution cost is
  pitch part: min(|dp|, 12)/12      (semitones, capped at an octave)
  rhythm part: min(|log2(d1/d2)|, 2)/2
weighted 0.5/0.5 for the combined distance; a gap costs 1 for the combined distance
(and 1 in each one-dimension distance). The alignment cost is divided by the longer
melody's length, so 0 is identical and about 1 is unrelated.
"""
from fractions import Fraction
import math, re, statistics

NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
FLAT = {'Db': 'C#', 'Eb': 'D#', 'Gb': 'F#', 'Ab': 'G#', 'Bb': 'A#'}


def name(midi):
    return f"{NAMES[midi % 12]}{midi // 12 - 1}"


def midi_of(tok):
    m = re.fullmatch(r'([A-G](?:#|b)?)(-?\d)', tok)
    if not m:
        raise ValueError(tok)
    n = FLAT.get(m.group(1), m.group(1))
    return NAMES.index(n) + 12 * (int(m.group(2)) + 1)


def to_text(notes, meter=None):
    out = []
    for p, d, end in notes:
        fr = Fraction(d).limit_denominator(48)
        ds = str(fr.numerator) if fr.denominator == 1 else f"{fr.numerator}/{fr.denominator}"
        out.append(f"{name(p)}:{ds}")
        if end:
            out.append('|')
    s = ' '.join(out).rstrip(' |')
    return (f"meter {meter}: " if meter else '') + s


def parse_text(s):
    """Parse the plain notation back. Tolerant of a leading 'meter x/y:' and stray bars."""
    s = s.strip()
    s = re.sub(r'^meter\s+\S+\s*:\s*', '', s)
    notes = []
    for tok in s.replace('||', '|').split():
        if tok == '|':
            if notes:
                p, d, _ = notes[-1]
                notes[-1] = (p, d, True)
            continue
        m = re.fullmatch(r'([A-G](?:#|b)?-?\d):(\d+(?:/\d+)?(?:\.\d+)?)', tok)
        if not m:
            raise ValueError(f'bad token {tok!r}')
        notes.append((midi_of(m.group(1)), float(Fraction(m.group(2))), False))
    if notes:
        p, d, _ = notes[-1]
        notes[-1] = (p, d, True)
    return notes


def norm(notes):
    fin = notes[-1][0]
    med = statistics.median(d for _, d, _ in notes) or 1.0
    return [(p - fin, d / med) for p, d, _ in notes]


def _cost(a, b, wp, wr):
    dp = min(abs(a[0] - b[0]), 12) / 12
    dr = min(abs(math.log2(a[1] / b[1])), 2) / 2 if a[1] > 0 and b[1] > 0 else 1
    return wp * dp + wr * dr


def distance(m1, m2, wp=0.5, wr=0.5):
    a, b = norm(m1), norm(m2)
    n, m = len(a), len(b)
    prev = [j * 1.0 for j in range(m + 1)]
    for i in range(1, n + 1):
        cur = [i * 1.0] + [0.0] * m
        for j in range(1, m + 1):
            cur[j] = min(prev[j - 1] + _cost(a[i - 1], b[j - 1], wp, wr),
                         prev[j] + 1, cur[j - 1] + 1)
        prev = cur
    return prev[m] / max(n, m)


def dist3(m1, m2):
    return {'all': distance(m1, m2), 'pitch': distance(m1, m2, 1, 0), 'rhythm': distance(m1, m2, 0, 1)}


def norm_tonic(notes, tonic_pc):
    """Post hoc (Session 178): pitch relative to the tonic pitch class at or below the final,
    so a changed last note does not shift the whole melody."""
    fin = notes[-1][0]
    ref = fin - ((fin - tonic_pc) % 12)
    med = statistics.median(d for _, d, _ in notes) or 1.0
    return [(p - ref, d / med) for p, d, _ in notes]


def distance_tonic(m1, t1, m2, t2, wp=0.5, wr=0.5):
    a, b = norm_tonic(m1, t1), norm_tonic(m2, t2)
    n, m = len(a), len(b)
    prev = [j * 1.0 for j in range(m + 1)]
    for i in range(1, n + 1):
        cur = [i * 1.0] + [0.0] * m
        for j in range(1, m + 1):
            cur[j] = min(prev[j - 1] + _cost(a[i - 1], b[j - 1], wp, wr), prev[j] + 1, cur[j - 1] + 1)
        prev = cur
    return prev[m] / max(n, m)
