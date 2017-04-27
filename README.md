# index.py: Oldschool Web Development for Humans

I miss the 'ol PHP/Apache days of throwing random files/folders on a web server.
I want to try to bring that back to Python land (maybe).

This is an experiment — it might not go very far.

## The Concept

- You can shove shit in a directory, and it'll just get served automatically.
- Use flask (or any other WSGI framework) if you want to, no configuration needed.
- No maintinence/deployment required to make changes — just make changes to the filesystem.

The real end goal here is to have a Python application running at playground.kennethreitz.org on a
digital ocean box that can be used to host all sorts of applications and random files for fun, just
by managing the filesystem — like it was in the PHP days.

## Basic Structure of a Deployment

Subject to (vastly) change:

    root/index.py <-- provides infrasctructure for whole application
    root/sometoy/randofile <-- gets served
    root/sometoy/index.py <-- gets run automatically for this path, could be Flask.
