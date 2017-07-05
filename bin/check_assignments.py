#!/usr/bin/env python3

# Show that the initialisation works:
import addressbook
import logging

# Set the logging to be verbose:
logging.basicConfig(
        level = logging.DEBUG
        )

ab = addressbook.Addressbook()
ab.read_config(configfiles=['addressbook.ini'])

logging.debug(addressbook.attributes(ab))

c1 = addressbook.Contact('John', 'Doe')
c2 = addressbook.Contact('Jane', 'Doe')
c2.add_attr("email", "jane@doe.org")

c = c1+c2
for att in c.get_attrs():
	logging.debug('Attr: \"%s\", value = [%s]'% (att,getattr(c,att)))

logging.debug(ab)
logging.debug(c1)

ab = ab + c1
ab = ab + c2
ab = ab + (c2 + c1)

logging.debug(ab)


#Add a (few) good tests for the config file functionality

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

print(ab)

msg = ""
for contact in ab:
    for attribute in contact.get_attrs():
        msg += "%s = %s \t "%(str(attribute),getattr(contact,attribute))
    msg+= "\n"    
ab.del_contact("Jane", "Doe") 
ab.del_contact("Jane", "Doe",Id=4) 
print(ab.full_print())




