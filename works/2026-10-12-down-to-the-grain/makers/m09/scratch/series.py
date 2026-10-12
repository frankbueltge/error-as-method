import json
pk=json.load(open('/tmp/claude-0/s122/mk/m09/scratch/peaks.json'))
x0=pk[0][0]; s=(pk[-1][0]-x0)/1463
N=1464; slots=[[] for _ in range(N)]
# greedy assign: sort by x, assign sequential slot nearest, no collisions
for p in pk:
  t=(p[0]-x0)/s
  i=int(round(t-0.2))
  i=max(0,min(N-1,i))
  slots[i].append(p)
# resolve collisions: move extras to empty neighbour
for i in range(N):
  while len(slots[i])>1:
    slots[i].sort()
    if i+1<N and not slots[i+1]: slots[i+1].append(slots[i].pop())
    elif i>0 and not slots[i-1]: slots[i-1].append(slots[i].pop(0))
    else: break
coll=sum(1 for sl in slots if len(sl)>1); empty=sum(1 for sl in slots if not sl)
print('collisions',coll,'empty',empty)
ys=[ (sum(p[1] for p in sl)/len(sl) if sl else None) for sl in slots]
# value = 360 - y (pixel height); interpolate empties
v=[None if y is None else 360-y for y in ys]
known=[i for i in range(N) if v[i] is not None]
filled=v[:]
for i in range(N):
  if v[i] is None:
    a=max([k for k in known if k<i],default=None); b=min([k for k in known if k>i],default=None)
    if a is None: filled[i]=v[b]
    elif b is None: filled[i]=v[a]
    else: filled[i]=v[a]+(v[b]-v[a])*(i-a)/(b-a)
json.dump({'v':[round(x,1) for x in filled],'measured':[x is not None for x in v]},open('/tmp/claude-0/s122/mk/m09/scratch/series.json','w'))
# mean diurnal profile
prof=[sum(filled[d*24+h] for d in range(61))/61 for h in range(24)]
print('profile',[round(p) for p in prof])
for d in (0,1,20,43,44,45,46,54,55):
  print(d,[round(filled[d*24+h]) for h in range(24)])
