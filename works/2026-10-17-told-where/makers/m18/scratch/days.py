import json
pk=json.load(open('peaks.json'))
S=1463/299.0
# noon fit from gaps 6.12..290.91
g=[6.12, 11.19, 15.87, 20.78, 25.63, 30.44, 35.31, 40.0, 44.8, 49.71, 54.62, 59.35, 64.15, 69.05, 73.83, 78.64, 83.46, 88.23, 93.08, 97.85, 102.72, 107.51, 112.28, 117.1, 121.94, 126.85, 131.54, 136.41, 141.2, 146.15, 150.93, 155.9, 160.43, 165.31, 170.12, 175.0, 179.75, 184.6, 189.49, 194.21, 199.14, 203.96, 208.76, 213.53, 218.24, 223.22, 228.03, 232.89, 237.72, 242.29, 247.28, 252.05, 257.0, 261.88, 266.71, 271.37, 276.07, 281.05, 285.95, 290.91]
ph=[(x*S)%24 for x in g]
import math
c=sum(math.cos(2*math.pi*p/24) for p in ph); s_=sum(math.sin(2*math.pi*p/24) for p in ph)
noon=(math.atan2(s_,c)*24/2/math.pi)%24
print('noon index mod 24', noon, [round(p,1) for p in ph[:10]], [round(p,1) for p in ph[-10:]])
pts=[(x*S,y,v) for x,y,v,_ in pk if y<81.5]
base=83.5
days={}
for i,y,v in pts:
  d=math.floor((i-noon+12)/24)  # day index, 0 = day whose noon is at noon-? 
  days.setdefault(d,[]).append((round(i-noon-24*d,2),round(base-y,2)))
for d in sorted(days):
  L=sorted(days[d]); 
  print(d,len(L),'max',max(v for _,v in L),'span',L[0][0],L[-1][0])
json.dump({'noon':noon,'days':{str(k):sorted(v) for k,v in days.items()}},open('days.json','w'))
