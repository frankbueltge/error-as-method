from PIL import Image
g=Image.open('/tmp/claude-0/s137/mk/m08/work/record.jpg').convert('L'); px=g.load()
W,H=g.size
x0,x1=2.0,297.0
def hour(x): return (x-x0)/(x1-x0)*1463
# per column: darkness-weighted centroid
bins={}
for x in range(3,205):
    ws=[(max(0,170-px[x,y]),y) for y in range(H)]
    s=sum(w for w,_ in ws)
    if not s: continue
    c=sum(w*y for w,y in ws)/s
    # local detrend: mean over +-5 px
    h=hour(x)%24
    b=int(h//3)
    bins.setdefault(b,[]).append(c)
# need detrended -> compute neighborhood mean
