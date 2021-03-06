#!/usr/bin/env python3
import csv
import json
import yaml
import os
from .addressbook import Addressbook, Contact

def from_csv(csvfilename, name="csv imported"):
    """
    Read the contents of a csvfile into an addressbook

    >>> import addressbook
    >>> filename = "FakeNameGenerator.csv"
    >>> addressbook.from_csv(filename)
    <class Addressbook "csv imported", containing 0 contacts>


    <class Addressbook "csv imported", containing 257 contacts>
    """
    importsbook = Addressbook( name )

    if os.path.exists(csvfilename):
        csv_config = Addressbook.configuration["csv columns"]
        skiplines = 1

        with open(csvfilename, 'rU') as csvfile:
            csv_content = csv.reader(csvfile,delimiter=',', quotechar='"')
            for row in csv_content:
                if skiplines > 0:
                    # Skip the first indicated number of rows/lines.
                    skiplines = skiplines - 1
                else:
                    #skiplines has become 0, continue reading the contacts.
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

def to_json(frombook, filename, **kargs):
    to_treeFormat(frombook, 'json', filename, **kargs)

def to_yaml(frombook, filename, **kargs):
    to_treeFormat(frombook, 'yaml', filename, **kargs)


def to_treeFormat(frombook,frmat, filename, **kargs):
    """
    Write the content of an addressbook to a treeformat file
    -- frombook is the source Addressbook.
    -- frmat is the requested format
    -- filename the name of the file to be generated.

    >>> import addressbook
    >>> ab = addressbook.Addressbook("My addressbook")
    >>> ab += addressbook.Contact("John", "Doe", mail="john@doe.nl")
    >>> ab += addressbook.Contact("Jane", "Doe", mail="jane@doe.nl")
    >>> addressbook.to_treeFormat(ab, "json", "ab.json")
    'ab.json'

    """
    outData = {frombook.name:{}}
    outData[frombook.name]['allowed attributes'] = frombook.allowed_attrs_dict()

    outData[frombook.name]['Contacts'] = frombook.to_list()

    with open(filename,'w') as outfile:
        if frmat == 'json':
            json.dump(outData,outfile,indent=4)
        elif frmat == 'yaml':
            yaml.dump(outData, outfile)

    return filename

def convert_main (args):
    """This is an entry point to run some tests on this module"""
    import doctest

    doctest.testmod()

if __name__ == '__main__':
     sys.exit(convert_main(sys.argv))

