# Usage:
# bin/(zeo|zope)ctl run path/to/this/script <plonesitename> <content type>
#
# Example:
# bin/zeoctl run /tmp/upgrade-youtube-embeds.py Plone 'News Item'
#
# The script will then shortly ask you for the Plone site ID to migrate
# and the content type you want to migrate.

import re
import sys
import transaction

# Usage:
# bin/(zeo|zope)ctl run path/to/this/script <plonesitename>

import re
import transaction

exp = re.compile("(<object.*?youtube.*?</object>)|(<embed.*?youtube.*?</embed>)", re.S)
idid = re.compile("youtube.com/v/(.+?)[\"&?]")
repf = lambda i: '<iframe width="560" height="315" src="https://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>'%i

site = raw_input("Plone site ID (default Plone): ")
if not site:
    site = "Plone"
portal_type = raw_input("Content type (default News Item): ")
if not portal_type:
    portal_type = "News Item"

cat = app[site].portal_catalog
res = cat.searchResults({'portal_type': portal_type})
for x in res:
    obj = x.getObject()
    text = obj.getText()
    matches = exp.findall(text)
    if matches:
        print x.getPath(), "matches"
        for match in matches:
            print "   text:", repr(match[0])
            try:
                vidid = idid.findall(match[0])[0]
            except IndexError:
                print "   norepl"
                continue
            repl = repf(vidid)
            print "   repl:", repr(repl)
            text = text.replace(match[0], repl)
        obj.setText(text)
        obj.reindexObject()
transaction.commit()exp = re.compile("(<object.*?youtube.*?</object>)|(<embed.*?youtube.*?</embed>)", re.S)
idid = re.compile("youtube.com/v/(.+?)[\"&?]")
repf = lambda i: '<iframe width="560" height="315" src="https://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>'%i

cat = app[sys.argv[3]].portal_catalog
res = cat.searchResults({'portal_type': sys.argv[4]})
for x in res:
    obj = x.getObject()
    text = obj.getText()
    matches = exp.findall(text)
    if matches:
        print x.getPath(), "matches"
        for match in matches:
            print "   text:", repr(match[0])
            try:
                vidid = idid.findall(match[0])[0]
            except IndexError:
                print "   norepl"
                continue
            repl = repf(vidid)
            print "   repl:", repr(repl)
            text = text.replace(match[0], repl)
        obj.setText(text)
        obj.reindexObject()
transaction.commit()
