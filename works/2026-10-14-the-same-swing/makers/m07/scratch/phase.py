exec(open('cols.py').read().split("print(' '.join('%d'%")[0])
P=4.84
sm=[sum(mean[max(0,i-7):i+8])/len(mean[max(0,i-7):i+8]) for i in range(W)]
r=[mean[i]-sm[i] for i in range(W)]
nb=10; acc=[0]*nb; n=[0]*nb
for i in range(1,298):
  b=int(((i%P)/P)*nb)%nb; acc[b]+=r[i]; n[b]+=1
print([round(acc[b]/n[b],1) for b in range(nb)])  # image y: larger = lower value
