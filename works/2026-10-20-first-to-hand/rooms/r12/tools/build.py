import json,sys,collections,datetime
from zoneinfo import ZoneInfo
tz=ZoneInfo('America/Denver')
d=json.load(open(sys.argv[1]))['entries']
ev={}
for e in d:
    if e['q']!='0': continue
    t=int(e['time']); k='L' if e['maj']=='1' else ('S' if e['min']=='1' else '')
    ev.setdefault(t,set()).add(k)
ts=sorted(ev)
out=[];last=None
for t in ts:
    if last is not None and t-last<20*60:
        out[-1][1]|=ev[t]; continue
    out.append([t,set(ev[t])]); last=t
rows=[]
hrs=collections.Counter()
for t,k in out:
    lt=datetime.datetime.fromtimestamp(t,tz)
    kind='L' if 'L' in k else ('S' if 'S' in k else 'U')
    rows.append(f"{t},{lt.timetuple().tm_yday},{lt.hour*60+lt.minute},{kind}")
    hrs[lt.hour]+=1
print(len(rows),sorted(hrs.items()),file=sys.stderr)
open(sys.argv[2],'w').write("// Old Faithful eruptions 2025 (GeyserTimes, ODbL). unix,dayOfYear(local),minuteOfDay(local),kind L=long S=short U=unmarked\nwindow.OF=`"+"\n".join(rows)+"`;\n")
