import sys
t=open('template.html').read()
d=open('data.txt').read()
params=dict(CX='550',R0='38',S='5.6',A='0.35')
for a in sys.argv[2:]:
  k,v=a.split('=');params[k]=v
t=t.replace('__DATA__',d)
for k,v in params.items(): t=t.replace('__%s__'%k,v)
open(sys.argv[1],'w').write(t)
