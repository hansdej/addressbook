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
ab = addressbook.Addressbook()
c1 = addressbook.Contact('John', 'Doe')
c2 = addressbook.Contact('Jane', 'Doe')
c2.add_attr("email", "jane@doe.org")
c3 = addressbook.Contact('Jane', 'Doe')

for c in c1,c2,c3:
    ab += c

csvfile = "Data/FakeNameGenerator.csv"

#ab.import_csv(csvfile)

jsonout = csvfile.replace("csv","json")
if jsonout == csvfile:
    # prevent overwriting of csv
    fallback = "addressbook.json"
    if jsonout == fallback:
        jsonout = "adresboek.json"
    else:
        jsonout = fallback

ab = ab+ab

print(ab.full_print())
ab.del_contact("Jane", "Doe")
ab.del_contact("Jane", "Doe",Id=4)
print(ab.full_print())
