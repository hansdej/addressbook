#!/usr/bin/env python3
#from addressbook import Addressbook,Contact
import unittest
import addressbook

#Addressbook = addressbook.Addressbook
#Contact     = addressbook.Contact

class TestContact(unittest.TestCase):

    def test_new_addressbook_creation(self):
        ab = addressbook.Addressbook("My testaddressbooek")
        self.assertIsInstance(ab, addressbook.Addressbook)

    def test_fail_addresbook_with_too_many_args(self):
        with self.assertRaises(TypeError):
            addressbook.Addressbook("name", "error")

    def test_zerolength_new_addressbook(self):
        ab = addressbook.Addressbook()
        self.assertEqual(len(ab),0)

    def test_new_contact(self):
        c = addressbook.Contact('John','Doe')
        self.assertIsInstance(c,addressbook.Contact)

    def test_faillure_on_wrong_arguments(self):
        with self.assertRaises(TypeError):
            addressbook.Contact("one argument lacking")

if __name__ == '__main__':
    unittest.main()
