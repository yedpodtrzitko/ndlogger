#!/usr/bin/python
import ndlogger
import os

from .server import serve_forever


def cli():
    serve_forever()


def bump_version():
    v = ndlogger.__version__
    new_version = v[:-1] + (v[-1] + 1,)
    new_version_str = '.'.join(map(str, new_version))
    initfile = os.path.join(os.path.dirname(ndlogger.__file__), '__init__.py')

    with open(initfile, 'r') as ifile:
        print("Reading old package init file...")
        istr = ifile.read()
        istr = istr.replace(str(v), str(new_version))

    with open(initfile, 'w') as ifile:
        print("Writing new init file with version %s..." % new_version_str)
        ifile.write(istr)


main = cli
