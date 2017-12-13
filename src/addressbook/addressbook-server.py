#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module docstring goes here"""
import sys,os,argparse

__author__ = 'Hans de Jonge'
__version__ = ''
__date__ = ''
__license__ = 'Gpl'

__all__ = [ ]

from addressbook import Contact, Addressbook
from bottle import route, run, template
from addressbook.convert import *
import json

@route('/addressbook/sample/<name>')
def index(name):
    c1 = Contact(fname='John', sname='Doe')
    c1.add_attr('email', 'jdoe@example.com')
    c1.add_attr('phone', '+31-123-456-789')

    c2 = Contact(fname='Jane', sname='Brown')
    c2.add_attr('email', 'jane.brown@example.com')
    c2.add_attr('phone', '+31-987-654-321')
    c2.add_attr('birthday', 'Jan 1')

    ab = Addressbook(name)
    ab.add_contact(c1)
    ab.add_contact(c2)
    return json.dumps(convert_to_struct(ab))


def main(args):
    """The main function is the entry point of a program"""
    # main is separated out into a function so that it too can be thoroughly
    # tested.
    return 0

if __name__ == '__main__':
    # This is the main body of this module. Ideally it should only contain at
    # most **one** call to the entry point of the program.
    sys.exit(main(sys.argv))


