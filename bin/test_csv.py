#!/usr/bin/env python3

import addressbook

ab = addressbook.Addressbook()

cnt1 = addressbook.Contact('John', 'Doe')
cnt2 = addressbook.Contact('Jane', 'Doe')
cnt2.add_attr("email", "jane@doe.org")

ab += cnt1
ab += cnt2

print(ab)

csvfile = "../FakeNameGenerator.csv"

ab.import_csv(csvfile)

jsonout = csvfile.replace("csv","json")
if jsonout == csvfile:
    # prevent overwriting of csv
    jsonout = "adresboek.json"

print(ab.full_print())

