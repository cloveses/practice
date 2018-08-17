import json
import os

import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
from tornado.web import RequestHandler, url, StaticFileHandler
from tornado.options import define, options

define("port", default=8000, type=int)


class IndexHandler(RequestHandler):
    def get(self):
        self.write('<a href="/itcast">itcast</a>')


class ItcastHandler(RequestHandler):
    def get(self):
        self.write(dict(a=1, b=2))
        
settings={
'static_path': os.path.join(os.path.dirname(__file__), "static"),
'debug': True,
}

if __name__ == "__main__":
    tornado.options.parse_command_line()
    current_path = os.path.dirname(__file__)
    app = tornado.web.Application(handlers=[
    (r"/itcast", IndexHandler),
    (r"/asd/(.*)", StaticFileHandler, {"path": os.path.join(current_path, "static/html"),
    "default_filename": "index.html"}),
    ], **settings)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.current().start()