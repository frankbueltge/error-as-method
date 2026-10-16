from PIL import Image; import numpy as np, json
im=np.array(Image.open('/tmp/claude-0/s131/mk/m06/work/record.jpg').convert('L')).astype(float)
d=255-im
cols=[]
for x in range(300):
    c=d[:,x]; ys=[]
    y=0
    while y<90:
        if c[y]>80:
            s=y; w=0; m=0
            while y<90 and c[y]>40: w+=c[y]; m+=c[y]*y; y+=1
            ys.append(round(m/w,1))
        y+=1
    cols.append(ys)
json.dump(cols,open('cols.json','w'))
for x in range(0,300):
    print(x,cols[x])
