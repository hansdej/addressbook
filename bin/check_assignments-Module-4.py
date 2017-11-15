#!/usr/bin/env python3

# Show that the initialisation works:
import sys
import addressbook
import logging

# Set the logging to be verbose:

#Dirty quickfix to prevent a  shitload of SQL messages while executing this script.
logging.basicConfig( level = logging.WARNING )

consoleHandler = logging.StreamHandler(sys.stdout)

logging.info("""
Exercise 4.1.1 Created the addressbook/db.py file which is loaded with
the rest of the addressbook.
""")

csvfile = "Data/FakeNameGenerator.csv"
ab = addressbook.from_csv(csvfile, name = "My addressboek")

databasefilename = "Data/addressboek.db"
logging.info("""
        Saving the addressbook into %s
"""%databasefilename)

addressbook.save_addressbook_to_db(ab,databasefilename)

logging.info("""
        The addressbook information should be stored in: %s
"""%databasefilename)

boek = addressbook.load_addressbook_from_db(databasefilename)

logging.info("""
        The addressbook contains:
        %s
        """%boek)
# Continue with the SQLAlchemy exercise.
logging.info("""
    Most of the SQLAlchemy exercises are writing code and adding
    propper logging.
    The most functional stuff are the three pytest tests.
    As a "bonus" (or actually something that challenged my curiosity "can I do it?")
    I implemented a query for a contact  as a method of an Addressbook. Got it 
    functioning via an extra "join" method and was wondering if this is the proper 
    way indeed.
    """)
