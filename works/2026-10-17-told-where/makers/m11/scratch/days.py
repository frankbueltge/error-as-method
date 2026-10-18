import json
bl=json.load(open('blobs.json'))
x0=3.85;P=4.8217
days=[[] for _ in range(61)]
for x,y,v in bl:
  d=int((x-x0+P/2)//P)
  if 0<=d<61: days[d].append((x,y,v))
for d,b in enumerate(days):
  ys=sorted(y for x,y,v in b if y<81)
  top=ys[:3]
  # daylight extent in x
  dx=[x for x,y,v in b if y<80]
  ext=(max(dx)-min(dx)) if dx else 0
  print(d, len(ys), [round(83.5-t,1) for t in top], round(ext,2), round(sum(83.5-y for y in ys),0))
