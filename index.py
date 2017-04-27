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
import sys

from docopt import docopt


def do_info():
    pass

def do_serve(port):
    if port is None:
        port = '8080'
    else:
        try:
            port = int(port)
        except ValueError:
            print 'Port must be a valid number!'
            sys.exit(1)


    print 'Serving on port {0}.'.format(port)

if __name__ == '__main__':
    args = docopt(__doc__, version='index.py, version 0.0.0')

    if args['info']:
      do_info()

    if args['serve']:
      do_serve(port=args['--port'])