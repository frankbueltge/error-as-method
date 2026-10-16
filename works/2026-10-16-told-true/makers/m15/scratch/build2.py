import sys,json
t=open('template2.html').read()
c=json.load(open('curve.json'))
d=json.dumps({'v':c['v'],'out':[[o[0],o[1],o[2]] for o in c['out']]},separators=(',',':'))
params=dict(RDISC='390',ROUT='378',RIN='138',RLAB='108',A='0.22',L='0.55')
for a in sys.argv[2:]:
  k,v=a.split('=');params[k]=v
t=t.replace('__DATA__',d)
for k,v in params.items(): t=t.replace('__%s__'%k,v)
open(sys.argv[1],'w').write(t)
