from PIL import Image
P=[int(v) for v in open('scratch/px.txt').read().split(',')]
ink=lambda c,r:max(0,min(1,(1-P[r*40+c]/255-0.06)/0.9))*0.92
W,H=1000,600; im=Image.new('L',(W,H),243)
for x in range(W):
    col=int(int(x/W*1464)*40/1464)
    for y in range(H):
        f=(y+0.5)/H*12-0.5; r0=max(0,min(11,int(f//1))); r1=min(11,r0+1); t=max(0,min(1,f-r0))
        a=(ink(col,r0)*(1-t)+ink(col,r1)*t)*0.62
        im.putpixel((x,y),int(243*(1-a)+28*a))
im.save('scratch/preview.png')
