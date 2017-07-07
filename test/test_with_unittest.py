#!/usr/bin/python3
import addressbook
import unittest

Addressbook = addressbook.Addressbook
Contact     = addressbook.Contact

class TestContact(unittest.TestCase):

    def test_new_addressbook_creation(self):
        ab = Addressbook("My testaddressbooek")
        self.assertIsInstance(ab, Addressbook)

    def test_fail_addresbook_with_too_many_args(self):
        with self.assertRaises(TypeError):
            Addressbook("name", "error")

    def test_zerolength_new_addressbook(self):
        ab = Addressbook()
        self.assertEqual(len(ab),0)

    def test_new_contact(self):
        c = Contact('John','Doe')
        self.assertIsInstance(c,Contact)

    def test_faillure_on_wrong_arguments(self):
        with self.assertRaises(TypeError):
            Contact("one argument lacking")

if __name__ == '__main__':
    unittest.main()
