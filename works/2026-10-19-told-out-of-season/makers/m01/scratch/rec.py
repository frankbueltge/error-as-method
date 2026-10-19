from PIL import Image, ImageDraw
import json
im=Image.open('/tmp/claude-0/s137/mk/m01/work/record.jpg').convert('L'); W,H=im.size; p=im.load()
X0,X1=2.5,297.0; N=1464
xofh=lambda h: X0+h*(X1-X0)/(N-1)
PH=22
vals=[None]*N
starts=list(range(PH-24,N,24))
for a in starts:
    b=a+24; a2=max(a,0); b2=min(b,N)
    if b2<=a2: continue
    xa=xofh(a2)-0.5*(X1-X0)/(N-1); xb=xofh(b2-1)+0.5*(X1-X0)/(N-1)
    pts=[]
    for x in range(W):
        # fractional overlap of pixel column [x,x+1) w/ [xa,xb)
        ov=max(0,min(x+1,xb)-max(x,xa))
        if ov<=0: continue
        for y in range(H):
            w=max(0,190-p[x,y])
            if w>0: pts.append((y,w*ov))
    pts.sort()
    tot=sum(w for _,w in pts); n=b2-a2
    acc=0; qi=0; out=[]
    targets=[(i+0.5)/n*tot for i in range(n)]
    for y,w in pts:
        acc+=w
        while qi<n and acc>=targets[qi]:
            out.append(y); qi+=1
    while len(out)<n: out.append(pts[-1][0])
    for i,h in enumerate(range(a2,b2)): vals[h]=out[i]
v=[H-1-y for y in vals]
lo,hi=min(v),max(v); print(lo,hi)
norm=[round((x-lo)/(hi-lo),3) for x in v]
json.dump(norm,open('/tmp/claude-0/s137/mk/m01/scratch/series.json','w'))
img=Image.new('L',(W,H),255); d=ImageDraw.Draw(img)
for h,y in enumerate(vals): d.point((xofh(h),y),0)
img.resize((W*3,H*3)).save('/tmp/claude-0/s137/mk/m01/scratch/recon.png')
# daily summary
for k in range(0,61):
    seg=norm[k*24:(k+1)*24]
    print(k, round(max(seg),2), round(min(seg),2))
