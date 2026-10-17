import json
days=json.load(open('days.json'))
inks=[2.59,2.86,2.43,2.63,2.54,2.44,2.55,2.49,2.57,2.50,2.64,2.67,2.67,2.69,2.59,2.59,2.57,2.64,2.65,2.82,2.78,2.65,2.65,2.90,3.17,2.82,2.67,2.83,2.69,2.79,2.76,2.96,2.61,2.79,2.64,2.78,2.77,2.75,2.90,2.72,2.83,2.78,2.71,2.68,2.65,2.80,2.87,2.93,2.81,2.72,2.92,2.95,3.15,3.05,2.98,2.83,3.00,3.27,3.14,3.22,3.11]
YB,YT=83.5,4.0
out=[]
for d,ink in zip(days,inks):
  pts=sorted(d['pts'],key=lambda p:(p[1],p[0]))
  kept=[]
  for p in pts:
    if kept and abs(p[1]-kept[-1][1])<0.6 and abs(p[0]-kept[-1][0])<=1: continue
    kept.append(p)
  vals=sorted([round((YB-p[1])/(YB-YT),3) for p in kept],reverse=True)
  out.append({'v':vals,'n':ink})
json.dump(out,open('data.json','w'),separators=(',',':'))
for i,o in enumerate(out): print(i,len(o['v']),o['v'][:3], round(sum(o['v']),2))
