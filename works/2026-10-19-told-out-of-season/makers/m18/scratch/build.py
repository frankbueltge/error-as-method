from PIL import Image
im=Image.open('/tmp/claude-0/s137/mk/m18/work/record.jpg').convert('L')
W,H=im.size; px=im.load()
X0,X1=2.0,297.0   # horizontal extent of the record in the picture
Y0,Y1=3,87        # vertical band holding all ink (top=high values)
D,S=61,6          # days, strips per day (~4 h each)
def ink(x,y):
    v=(232-px[x,y])/150.0
    return 0.0 if v<0 else min(1.0,v)
rows=[]
for d in range(D):
    for s in range(S):
        a=X0+(X1-X0)*(d*S+s)/(D*S); b=X0+(X1-X0)*(d*S+s+1)/(D*S)
        col=[]
        for y in range(Y1,Y0-1,-1):   # low values first
            acc=0;wt=0
            for x in range(int(a),int(b)+1):
                ov=max(0,min(b,x+1)-max(a,x))
                if ov>0 and x<W: acc+=ink(x,y)*ov; wt+=ov
            col.append(acc/wt if wt else 0)
        rows.append(''.join(str(min(9,round(v*9))) for v in col))
data='|'.join(rows)
tpl=open('template.html').read()
open('/tmp/claude-0/s137/mk/m18/work/index.html','w').write(tpl.replace('__DATA__',data).replace('__S__',str(S)).replace('__N__',str(Y1-Y0+1)))
print(len(data))
