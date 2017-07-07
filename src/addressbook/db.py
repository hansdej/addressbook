#!/usr/bin/python3

import addressbook
import sqlite3

make_contacts_table = """
DROP TABLE IF EXISTS contacts;
CREATE TABLE contacts (
    id      INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
    fname   CHAR(30),
    sname   CHAR(30)
);
"""

make_allowed_attrs_table = """
DROP TABLE IF EXISTS allowed_attrs;
CREATE TABLE allowed_attrs (
    attrname  CHAR(30) PRIMARY KEY UNIQUE     NOT NULL,
    desc      CHAR(255)
);
"""

make_attributes_table = """
DROP TABLE IF EXISTS attributes;
CREATE TABLE attributes (
    id      INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
    contact INTEGER               NOT NULL,
    attr    CHAR(30)              NOT NULL,
    value   CHAR(255),
    FOREIGN KEY(contact) REFERENCES contacts(id),
    FOREIGN KEY(attr) REFERENCES allowed_attrs(attr)
);
"""

def initialize_addressbook_db_schema(connection):
    cursor = connection.cursor()
    cursor.executescript(make_contacts_table)
    cursor.executescript(make_allowed_attrs_table)
    cursor.executescript(make_attributes_table)
    cursor.commit()

def write_addressbook_to_db(addressbook,connection):
    cursor=connection.cursor()
    for contact in addressbook:
        insert_cmd = u"""
        INSERT INTO contacts (contact, fname, sname) VALUES "(%s,%s)"
        """
        contact_id = cursor.lastrowid
        # The contact was inserted into the contacts table and we got
        # its id in this table that can be used in the atrributes table
        # to identify the proper contact of a certain property in the
        # properties table.

        #for pr





    cursor.commit()

if __name__ == "__main__":
    # initialize an addressbook:
    ab = addressbook.Addressbook()
    c1 = addressbook.Contact("John", "Doe")
    c2 = addressbook.Contact("Jane", "Doe")
    c2.add_attr('phone', '+31(0)63414214')
    ab.add_contact(c1)
    ab.add_contact(c2)

    dbfilename = "./addressdb.db"
    connection = sqlite3.connect(dbfilename)

    initialize_addressbook_db_schema(connection)
    write_addressbook_to_db(ab,connection)



