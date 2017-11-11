#!/usr/bin/env python3

# Show that the initialisation works:
import addressbook
import logging

# Set the logging to be verbose:


logging.basicConfig(
        level = logging.WARNING
        )
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


