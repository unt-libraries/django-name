from pynaco.naco import normalizeSimplified
import urllib2
from name.models import Name

dupe = 0

f = open('/home/jliechty/names_2013-02-04.tsv', 'r')

for line in f:

    line = line.split('\t')
    naco = normalizeSimplified(line[1])
    host = 'libdigital2test.library.unt.edu'
    # FIXME: Remove hardcoded URL
    path = '/name/label/' + naco
    try:
        conn = urllib2.urlopen('http://%s%s' % (host, urllib2.quote(path)))

    except urllib2.HTTPError, e:

        if e.code == 404:

            numeric_type = 0

            if line[0] == 'organization':
                numeric_type = 1
            elif line[0] == 'event':
                numeric_type = 2
            elif line[0] == 'software':
                numeric_type = 3

            n = Name(name=line[1].strip('\n'), name_type=numeric_type)
            n.save()

            print 'record doesn\'t yet exist. saved %s, %s' %\
                (normalizeSimplified(line[1].strip('\n')), line[0])

        elif e.code in (302, 301):

            print 'record exists already. not added.'
            dupe += 1

print str(dupe) + " duplicates omitted from creation."
