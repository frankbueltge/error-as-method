import json
B=json.load(open('blobs.json'))
P=4.82; c0=3.89-P
up=[b for b in B if b['ymax']<=81]
FL=83.5; TOP=5.5
rows=[]
n=0
while c0+n*P<300:
  a=c0+n*P; b=a+P
  bs=[q for q in up if a<=q['x']<b]
  cnt=sum(q['ink'] for q in bs)/380
  mx=max([(FL-q['y'])/(FL-TOP) for q in bs],default=0)
  s=sum((FL-q['y'])/(FL-TOP)*q['ink']/380 for q in bs)
  rows.append((n,round(a,1),round(cnt,1),round(mx,2),round(s,2)))
  n+=1
for r in rows: print(r)
