from PIL import Image
im=Image.open('/tmp/claude-0/s123/mk/m12/work/record.jpg').convert('L')
W,H=im.size
x0,x1=3,297; ppd=(x1-x0)/61
work={d for d in range(61) if d%7 not in (0,1) and d not in (37,38,39,40,41,44,45,46,47,48)}
bins={}
for x in range(x0,x1):
    c=x+0.5-x0; d=int(c//ppd); ph=(c%ppd)/ppd*24
    ws=[max(0,240-im.getpixel((x,y))) for y in range(H)]
    t=sum(ws); m=sum(y*w for y,w in enumerate(ws))/t
    k=int(ph//2)*2
    bins.setdefault((d in work,k),[]).append(m)
for (w,k),v in sorted(bins.items()): print(w,k,len(v),round(sum(v)/len(v),1))
