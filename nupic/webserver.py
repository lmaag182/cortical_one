import sys
from twisted.web.server import Site
from twisted.web.static import File
from twisted.internet import reactor

if len(sys.argv)>1:
    resource = sys.argv[1]
else:
    resource = '/home/hans/ownCloud/Documents/code/cortical_one/web/html5UI/public_html/'    #in case we are in the project structure

resource = File(resource)
factory = Site(resource)
reactor.listenTCP(8888, factory)
reactor.run()