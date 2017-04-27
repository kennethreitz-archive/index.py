"""index.py

Usage:
  index.py serve <dir>
  index.py serve <dir> [--port=<port>]
  index.py info
  index.py (-h | --help)
  index.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --port=<port> Port to bind to [default: 8080].
"""
# -*- coding: utf-8 -*-

import sys

from docopt import docopt
from flask import Flask, request
from gunicorn import util
from gunicorn.app.base import Application


# \
#  \ji
#  /.(((
#  (,/"(((__,--.
#     \  ) _( /{
#      !|| " :||
#      !||   :||
#       '''   '''

class WSGIApp(Application):

    def __init__(self, application, options={}):
        """ Construct the Application. Default gUnicorn configuration is loaded """

        self.application = application
        self.usage = None
        self.callable = None
        self.options = options
        self.prog = None
        self.do_load_config()

    def init(self, parser, opts, args):
        """ Apply our custom settings """

        cfg = {}
        for k, v in self.options.items():
            if k.lower() in self.cfg.settings and v is not None:
                cfg[k.lower()] = v
        return cfg

    def load(self):
        """ Attempt an import of the specified application """

        if isinstance(self.application,str):
            return util.import_app(self.application)
        else:
            return self.application

class GunicornMeat(object):

    def __init__(self,app,**options):
        """ Construct our application """

        self.app = WSGIApp(app, options)

    def run(self):
        """ Run our application """

        self.app.run()


app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.after_request
def after_request(response):
    response.headers['X-Powered-By'] = 'index.py by Kenneth Reitz'
    return response


def do_info():
    """Runs the 'info' command, from the CLI."""
    pass

def do_serve(port):
    """Runs the 'serve' command, from the CLI."""
    if port is None:
        port = '8080'
    else:
        try:
            port = int(port)
        except ValueError:
            print 'Port must be a valid number!'
            sys.exit(1)

    print 'Serving on port {0}.'.format(port)
    server = GunicornMeat(app=app, workers=4, type='sync')
    server.run()

def main():
    args = docopt(__doc__, version='index.py, version 0.0.0')

    if args['info']:
      do_info()

    if args['serve']:
      do_serve(port=args['--port'])


if __name__ == '__main__':
    main()