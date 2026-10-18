import json
f=json.load(open('fit_2.1_0.85.json')); ys=f['ys']
z=84.0
v=[max(0,(z-y)) for y in ys]
v=[0 if a<=1.0 else a for a in v]
days=[v[d*24:(d+1)*24] for d in range(61)]
prof=[sum(days[d][h] for d in range(61))/61 for h in range(24)]
print('mean by hour index:',' '.join('%d:%.0f'%(h,a) for h,a in enumerate(prof)))
print('zero count by hour:',' '.join('%d:%d'%(h,sum(1 for d in range(61) if days[d][h]==0)) for h in range(24)))
# daily stats with day defined from 07 index (solar midnight) 
for d in range(61):
    seg=v[d*24+7:(d+1)*24+7]
    nz=sum(1 for a in seg if a>0)
    print(d, 'max %4.1f sum %6.1f nz %2d'%(max(seg),sum(seg),nz), ''.join(' .:-=+*#%@'[min(9,int(a/8))] for a in seg))
