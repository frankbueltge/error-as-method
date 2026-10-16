from PIL import Image; import numpy as np
im=255-np.array(Image.open('/tmp/claude-0/s131/mk/m13/work/record.jpg').convert('L')).astype(float)
d=im*(im>60)
nz=np.where(d.sum(0)>0)[0]; print('x range',nz.min(),nz.max()); ny=np.where(d.sum(1)>0)[0]; print('y range',ny.min(),ny.max())
for x in range(int(__import__('sys').argv[1]),int(__import__('sys').argv[2])):
    col=d[:,x]
    # blob runs
    runs=[];y=0
    while y<90:
        if col[y]>0:
            s=y
            while y<90 and col[y]>0: y+=1
            w=col[s:y]; runs.append((round((w*np.arange(s,y)).sum()/w.sum(),1), y-s, int(w.sum())))
        y+=1
    print(x, runs)
