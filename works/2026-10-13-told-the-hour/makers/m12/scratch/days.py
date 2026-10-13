from PIL import Image
im=Image.open('/tmp/claude-0/s123/mk/m12/work/record.jpg').convert('L')
W,H=im.size
x0,x1=3,297  # data extent approx
ppd=(x1-x0)/61
ink=[[max(0,240-im.getpixel((x,y))) for y in range(H)] for x in range(W)]
def q(ws,p):
    t=sum(ws); c=0
    for y,w in enumerate(ws):
        c+=w
        if c>=p*t: return y
for d in range(61):
    a=x0+d*ppd; b=a+ppd
    ws=[0]*H
    for x in range(int(a),int(b)+1):
        f=max(0,min(b,x+1)-max(a,x))
        for y in range(H): ws[y]+=f*ink[x][y]
    print(d, d%7, 'top',q(ws,.1),'med',q(ws,.5),'bot',q(ws,.9), round(sum(ws)))
