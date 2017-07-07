#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Module docstring goes here"""

from __future__ import print_function
import sys

from .addressbook import *
from .db import *

__author__ = 'Hans de Jonge'
__version__ = '0.1'
__date__ = '20170607'
__license__ = 'GNU gplv3'

__all__ = [ ]

def init_main(args):
    """The main function is the entry point of a program"""
    # main is separated out into a function so that it too can be thoroughly
    # tested.
    return 0

if __name__ == '__main__':
    # This is the main body of this module. Ideally it should only contain at
    # most **one** call to the entry point of the program.
    sys.exit(init_main(sys.argv))

# vim: tabstop=9 expandtab shiftwidth=4 softtabstop=4 showbreak=…

