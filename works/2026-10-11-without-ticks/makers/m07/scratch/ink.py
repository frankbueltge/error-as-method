import json
g=json.load(open('gray.json'))
grid={19,20,91,92,162,163,234,235,306,307,377,378}
def val(y): return 17000-(y-19.5)*12000/430.0
X0,X1=80,1080
import collections
baseof={y:collections.Counter(g[y][x] for x in range(81,1080)).most_common(1)[0][0] for y in range(21,449)}
cols=[]
for x in range(X0,X1+1):
    col=[]
    for y in range(21,449):
        base=baseof[y]
        v=g[y][x]
        # gridline rows: dots there can be darker than base
        ink=max(0,base-v)/ (base-32)
        col.append(ink)
    if x==80: col=[0.0]*len(col)
    cols.append(col)
# isolated dot ink
dot=sum(max(0,255-g[y][x]) for y in range(50,56) for x in range(721,729))/223
print('ink per dot',dot)
tot=sum(sum(c) for c in cols)
print('total ink/dot',tot/dot)
json.dump({'cols':cols,'dot':dot},open('ink.json','w'))
