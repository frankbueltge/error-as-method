import json
ys=json.load(open('/tmp/claude-0/s133/mk/m13/scratch/ys.json'))
v=[max(0,(84-y)/78) for y in ys]
for d in range(61):
    print('%2d '%d+' '.join('%3d'%round(100*v[24*d+h]) for h in range(24)))
