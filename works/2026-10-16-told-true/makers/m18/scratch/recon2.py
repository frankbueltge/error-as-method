from PIL import Image, ImageDraw
import json
im=Image.open('/tmp/claude-0/s130/mk/m18/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
N=1464; x0,x1=2.3,296.7
xs=[x0+i*(x1-x0)/(N-1) for i in range(N)]
bycol={}
for i,x in enumerate(xs): bycol.setdefault(round(x),[]).append(i)
vals=[None]*N
groups=[]
for x in sorted(bycol):
    hrs=bycol[x]; k=len(hrs)
    p=[(y,max(0,215-px[x,y])) for y in range(H)]
    p=[(y,w) for y,w in p if w>40]
    tot=sum(w for _,w in p)
    q=[]
    for j in range(k):
        t=(j+0.5)/k*tot; c=0
        for y,w in p:
            if c+w>=t: q.append(y+ (t-c)/w - 0.5); break
            c+=w
    groups.append((hrs,sorted(q)))
# DP over orientation
best=[[0,0]]; bk=[]
for gi in range(1,len(groups)):
    pq=groups[gi-1][1]; q=groups[gi][1]
    ends=[pq[-1],pq[0]]; starts=[q[0],q[-1]]
    row=[];b=[]
    for s in range(2):
        c=[best[-1][t]+abs(ends[t]-starts[s]) for t in range(2)]
        t=0 if c[0]<=c[1] else 1
        row.append(c[t]); b.append(t)
    best.append(row); bk.append(b)
s=0 if best[-1][0]<=best[-1][1] else 1
ori=[s]
for gi in range(len(groups)-1,0,-1):
    s=bk[gi-1][s]; ori.append(s)
ori=ori[::-1]
for (hrs,q),o in zip(groups,ori):
    qq=q if o==0 else q[::-1]
    for h,v in zip(hrs,qq): vals[h]=v
# value: higher = larger => invert y
json.dump([round(v,2) for v in vals],open('ys.json','w'))
out=Image.new('L',(W,H),255); d=ImageDraw.Draw(out)
for x,y in zip(xs,vals): d.point((round(x),round(y)),0)
big=Image.new('L',(W,H*2+4),128); big.paste(im,(0,0)); big.paste(out,(0,H+4))
big.resize((W*3,(H*2+4)*3),Image.NEAREST).save('compare2.png')
# line plot
ln=Image.new('L',(1500,300),255); d=ImageDraw.Draw(ln)
d.line([(x*5,(y-20)*4.5) for x,y in zip(xs,vals)],fill=0)
ln.save('line2.png')
print(min(vals),max(vals))
