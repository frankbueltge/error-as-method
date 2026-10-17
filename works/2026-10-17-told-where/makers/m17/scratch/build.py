d=open('/tmp/claude-0/s133/mk/m17/scratch/data.json').read()
t=open('/tmp/claude-0/s133/mk/m17/scratch/template.html').read().replace('__DATA__',d)
open('/tmp/claude-0/s133/mk/m17/work/index.html','w').write(t)
