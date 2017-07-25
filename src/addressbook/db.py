#!/usr/bin/python3

import addressbook
import sqlite3
import logging

# Generate a table called "contacts" with a unique ID and fname & sname.
# If one already exists: drop it first.
# The id is an numeric, unique one.
contacts_table = "contacts"
attrs_table = "attributes"
allowed_table = "allowed_attrs"

make_contacts_table = """
DROP TABLE IF EXISTS contacts;
CREATE TABLE %s (
    id      INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
    fname   CHAR(30),
    sname   CHAR(30)
);
"""%contacts_table

# Generate a table of allowed contacts.
make_allowed_attrs_table = """
DROP TABLE IF EXISTS allowed_attrs;
CREATE TABLE %s (
    attrname  CHAR(30) PRIMARY KEY UNIQUE     NOT NULL,
    desc      CHAR(255)
);
"""%allowed_table

make_attributes_table = """
DROP TABLE IF EXISTS attributes;
CREATE TABLE %s (
    id      INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
    contact INTEGER               NOT NULL,
    attr    CHAR(30)              NOT NULL,
    value   CHAR(255),
    FOREIGN KEY(contact) REFERENCES contacts(id),
    FOREIGN KEY(attr) REFERENCES allowed_attrs(attr)
);
"""%attrs_table

def initialize_addressbook_db_schema(connection):
    cursor = connection.cursor()
    cursor.executescript(make_contacts_table)
    cursor.executescript(make_allowed_attrs_table)
    cursor.executescript(make_attributes_table)
    connection.commit()


def write_allowed_attributes_to_db(addressbook,connection):
    cursor=connection.cursor()
    for attrname,description in addressbook.allowed_attrs_dict().items():

        insert_cmd = u"""
        INSERT INTO %s (attrname, desc) VALUES ('%s','%s')
        """%(allowed_table,attrname,description)

        cursor.execute(insert_cmd)
    connection.commit()

def write_contacts_to_db(addressbook,connection):
    cursor=connection.cursor()

    for contact in addressbook:

        insert_cmd = u"""
        INSERT INTO %s (fname, sname) VALUES ('%s','%s')
        """%(contacts_table,contact.fname,contact.sname)
        cursor.execute(insert_cmd)

        # This is None if executescript or some other method than
        # execute is used.
        contact._dbId = cursor.lastrowid
        # The contact was inserted into the contacts table.
        # this numeric ID is to be used in the atrributes table
        # to link the attributes to the proper contact.
    connection.commit()

def write_attrs_to_db(contact,connection):
        for attr in contact.get_attrs():
            cId = contact._dbId
            value = getattr(contact,attr)

            insert_cmd = u"""
            INSERT INTO %s (contact, attr, value) VALUES (%d,'%s','%s')
            """%(attrs_table,cId,attr,value)
            cursor.execute(insert_cmd)
    connection.commit()

if __name__ == "__main__":
    # initialize an addressbook:
    ab = addressbook.Addressbook()
    c1 = addressbook.Contact("John", "Doe",email="john@doe.org")
    c2 = addressbook.Contact("Jane", "Doe")
    c2.add_attr('phone', '+31(0)63414214')
    ab.add_contact(c1)
    ab.add_contact(c2)

    dbfilename = "./addressdb.db"
    connection = sqlite3.connect(dbfilename)

    initialize_addressbook_db_schema(connection)
    write_addressbook_to_db(ab,connection)



