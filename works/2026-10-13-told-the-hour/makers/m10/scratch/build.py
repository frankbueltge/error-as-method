import json
v=json.load(open('series.json'))
N=len(v)
w=[1,2,3,2,1]
s=[sum(w[k]*v[min(N-1,max(0,i+k-2))] for k in range(5))/9 for i in range(N)]
data=','.join(str(round(x)) if abs(x-round(x))<0.05 else f'{x:.1f}' for x in s)
html=open('template.html').read().replace('/*DATA*/',data)
open('/tmp/claude-0/s123/mk/m10/work/index.html','w').write(html)
print(len(html))
