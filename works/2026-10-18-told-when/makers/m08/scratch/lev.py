from PIL import Image
import json
im=Image.open('/tmp/claude-0/s135/mk/m08/work/record.jpg').convert('L')
W,H=im.size; p=im.load()
c0,step=5.6,4.585
centers=[c0+k*step for k in range(18)]
M=[]
for x in range(W):
    row=[]
    for c in centers:
        ys=[y for y in range(H) if abs(y-c)<=1.6]
        d=max(255-p[x,y] for y in ys)
        row.append(d)
    M.append(row)
json.dump(M,open('M.json','w'))
# per day histogram
days=[]
for d in range(61):
    x0=d*300/61; x1=(d+1)*300/61
    h=[0]*18
    for x in range(W):
        if x0<=x+0.5<x1:
            for k in range(18):
                if M[x][k]>110: h[k]+=1
    days.append(h)
    present=[k for k in range(18) if h[k]]
    print(d, ''.join(('%d'%min(h[k],9)) if h[k] else '.' for k in range(18)))
json.dump(days,open('days.json','w'))
