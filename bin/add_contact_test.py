#!/usr/bin/env python3

import addressbook

ab = addressbook.Addressbook()

c1 = addressbook.Contact('John', 'Doe')
c2 = addressbook.Contact('Jane', 'Doe')
c2.add_attr("email", "jane@doe.org")

c = c1+c2
for att in c.get_attrs():
	print('Attr: \"%s\", value = [%s]'% (att,getattr(c,att)))

print(ab)
print(c1)

ab = ab + c1
ab = ab + c2
ab = ab + (c2 + c1)

print(ab)

csvfile = "../FakeNameGenerator.csv"

ab.import_csv(csvfile)

jsonout = csvfile.replace("csv","json")
if jsonout == csvfile:
    # prevent overwriting of csv
    jsonout = "adresboek.json"

msg = ""
for contact in ab:
    for attribute in contact.get_attrs():
        msg += "%s = %s \t "%(str(attribute),getattr(contact,attribute))
    msg+= "\n"

print(msg)
