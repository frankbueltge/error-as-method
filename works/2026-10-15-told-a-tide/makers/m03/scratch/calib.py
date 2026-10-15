from PIL import Image
import math,json
im=Image.open('/tmp/claude-0/s128/mk/m03/work/record.jpg').convert('L');px=im.load()
for x in list(range(0,8))+list(range(292,300)):
    print(x,[255-px[x,y] for y in range(90) if 255-px[x,y]>40])
d=json.load(open('cols.json'));cols=d['cols']
def amp(x0,x1,hrs):
    ser=[sum(w*max(0,y-42) for y,w in cols[x]) for x in range(300)]
    span=x1-x0
    m=sum(ser)/300;c=s=0
    for x in range(300):
        t=(x+0.5-x0)/span*1463
        c+=(ser[x]-m)*math.cos(2*math.pi*t/hrs);s+=(ser[x]-m)*math.sin(2*math.pi*t/hrs)
    return math.hypot(c,s)
best=max(((amp(2.5,296.5,h/100),h/100) for h in range(2380,2420)));print('best period h',best)
