#!/usr/bin/python3
import addressbook.orm as ab_orm
import pytest
import unittest

class Test_SQLAlchemy_Addressbook(unittest.TestCase):
    def test_new_addressbook_create(self):
        db_uri = "sqlite:///Addressbook.db"
        ab_orm.createdb(db_uri)
        DBsess = ab_orm.createdbsession(db_uri)
        ab = ab_orm.Addressbook(name="My book")
        self.assertIsInstance(ab, ab_orm.Addressbook)


def test_create_sqlitedb_with_alchemy(tmpdir):
    '''
    Test if an addressbook can be created with SQLAlchemy, add a few
    contacts , close the addressbook and see if presicely one John Doe can be
    retreived from the re-opened database.
    '''
    dbfile=tmpdir.join("allowedAttrTest.db")
    db_uri = "sqlite:///"+dbfile.strpath
    ab_orm.createdb(db_uri)
    ab_sess = ab_orm.createdbsession(db_uri)
    ab = ab_orm.Addressbook("Mijn Boek")
    ab_sess.add(ab)

    c1 = ab_orm.Contact(ab_sess,"John", "Doe")
    c2 = ab_orm.Contact(ab_sess,"Jane", "Doe")
    c3 = ab_orm.Contact(ab_sess,"Pietje", "Puk")


    for c in c1,c2,c3:
       ab.add_contact(c)

    ab_sess.commit()
    ab_sess.close()

    new_sess = ab_orm.createdbsession(db_uri)
    result = new_sess.query(ab_orm.Contact).filter_by(fname='John',sname='Doe').all()
    assert len(result) == 1

def test_add_allowed_attribute(tmpdir):
    dbfile=tmpdir.join("allowedAttrTest.db")
    db_uri = "sqlite:///"+dbfile.strpath
    ab_orm.createdb(db_uri)
    ab_sess = ab_orm.createdbsession(db_uri)
    attrList = ab_orm._allowed_attributes
    # We need a contact to add allowed attributes.
    # In a new design the addressbook will be another 1-many table,
    # and this method will an addressbook method.
    c = ab_orm.Contact(ab_sess,"John", "Doe")
    for name,desc in attrList.items():
        c.add_allowed_attr(name,desc)

    ab_sess.commit()
    ab_sess.close()
    new_sess = ab_orm.createdbsession(db_uri)
    assert len(new_sess.query(ab_orm.AllowedAttribute).all()) == len(attrList)




