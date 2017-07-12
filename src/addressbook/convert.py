#!/usr/bin/env python3
import csv
import json
import os
from .addressbook import Addressbook, Contact

def to_structure(thing):
    """
    Returns a Contact or an Addressbook as a dict or list of dicts.

    >>> import addressbook
    >>> c = addressbook.Contact("John", "Doe",email="John@doe.org")
    >>> l = addressbook.to_structure(c)
    >>> len(l)
    3

    """
    if isinstance(thing,Addressbook):
        structure = [ to_structure(contact) for contact in thing]
    elif isinstance(thing,Contact):
        structure = { attr: getattr(thing,attr) for attr in thing.get_attrs() }
    else:
        structure = {"Not an addresbook"}
    return structure

def from_csv(csvfilename):
    """
    Read the contents of a csvfile into an addressbook

    >>> import addressbook
    >>> filename = "FakeNameGenerator.csv"
    >>> addressbook.from_csv(filename)
    <class Addressbook "csv imported", containing 0 contacts>


    <class Addressbook "csv imported", containing 257 contacts>
    """
    importsbook = Addressbook( "csv imported" )

    if os.path.exists(csvfilename):
        csv_config = Addressbook.configuration["csv columns"]
        skiplines = 1

        with open(csvfilename, 'rU') as csvfile:
            csv_content = csv.reader(csvfile,delimiter=',', quotechar='"')
            for row in csv_content:
                if skiplines > 0:
                    skiplines = skiplines - 1
                    next
                attrs = {}
                for label in csv_config:
                    col = int(csv_config[label])
                    # Since fname and sname are always there AND we need
                    # them to define a new contact, these are assigned
                    # separately from the list with the rest of the attributes.
                    if label == 'fname':
                        fname = row[col]
                    elif label == 'sname':
                        sname = row[col]
                    else:
                        attrs[label] = row[col]
                newcontact = Contact(fname, sname)
                for attr in attrs:
                    # Try to add them, if allowed they will:
                    attrData = attrs[attr]
                    newcontact.add_attr(attr,attrData)
                importsbook.add_contact( newcontact)
    return importsbook

def to_json(frombook, jsonfilename):
    """
    Write the content of an addressbook to a json file
    -- frombook is the source Addressbook.
    -- jsonfilename the name of the file to be generated.

    >>> import addressbook
    >>> ab = addressbook.Addressbook("My addressbook")
    >>> ab += addressbook.Contact("John", "Doe", mail="john@doe.nl")
    >>> ab += addressbook.Contact("Jane", "Doe", mail="jane@doe.nl")
    >>> addressbook.to_json(ab, "ab.json")
    'ab.json'

    """
    outData = {frombook.name:{}}
    outData[frombook.name]['allowed attributes'] = frombook.allowed_attrs_dict()
    outData[frombook.name]['Contacts'] = to_structure(frombook)

    with open(jsonfilename,'w') as jsonfile:
        json.dump(outData,jsonfile,indent=4)

    return jsonfilename

def convert_main (args):
    """This is an entry point to run some tests on this module"""
    import doctest

    doctest.testmod()

if __name__ == '__main__':
     sys.exit(convert_main(sys.argv))

