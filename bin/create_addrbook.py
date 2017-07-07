#!/usr/bin/env python3
import argparse
import addressbook
import logging

loggin.debug("""Python advanced: The simple solution to exercise 7.4-1:
        \tscript addressbook creation with argparsed arguments.""")

parser = argparse.ArgumentParser()
parser.add_argument( '-n', '--name',
                help='The name of the initialised addressbook.',
                nargs = '?', type=str
                )

cliargs = parser.parse_args()
addressbookName = cliargs.name

if addressbook is None:
    ab = addressbook.Addressbook()
else:
    ab = addressbook.Addressbook(addressbookName)

