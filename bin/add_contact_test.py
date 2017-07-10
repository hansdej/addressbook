#!/usr/bin/env python3

import addressbook

ab = addressbook.Addressbook()

cnt1 = addressbook.Contact('John', 'Doe')
cnt2 = addressbook.Contact('Jane', 'Doe')
cnt2.add_attr("email", "jane@doe.org")

c = cnt1+cnt2
for att in c.get_attrs():
	print('Attr: \"%s\", value = [%s]'% (att,getattr(c,att)))

print(ab)
print(cnt1)

ab = ab + cnt1
ab = ab + cnt2
ab = ab + (cnt2 + cnt1)

print(ab)

csvfile = "../FakeNameGenerator.csv"

ab.import_csv(csvfile)

jsonout = csvfile.replace("csv","json")
if jsonout == csvfile:
    # prevent overwriting of csv
    jsonout = "adresboek.json"

print(ab.full_print())

