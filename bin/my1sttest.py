#!/usr/bin/env python3

import addressbook
import logging
logging.basicConfig(
        level = logging.INFO)

ab = addressbook.Addressbook()
c1 = addressbook.Contact('John', 'Doe')
c2 = addressbook.Contact('Jahn', 'Doe')
c3 = addressbook.Contact('Jane', 'Doe')

ab.add_contact(c1)
ab.add_contact(c2)
ab.add_contact(c3)
ab.del_contact('Jane', 'Doe')

print(ab)


