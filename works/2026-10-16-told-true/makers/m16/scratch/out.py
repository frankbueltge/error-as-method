import json
d=json.load(open('/tmp/claude-0/s130/mk/m16/scratch/series.json'))
s=d['series']
# local robust baseline: median over +-36h
out=[]
for h,v in enumerate(s):
    win=sorted(s[max(0,h-36):h+37]); med=win[len(win)//2]
    q=win[int(len(win)*0.05)]
    if v<q-6: out.append((h,round(v,1),round(med,1),h%24))
print(len(out)); print(out)
print(min(s),max(s))
