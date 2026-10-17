import json,math
pk=json.load(open('peaks.json'))
g=[6.12, 11.19, 15.87, 20.78, 25.63, 30.44, 35.31, 40.0, 44.8, 49.71, 54.62, 59.35, 64.15, 69.05, 73.83, 78.64, 83.46, 88.23, 93.08, 97.85, 102.72, 107.51, 112.28, 117.1, 121.94, 126.85, 131.54, 136.41, 141.2, 146.15, 150.93, 155.9, 160.43, 165.31, 170.12, 175.0, 179.75, 184.6, 189.49, 194.21, 199.14, 203.96, 208.76, 213.53, 218.24, 223.22, 228.03, 232.89, 237.72, 242.29, 247.28, 252.05, 257.0, 261.88, 266.71, 271.37, 276.07, 281.05, 285.95, 290.91]
sp=(g[-1]-g[0])/(len(g)-1)
G=[g[0]-sp]+g+[g[-1]+sp]
print('spacing',sp, 'hours/px',24/sp)
base=83.6
days={k:[] for k in range(len(G))}
for x,y,v,s in pk:
  k=min(range(len(G)),key=lambda j:abs(G[j]-x))
  days[k].append((round((x-G[k])*24/sp,2),round(base-y,2),v))
for k in days:
  L=sorted(days[k]); print(k,' '.join('%+.1f:%.0f'%(a,b) for a,b,_ in L))
json.dump({'G':G,'sp':sp,'days':{str(k):sorted(v) for k,v in days.items()}},open('days2.json','w'))
