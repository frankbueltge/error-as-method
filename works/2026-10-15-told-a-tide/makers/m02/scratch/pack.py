from PIL import Image
import math, json
im=Image.open('/tmp/claude-0/s128/mk/m02/work/record.jpg').convert('L'); px=im.load()
W,H=im.size
s=''.join('0123456789abcdef'[min(15,round(max(0,235-px[x,y])/235*15))] for y in range(H) for x in range(W))
open('/tmp/claude-0/s128/mk/m02/scratch/pix.txt','w').write(s)
x0=2.5; hpp=1463/294.0
# sinusoid fit on column mean y at 24h
cols=json.load(open('/tmp/claude-0/s128/mk/m02/scratch/cols.json'))
v=[c[4] for c in cols]; m=sum(v)/W
C=sum((v[x]-m)*math.cos(2*math.pi*(x-x0)*hpp/24) for x in range(W)); S=sum((v[x]-m)*math.sin(2*math.pi*(x-x0)*hpp/24) for x in range(W))
ph=math.atan2(S,C)%(2*math.pi)
print('phase of lowest values (hours after first sample): %.2f'%(ph/2/math.pi*24), 'amp', 2*math.hypot(C,S)/W)
print(len(s), s.count('0'))
