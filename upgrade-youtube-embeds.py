# Usage:
# bin/(zeo|zope)ctl run path/to/this/script <plonesitename> <content type>
#
# Example:
# bin/zeoctl run /tmp/upgrade-youtube-embeds.py Plone 'News Item'
#
# The script will then shortly ask you for the Plone site ID to migrate
# and the content type you want to migrate.

import re
import transaction

vid = dict(
    exp = re.compile("(<object.*?youtube.com/v.*?</object>)|(<embed.*?youtube.com/v.*?</embed>)", re.S),
    id = re.compile("youtube.com/v/(.+?)[\"&?]"),
    rep = lambda i: '<iframe width="560" height="315" src="https://www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>'%i,
)

pl = dict(
    exp = re.compile("(<object.*?youtube.com/p.*?</object>)|(<embed.*?youtube.com/p.*?</embed>)", re.S),
    id = re.compile("youtube.com/p/(.+?)[\"&?]"),
    rep = lambda i: '<iframe width="560" height="315" src="https://www.youtube.com/embed/videoseries?list=PL%s" frameborder="0" allowfullscreen></iframe>'%i,
)

tls = dict(
    exp = re.compile("(http://www.youtube.com/)|(http://youtube.com/)", re.S),
    id = re.compile("(/www.youtube.com|/youtube.com)"),
    rep = lambda i: 'https:/%s/'%i,
)

site = raw_input("Plone site ID (default Plone): ")
if not site:
    site = "Plone"
portal_type = raw_input("Content type (default News Item): ")
if not portal_type:
    portal_type = "News Item"

cat = app.unrestrictedTraverse(site).portal_catalog
res = cat.searchResults({'portal_type': portal_type})
for x in res:
    obj = x.getObject()
    text = obj.getText()
    for typ in (vid, pl, tls):
        matches = typ['exp'].findall(text)
        if matches:
            repl = True
            print x.getPath(), "matches"
            for match in matches:
                print "   text:", repr(match[0])
                try:
                    vidid = typ['id'].findall(match[0])[0]
                except IndexError:
                    print "   norepl"
                    continue
                repl = typ['rep'](vidid)
                print "   repl:", repr(repl)
                text = text.replace(match[0], repl)
    if text != obj.getText():
        obj.setText(text)
        obj.reindexObject()

q = raw_input("Commit these changes [Ny]? ")
if q in 'yY':
    transaction.commit()
