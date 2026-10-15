from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m12/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
X0,X1=1,297
hp=1463/(X1-X0)   # hours per px
def fold(P,nb=24):
    bins=[[0]*H for _ in range(nb)]
    for x in range(W):
        for y in range(H):
            w=max(0,235-px[x,y])
            if not w: continue
            for s in range(10):
                t=(x-0.5+(s+.5)/10-X0)*hp
                b=int((t%P)/P*nb)%nb
                bins[b][y]+=w/10
    for b in range(nb):
        ws=bins[b]; t=sum(ws)
        m=sum(y*w for y,w in enumerate(ws))/t
        # quantiles
        def q(p):
            c=0
            for y,w in enumerate(ws):
                c+=w
                if c>=t*p: return y
        print(P,b,round(m,1),q(.1),q(.25),q(.5),q(.75),q(.9))
fold(24.0); fold(24.84); fold(12.42,12)
