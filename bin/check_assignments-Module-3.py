#!/usr/bin/env python3

# Show that the initialisation works:
import addressbook
import logging

# Set the logging to be verbose:
logging.basicConfig(
        level = logging.INFO
        )
logging.info("""
Exercise 3.5.1 Created a CSV import module
""")

csvfile = "Data/FakeNameGenerator.csv"
ab = addressbook.from_csv(csvfile, name = "My addressboek")
logging.info("""
        Addresbook %s loaded from file %s:
        %s
        """%(ab.name, csvfile, ab))

logging.info("""
Exercise 3.5.2 Created JSON and YAML export modules:
""")

jsonout = csvfile.replace("csv","json")
yamlout = csvfile.replace("csv","yaml")

addressbook.to_json(ab,jsonout)
addressbook.to_yaml(ab,yamlout)

logging.info("""
        Addresbook %s was exported to JSON and YAML-files:
        %s
        %s
        """%(ab.name, jsonout, yamlout))


logging.info("""
Exercise 3.5.3 The functionality was succesfully inserted in 
a separate addressbook/convert.py.
Please look into that file for more info
""")

