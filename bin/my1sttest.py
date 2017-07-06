#!/usr/bin/env python3

import addressbook
import logging
logging.basicConfig(
        level = logging.DEBUG)

ab = addressbook.Addressbook()
ab.read_config()
ab.set_config()
c1 = addressbook.Contact('John', 'Doe')

ac = addressbook.Addressbook()
ad = addressbook.Addressbook(name="nog een boek")
print(ab)
print(ac)
print(ad)


