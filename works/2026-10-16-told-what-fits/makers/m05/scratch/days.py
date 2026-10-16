from PIL import Image; import numpy as np, json
im=np.array(Image.open('/tmp/claude-0/s131/mk/m05/work/record.jpg').convert('L')).astype(float)
H,W=im.shape
ink=np.clip((235-im)/235.0,0,1)
cols=np.where((im<128).any(0))[0]; x0,x1=cols[0]-0.5,cols[-1]+0.5
span=x1-x0; D=61
profs=[];stats=[]
for d in range(D):
    a=x0+d*span/D; b=a+span/D
    p=np.zeros(H)
    for x in range(W):
        ov=max(0,min(b,x+0.5)-max(a,x-0.5))  # pixel x covers [x-.5,x+.5]
        if ov>0: p+=ov*ink[:,x]
    p/=span/D
    yy=np.where(p>0.12)[0]
    top,bot=int(yy.min()),int(yy.max())
    profs.append(p); stats.append((top,bot))
    print(d, top, bot, bot-top, round(p.sum(),1))
json.dump({'H':H,'stats':stats,'prof':[[round(float(v),3) for v in p] for p in profs]},open('days.json','w'))
