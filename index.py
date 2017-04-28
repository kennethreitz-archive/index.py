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

import os
import multiprocessing
import sys


import crayons
import delegator
from docopt import docopt
from flask import Flask, request, abort
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

def yield_files(dir, endswith):
    for root, dirs, files in os.walk(dir):

        # Cleanup root.
        root = root[len(dir) + 1:]

        # Exclude directories that start with a period.
        if not root.startswith('.'):
            for file in files:
                if file.endswith(endswith):
                    yield os.sep.join((root, file))


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

def prepare_extras(request):
    extras = {}

    # 
    if request.json:
        extras.update(request.json)
    if request.form:    
        extras.update(request.form)
    
    if request.args:
        extras.update(request.args)

    extra = []

    for key, values in extras.items():
        for value in values:
            extra.append((key, value))
    
    return extra

def find(endswith, dir, path):
    found = None
    for fs_path in yield_files(dir, endswith):
        print '{0}{1}'.format(path, endswith) 
        print fs_path
        print
        if '{0}{1}'.format(path, endswith) in fs_path:
            return fs_path

def do_serve(dir, port):
    """Runs the 'serve' command, from the CLI."""

    # Convert dir and port to appropriate values.
    dir = convert_dir(dir)
    port = convert_port(port)

    app = Flask(__name__)

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):

        # Support for index.html.
        found = find('index.html', dir, path)
        
        # Support for index.py
        if not found:
            found = find('index.py', dir, path)

        # Support for directory listing.
        if not found:
            found = find('.py', dir, path)
        

        # A wild script was found!
        if found:
            if '.py' in found:
                extras = prepare_extras(request)
            
                for key, value in extras:
                    os.environ[key] = value
                
                c = delegator.run('python {0}'.format(found))

                for key, value in extras:
                    del os.environ[key]

                return c.out

            elif '.html' in found:
                with open(found) as html:
                    return html.read()

        else:
            abort(404)


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