from PIL import Image
import json
im=Image.open('/tmp/claude-0/s133/mk/m05/work/record.jpg').convert('L')
W,H=im.size;p=im.load()
NO=0.06
d=[[max(0,(255-p[x,y])/255-NO) for x in range(W)] for y in range(H)]
# dot ink under same transform: median of isolated dots 5x5
P=4.82; x0=2.01-4.82/2; FLOOR=83.5; SPAN=78.0; TOPROW=80
def val(y): return max(0,(FLOOR-y)/SPAN)
# calibrate DOT: total transformed ink in a few isolated dots
pts=[(35,14),(146,35),(228,45),(147,66),(238,27),(7,51),(127,43),(292,52)]
dots=[sum(d[y+j][x+i] for i in range(-2,3) for j in range(-2,3)) for x,y in pts]
DOT=sorted(dots)[len(dots)//2]; print('DOT',dots,DOT)
days=[]
for k in range(0,62):
    c=2.01+P*k
    sides=[]
    for lo,hi in ((c-P/2,c),(c,c+P/2)):
        hist=[0.0]*(TOPROW+1)
        for x in range(W):
            w=max(0,min(x+1,hi)-max(x,lo))
            if w<=0: continue
            for y in range(TOPROW+1): hist[y]+=d[y][x]*w
        sides.append([h/DOT for h in hist])
    am=sum(sides[0]); pm=sum(sides[1])
    days.append({'k':k,'am':sides[0],'pm':sides[1]})
    print(k, round(am,1), round(pm,1), round(sum(val(y)*(sides[0][y]+sides[1][y]) for y in range(TOPROW+1)),2))
json.dump({'days':days,'floor':FLOOR,'span':SPAN},open('hist.json','w'))
