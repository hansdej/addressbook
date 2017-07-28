#!/usr/bin/env python3

import addressbook
import logging
logging.basicConfig(
        level = logging.INFO)

ab = addressbook.Addressbook()
ab += addressbook.Contact('John', 'Doe')
ab += addressbook.Contact('Jahn', 'Doe')
ab += addressbook.Contact('Jane', 'Doe')

ab.del_contact('Jane', 'Doe')

#print(ab)

book = addressbook.load_addressbook_from_db("Data/addressboek.db")

print(book)


