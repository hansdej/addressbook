#!/usr/bin/env python3

# Show that the initialisation works:
import addressbook
import logging

# Set the logging to be verbose:
logging.basicConfig(
        level = logging.INFO
        )
logging.info("""
Exercise 1.7.2.1-1 Create contact class and demonstrate the add_attr method:
""")
c1 = addressbook.Contact('John', 'Doe')
c2 = addressbook.Contact('Jane', 'Doe')
c2.add_attr("email", "jane@doe.org")
logging.info("""Simple prints:
c1 = %s
c2 = %s

With attributes:
%s
%s"""%(c1,c2,c1.full_print(),c2.full_print()))

logging.info("Demonstrate a non allowed attribute:")
c2.add_attr("ail", "jane@doe.org")


logging.info("""
Exercise 1.7.2.1-1 The addressbook
""")
ab = addressbook.Addressbook()
logging.info("""
ab = %s
"""%ab)

logging.info("""
Exercise 1.7.2.2 Magic methods:
Simple print: already demonstrated.
""")
c3 = c1+ c2
logging.info("""
magic: c1 = c1+c2 will add (c2)jane's email to John(c1)

John = %s
John + Jane = %s
"""%(c1.full_print(),c3.full_print()))

ac = ab + c1
ac = ac + c2
logging.info("""
More magic: ab + c1 will create a copy with John added
ab: %s

ac = ab + c1 : %s

ac + c2:  %s
"""%(ab,ab+c1,ac))

logging.info("""
For loop iterates over all contacts:
""")
for contact in ac:
    logging.info(contact.full_print())


logging.info("""
Exercise 1.7.3.1 
Configuration files:
""")

ab.read_config(configfiles=['addressbook.ini'])

logging.info( ab.print_config())

logging.debug(addressbook.attributes(ab))

logging.debug(ab)

logging.info("""
Exercise 1.7.4.1 
Argument parsing:
Copy or link the argparse_exercise.py twice:
create_contact -> argparse_exercise.py
create_addrbook -> argparse_exercise.py

And execute:
./create_contact --firstname John --surname Doe --attr email john@doe.org
""")
from subprocess import call

call(["./create_contact", "--firstname","John","--surname", "Doe", "--attr",
    "email", "John@doe.org"])

logging.info("""

And:        
./create_addrbook --name 'MyAddressbook'
""")
call( ["./create_addrbook", "--name",'MyAddressbook'])
logging.info("""

""")

logging.info("""
Exercise 1.7.5.1
A lot of logging is used here already

Module 1 finished.
""")

logging.info("""
Exercise 2.6.1.[1-6]
doctest: execute the module addressbook/src/addressbook.py

""")
call(["../src/addressbook/addressbook.py"])
logging.info("""
Doctest finished (successfully?)        

""")

logging.info("""
Exercise 2.6.1.7
Advantages of Doctest:
* Illustrates simple how the code can be used.
* Gives quick ability to testing ability of small and quick mods.
* Enables test driven development close to the code itself.
* ...
Disadvantage
* For complex tests it can clutter the in-code docmentation.
""")

logging.info("""
Exercise 2.6.2.[1-5]
Unittest: illstrated via ../test/test_with_unittest.py
""")
call(["../test/test_with_unittest.py"])

logging.info("""
Unittest finished (successfully?)        

""")

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
