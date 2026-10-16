from PIL import Image
im=Image.open('/tmp/claude-0/s130/mk/m13/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
D=lambda x,y: max(0,250-px[x,y]) if 0<=x<W else 0
pts=[]
for x in range(W):
    for y in range(H):
        dk=255-px[x,y]
        if dk>=40:
            q=min(9,dk//26)
            sw=D(x-1,y)+D(x,y)+D(x+1,y)
            cx=(D(x+1,y)-D(x-1,y))/sw if sw else 0   # -1..1 sub-pixel shift
            sub=max(0,min(9,round((cx+1)/2*9)))
            pts.append('%03d%02d%d%d'%(x,y,q,sub))
data=''.join(pts)
print(len(pts),'pixels',len(data),'chars')
tpl=open('/tmp/claude-0/s130/mk/m13/scratch/template.html').read()
open('/tmp/claude-0/s130/mk/m13/work/index.html','w').write(tpl.replace('__DATA__',data))
