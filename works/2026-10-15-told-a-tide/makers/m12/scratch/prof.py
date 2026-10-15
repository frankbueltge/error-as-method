from PIL import Image
im=Image.open('/tmp/claude-0/s128/mk/m12/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
def q(ws,p):
    t=sum(ws)*p; c=0
    for y,w in enumerate(ws):
        c+=w
        if c>=t: return y
out=[]
for x0 in range(0,W,5):
    ws=[0]*H
    for x in range(x0,min(W,x0+5)):
        for y in range(H):
            w=max(0,235-px[x,y]); ws[y]+=w
    tot=sum(ws)
    out.append((x0,round(tot/1000,1),q(ws,.05),q(ws,.25),q(ws,.5),q(ws,.75),q(ws,.95)))
for o in out: print(*o)
