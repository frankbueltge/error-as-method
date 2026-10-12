from PIL import Image
im=Image.open('/tmp/claude-0/s122/mk/m11/work/record.jpg').convert('L')
W,H,N=19,6,1464
L,T,PW,PH=70,96,960,564; rh=PH/H
out=Image.new('L',(1100,800),250); p=out.load()
for h in range(N):
    col=min(W-1,h*W//N); px=int(L+(h+.5)*PW/N)
    for r in range(H):
        d=(255-im.getpixel((col,r)))/255
        for y in range(int(T+r*rh),int(T+(r+1)*rh)):
            p[px,y]=int(p[px,y]*(1-.62*d*.8))
out.save('/tmp/claude-0/s122/mk/m11/scratch/preview.png')
