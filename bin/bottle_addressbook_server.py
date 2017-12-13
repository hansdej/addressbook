#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Module docstring goes here"""
import sys,argparse
import logging
import logging.config
logging.basicConfig(
    filename = 'bottle-ab.log',
    format = '%(module)s:%(lineno)d: %(message)s',
    level = logging.DEBUG
)
import configparser

__author__ = 'Hans de Jonge'
__version__ = ''
__date__ = ''
__license__ = 'Gpl'

__all__ = [ ]

from addressbook import Addressbook
import addressbook
from addressbook.convert import *
from bottle import route, run
import json

@route('/addressbook/sample/')
def parse_addressbook_json(addressbk=None):
    """
    Parse an addressbook in JSON format

    """
    if addressbk is None:
        csvfile = "Data/FakeNameGenerator.csv"
        ab = addressbook.from_csv(csvfile, name = "My addressboek")
    else:
        ab = addressbk
    output = "["
    for record in addressbook.convert.to_structure(ab):
        output += "%s\n"%json.dumps(record,indent=4)
    output += "]"
    output = json.dumps( addressbook.convert.to_structure(ab),indent=4)

    return output
# Wa

def start_bottle():
    """
    """
    #set things ready:
    fallbackPort = 8081
    # Do the config loading part:
    c_parser = configparser.ConfigParser()
    try:
        c_parser.read("bottle-ab.ini")
    except TypeError as error:
        logging.warning("Error parsing config files: no files provided")
    except Exception as error:
        logging.error("Error parsing config files:")
        logging.error(error)
        exit(10)

    # A bit of option gymnastics, just as a reminder that this also works.
    config = { sect: { opt:c_parser.get(sect,opt) for opt in c_parser.options(sect)}
                                    for sect in c_parser.sections()}
    try:
        portNo = int(config['server']['port'])
    except KeyError as error:
        portNo = fallbackPort
        warning  = "No configured portnumber found, falling back on "
        warning += "portnumber %s"%port
        logging.warning(warning)

    run(host='localhost', port=portNo, debug=True)
    return 0


def main(args):
    """The main function is the entry point of a program"""
    # main is separated out into a function so that it too can be thoroughly
    # tested.
    start_bottle()
    return 0

if __name__ == '__main__':
    # This is the main body of this module. Ideally it should only contain at
    # most **one** call to the entry point of the program.
    sys.exit(main(sys.argv))


