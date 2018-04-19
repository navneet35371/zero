import cherrypy
import os
import json
from utils import get_10_stocks, get_stock_by_name


class StockList(object):
    @cherrypy.expose
    def index(self):
        return open("index.html")

@cherrypy.expose
class StockListService(object):

    @cherrypy.tools.accept(media='text/plain')
    def GET(self):
        return json.dumps(get_10_stocks())


@cherrypy.expose
class StockSearchService(object):

    @cherrypy.tools.accept(media='text/plain')
    @cherrypy.tools.json_out()
    def GET(self, q):
        return get_stock_by_name(q)

if __name__ == "__main__":

    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': int(os.environ.get('PORT', 5000))
        },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/stocks': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/stocks/search': {
            'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
            'tools.response_headers.on': True,
            'tools.response_headers.headers': [('Content-Type', 'text/plain')],
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'public'
        }
    }
    webapp = StockList()
    webapp.stocks = StockListService()
    webapp.stocks.search = StockSearchService()
    cherrypy.quickstart(webapp, '/', conf)
