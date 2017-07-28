#!/usr/bin/python3

import logging
import sqlite3
import addressbook

# Generate a table called "contacts" with a unique ID and fname & sname.
# If one already exists: drop it first.
# The id is an numeric, unique one.
contacts_table = "contacts"
attrs_table = "attributes"
allowed_table = "allowed_attrs"

dblog = logging.getLogger('dblogger')

make_contacts_table = """
DROP TABLE IF EXISTS contacts;
CREATE TABLE table (
    id      INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
    fname   CHAR(30),
    sname   CHAR(30)
);
""".replace('table',contacts_table)

# Generate a table of allowed contacts.
make_allowed_attrs_table = """
DROP TABLE IF EXISTS table;
CREATE TABLE table (
    attrname  CHAR(30) PRIMARY KEY UNIQUE     NOT NULL,
    desc      CHAR(255)
);
""".replace('table', allowed_table )

make_attributes_table = """
DROP TABLE IF EXISTS table;
CREATE TABLE table (
    id      INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,
    contact INTEGER               NOT NULL,
    attr    CHAR(30)              NOT NULL,
    value   CHAR(255),
    FOREIGN KEY(contact) REFERENCES contacts(id),
    FOREIGN KEY(attr) REFERENCES allowed_attrs(attr)
);
""".replace('table', attrs_table)

def initialize_addressbook_db_schema(connection):
    """ rewrites the pretty fixed database schema into
    the sqlite database file.
    """
    cursor = connection.cursor()
    cursor.executescript(make_contacts_table)
    cursor.executescript(make_allowed_attrs_table)
    cursor.executescript(make_attributes_table)
    connection.commit()

def do_transaction(connection,query,params):
    """
    """
    dblog.debug('inserting: "%s",%s'%(query,params))

    cursor = connection.cursor()
    try:
        cursor.execute(query,params)
        dblog.info('executed:"%s,%s"'%(query,params))
    except OperationalError:
        dblog.error("sqlite3 Operational error while trying: %s %s"%(query,params))

    return cursor

def write_allowed_attributes_to_db(addressbook,connection):
    """
    """

    for attrname,description in addressbook.allowed_attrs_dict().items():

        query = u"""INSERT INTO table (attrname, desc) VALUES (?,?)"""
        query = query.replace('table',allowed_table,)
        params =(attrname, description)
        do_transaction(connection, query, params)

    connection.commit()

def write_contacts_to_db(addressbook,connection):
    """
    """

    for contact in addressbook:
        # Use " to circumfer the apostrophe problem.
        query = u"""INSERT INTO table (fname, sname) VALUES (?,?)"""
        query = query.replace('table',contacts_table)
        params = (contact.fname, contact.sname)


        cursor = do_transaction( connection, query, params)

        # This is None if executescript or some other method than
        # execute is used.
        contact._dbId = int(cursor.lastrowid)

        # The contact was inserted into the contacts table.
        # this numeric ID is to be used in the atrributes table
        # to link the attributes to the proper contact.
    connection.commit()

def write_attrs_to_db(contact,connection):
    """
    """
    for attr in contact.get_attrs():

        cId = contact._dbId
        value = getattr(contact,attr)

        # Use " to circumfer the apostrophe problem.
        query =  u"""INSERT INTO table (contact, attr, value) VALUES (?,?,?)"""
        query = query.replace('table',attrs_table)
        params = (cId, attr, value)
        do_transaction(connection ,query, params)

    connection.commit()

def save_addressbook_to_db(addressbook,dbfilename):
    """
    """
    connection = sqlite3.connect(dbfilename)

    initialize_addressbook_db_schema(connection)

    write_allowed_attributes_to_db(addressbook,connection)

    write_contacts_to_db(addressbook,connection)
    for contact in addressbook:
        write_attrs_to_db(contact,connection)


def read_db_allowed_attrs(connection):
    """
    """
    query = u"""SELECT * FROM table"""
    query = query.replace('table',allowed_table)
    params = ()

    allowed_attrs = do_transaction(connection, query, params).fetchall()

    for attr, desc in allowed_attrs:
        addressbook.Contact.add_allowed_attr(attr,desc)

def read_db_contact_attributes(connection,cId ,contact):
    """
    """
    query  = u"""SELECT attr,value FROM table WHERE contact = ? """
    query += u""" EXCEPT SELECT attr,value FROM table """
    query += u""" WHERE attr='fname' OR attr='sname' """
    query = query.replace('table',attrs_table)

    params = (cId,)

    #cursor = do_transaction(query,connection)
    #c_attrs= cursor.fetchall()
    c_attrs= do_transaction(connection,query,params).fetchall()

    for attr,value in c_attrs:
        contact.add_attr(attr,value)

def read_db_contacts(connection, abook):
    """
    """
    query = u"""SELECT * FROM table """
    query = query.replace('table',contacts_table)
    params = ()

    allcontacts = do_transaction(connection,query,params).fetchall()

    for cId,fname,sname in allcontacts:
        contact = addressbook.Contact(fname, sname)
        read_db_contact_attributes(connection,cId,contact)

        abook.add_contact(contact)

def load_addressbook_from_db(dbfilename, name  = None):

    abook = addressbook.Addressbook() if name is None else addressbook.Addressbook(name = name)

    connection = sqlite3.connect(dbfilename)
    # First read the allowed attributes
    # Then the contacts with their properties:
    # The database should be better at selecting the indexed
    # properties, using this should be the fastest AND the
    # unique database Id can stay out of `python space'.
    read_db_allowed_attrs(connection)

    read_db_contacts(connection, abook)


    return abook


if __name__ == "__main__":
    # initialize an addressbook:
    ab = addressbook.Addressbook()
    c1 = addressbook.Contact("John", "Doe",email="john@doe.org")
    c2 = addressbook.Contact("Jane", "Doe")
    c2.add_attr('phone', '+31(0)63414214')
    ab.add_contact(c1)
    ab.add_contact(c2)

    dbfilename = "./addressdb.db"
    save_addressbook_to_db(ab,dbfilename)



