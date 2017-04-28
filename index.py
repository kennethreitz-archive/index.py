"""index.py

Usage:
  index.py serve <dir>
  index.py serve <dir> [--port=<port>]
  index.py info <dir>
  index.py (-h | --help)
  index.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.
  --port=<port> Port to bind to [default: 8080].
"""
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import multiprocessing
import sys


import crayons
from docopt import docopt
from flask import Flask, request
from gunicorn import util
from gunicorn.app.base import Application
from livereload import Server as ReloadServer
from whitenoise import WhiteNoise


# \
#  \ji
#  /.(((
#  (,/"(((__,--.
#     \  ) _( /{
#      !|| " :||
#      !||   :||
#       '''   '''


def number_of_workers():
    return multiprocessing.cpu_count() + 1

def yield_fs(dir):
    for root, dirs, files in os.walk(dir):

        # Cleanup root.
        root = root[len(dir) + 1:]

        # Exclude directories that start with a period.
        if not root.startswith('.'):
            for file in files:
                if not file.endswith('.py'):
                    yield os.sep.join((root, file))
            # if not result.startswith('.'):
                # yield result

def fs_map(dir):
    print('Valid paths:')
    for file in yield_fs(dir):
        print(file)

    return dir







def do_info():
    """Runs the 'info' command, from the CLI."""
    pass


def convert_dir(dir):
    dir = os.path.abspath(dir)
    try:
        assert os.path.isdir(dir)
    except AssertionError:
        print(crayons.red('The directory given must be a valid one!'))
        sys.exit(1)

    return dir

def convert_port(port):
    if port is None:
        port = '8080'
    else:
        try:
            port = int(port)
        except ValueError:
            print(crayons.red('The port given must be a valid number!'))
            sys.exit(1)

    return port

def do_serve(dir, port):
    """Runs the 'serve' command, from the CLI."""

    # Convert dir and port to appropriate values.
    dir = convert_dir(dir)
    port = convert_port(port)

    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.before_request
    def before_request():
        app.add_files(dir, prefix='/')

    @app.after_request
    def after_request(response):
        response.headers['X-Powered-By'] = 'index.py by Kenneth Reitz'
        return response

    app = WhiteNoise(app, root=dir)
    server = ReloadServer(app)
    server.watch('{0}/**'.format(dir))

    # Alert the user.
    print(crayons.yellow('Serving up \'{0}\' on port {1}.'.format(dir, port)))
    server.serve(port=port)


def main():
    args = docopt(__doc__, version='index.py, version 0.0.0')

    if args['info']:
      do_info()

    if args['serve']:
      do_serve(dir=args['<dir>'], port=args['--port'])


if __name__ == '__main__':
    main()