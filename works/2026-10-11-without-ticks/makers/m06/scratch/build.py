import sys
P=dict(RIN='88',K='1.62',C0='38,84,140',C1='176,62,36',ALPHA='0.30',LW='1.7')
for a in sys.argv[1:]:
  k,v=a.split('=',1);P[k]=v
t=open('template.html').read().replace('__DATA__',open('pts.b64').read().strip())
for k,v in P.items(): t=t.replace('__%s__'%k,v)
open('/tmp/claude-0/s121/mk/m06/work/index.html','w').write(t)
