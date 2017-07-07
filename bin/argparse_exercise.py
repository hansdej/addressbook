#!/usr/bin/env python3
import sys
import argparse
import addressbook
import logging
logging.basicConfig(
        level = logging.DEBUG
        )

parser = argparse.ArgumentParser()
parser.add_argument( '-n', '--name',
                help='The name of the new addressbook',
                nargs=1,
                default = None,
                type= str
                )
parser.add_argument( '-f', '--firstname',
                help='The first name of the new contact.',
                default = None,
                type= str
                )
parser.add_argument( '-s', '--surname',
                help='The family name of the new contact.',
                default = None,
                type= str
                )
parser.add_argument( '-a', '--attr',
                help='add extra attribute to the contact',
                nargs = 2,
                default = [None,None],
                metavar = str
                )
cliargs = parser.parse_args()


# I used one script to solve both problems: linked them (either hard or soft)
# to one main script and use the called filename to determine which behaviour is used.
# (I like to split related scripts as late as possible: I find maintenance easier with
# all associate, equal level Code in one file.
logging.debug('Program was called as \'%s\''%(sys.argv[0]))
logging.debug('with arguments:%s'%cliargs)

if "create_contact" in sys.argv[0]:
    fname = cliargs.firstname
    sname = cliargs.surname
    extra_attrs = cliargs.attr

    if sname is None or sname is None:
        logging.error("first- & family name arguments are obligatory for new Contacts\nExiting")
        exit(10)
    # Script was called via the create_contact filename.
    # Create the Contact:
    c = addressbook.Contact(fname,sname)
    c.add_attr(extra_attrs[0], extra_attrs[1])
    # Display the contact:
    logging.debug(c)
    # Crudely display the attributes
    for attribute in addressbook.attributes(c):
        label = c._allowed_attributes[attribute]
        value = getattr(c, attribute)
        logging.debug("\t%s \t=> [%s]"%(label,value))

elif "create_addrbook" in sys.argv[0]:
    name = cliargs.name

    logging.debug('found addressbookname: \'%s\''%name)
    if name is not None:
        logging.debug('Creating addressbook \'%s\''%name)
        ab = addressbook.Addressbook(name=name)
    else:
        ab = addressbook.Addressbook()

    logging.debug("Addressbook creation was called as %s"%sys.argv[0])
    logging.debug("To create the addressbook %s"%ab)
    logging.debug("with contacts:")
    if len(ab) == 0:
        logging.debug("<None>")
    else:
        for c in ab:
            logging.debug(c)

