import json, re, sys, collections
src, out = sys.argv[1], sys.argv[2]
d = json.load(open(src))['ngalol']
def pos(p):
    a = p.replace('\n',' ').split()
    def dms(s):
        m = re.match(r"(\d+)°(\d+)'([\d.]+)?\"?([NSEW])", s)
        if not m: m = re.match(r"(\d+)°(\d+)'()([NSEW])", s)
        v = int(m.group(1)) + int(m.group(2))/60 + (float(m.group(3)) if m.group(3) else 0)/3600
        return -v if m.group(4) in 'SW' else v
    return dms(a[0]), dms(a[1])
rows = []; skipped = collections.Counter()
for x in d:
    ch = x['characteristic'] or ''
    if not ch or not (x['position'] or '').strip(): skipped['empty'] += 1; continue
    if 'RACON' in (x['name'] or '').upper() or re.match(r'^[A-Z]\(', ch): skipped['racon/morse'] += 1; continue
    lines = [l.strip() for l in ch.split('\n') if l.strip()]
    if not lines: skipped['empty'] += 1; continue
    head = lines[0]
    hs = re.sub(r'\([^)]*\)', ' ', head)
    cols = re.findall(r'(?<![A-Za-z])(W|R|G|Y|Bu|Vi|Or)(?=\.|\s|$|,)', hs)
    mult = int(re.match(r'(\d+)\s', head).group(1)) if re.match(r'(\d+)\s', head) else 1
    if not cols: skipped['nocolor'] += 1; continue
    per = None; lit = 0.0; ok = False
    for l in lines[1:]:
        m = re.match(r'period ([\d.]+)s', l)
        if m: per = float(m.group(1))
        m = re.match(r'(?:fl|lt)\.\s*([\d.]+)s,\s*ec\.\s*([\d.]+)s', l)
        if m: lit += float(m.group(1)); ok = True
    h = re.sub(r'^\d+\s+', '', head).replace('Dir.', '').replace('Al.', '')
    if ok and per: duty = lit / per
    elif h.startswith('F.') or h.startswith('2 F.') or h.startswith('3 F.') or 'F.' == h[:2]: duty = 1.0
    elif h.startswith('Iso'): duty = 0.5
    elif h.startswith('Oc'): duty = 0.7
    elif h.startswith('L.Fl'): duty = (2.0 / per) if per else 0.2
    elif h.startswith('V.Q'): duty = 0.3
    elif h.startswith('Q') or 'Q.' in h[:4]: duty = 0.3 if not per else min(0.3, 0.3*int((re.search(r'\((\d+)\)', h) or [0,'1'])[1])/per)
    elif h.startswith('Mo'): duty = 0.3
    elif h.startswith('Fl'):
        n = int((re.search(r'\((\d+)\)', h) or [0,'1'])[1]); duty = (n*0.5/per) if per else 0.1
    else: duty = 0.3; skipped['default-duty'] += 1
    duty = max(0.01, min(1.0, duty))
    rg = x['range'] or ''
    rmap = {}
    for c, v in re.findall(r'(W|R|G|Y|Bu)\.\s*([\d.]+)', rg): rmap[c] = float(v)
    if not rmap:
        m = re.match(r'\s*([\d.]+)', rg)
        base = float(m.group(1)) if m else None
    else: base = None
    lat, lon = pos(x['position'])
    lc = []
    for c in dict.fromkeys(cols):
        r = rmap.get(c, base)
        lc.append([c, r])
    rows.append({'n': (x['name'] or '').strip().rstrip('.'), 'lat': round(lat,4), 'lon': round(lon,4),
                 'c': lc, 'k': mult, 'p': per, 'd': round(duty,3), 'h': head})
print(len(rows), skipped, file=sys.stderr)
print(collections.Counter(c for r in rows for c,_ in r['c']), file=sys.stderr)
print(sum(1 for r in rows if r['c'][0][1] is None), 'no range', file=sys.stderr)
open(out,'w').write('window.LIGHTS=' + json.dumps(rows, separators=(',',':'), ensure_ascii=False) + ';\n')
