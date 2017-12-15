#!/usr/bin/python3
import addressbook.orm as ab_orm
import unittest
import shutil
import tempfile 

class Test_SQLAlchemy_Addressbook(unittest.TestCase):
    def test_new_addressbook_create(self):
        db_uri = "sqlite:///Addressbook.db"
        ab_orm.createdb(db_uri)
        DBsess = ab_orm.createdbsession(db_uri)
        ab = ab_orm.Addressbook(name="My book")
        DBsess.add(ab)
        DBsess.commit()
        self.assertIsInstance(ab, ab_orm.Addressbook)

    def test_SQLAlchemy_create_database_with_Addressbook(self):
        '''
        Test if an addressbook can be created with SQLAlchemy, add a few
        contacts , close the addressbook and see if presicely one John Doe can be
        retreived from the re-opened database.
        '''
        with tempfile.TemporaryDirectory() as tmpdir:
            dbmakefile=tmpdir+"/makeDBandAB.db"
            dbfetchfile=tmpdir+"/fetchDBandAB.db"
            db_uri = "sqlite:///"+dbmakefile
            ab_orm.createdb(db_uri)
            db_sess = ab_orm.createdbsession(db_uri)
            db_sess.add(ab_orm.Addressbook("Mijn Boek"))
            db_sess.commit()
            db_sess.close()
            # make a copy of the sqlite file.
            shutil.copy(dbmakefile,dbfetchfile)
            db_uri = "sqlite:///"+dbfetchfile
            ab_orm.createdb(db_uri)
            new_sess = ab_orm.createdbsession(db_uri)
            books = new_sess.query(ab_orm.Addressbook).all()
            assert len(books) == 1

    def test_SQLAlchemy_test_create_Contact(self):
        '''
        Test if an addressbook can be created with SQLAlchemy, add a few
        contacts , close the addressbook and see if presicely one John Doe can be
        retreived from the re-opened database.
        '''
        with tempfile.TemporaryDirectory() as tmpdir:
            dbfile=tmpdir+"/allowedAttrTest.db"
            db_uri = "sqlite:///"+dbfile
            ab_orm.createdb(db_uri)
            db_sess = ab_orm.createdbsession(db_uri)
            # The session is estabished

            ab = ab_orm.Addressbook("Mijn Boek")
            db_sess.add(ab)

            c1 = ab_orm.Contact(db_sess,"John", "Doe")
            c2 = ab_orm.Contact(db_sess,"Jane", "Doe")
            c3 = ab_orm.Contact(db_sess,"Pietje", "Puk")

            for c in c1,c2,c3:
               ab.add_contact(c)

            db_sess.commit()
            db_sess.close()

            new_sess = ab_orm.createdbsession(db_uri)
            result = new_sess.query(ab_orm.Contact).all()
            # Assert if three contacts were stored.
            assert len(result) == 3

    def test_add_allowed_attribute(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            dbfile=tmpdir+"/allowedAttrTest.db"
            db_uri = "sqlite:///"+dbfile
            ab_orm.createdb(db_uri)
            db_sess = ab_orm.createdbsession(db_uri)
            attrList = ab_orm._allowed_attributes

            for name,desc in attrList.items():
                ab_orm.AllowedAttribute(db_sess,name,desc)

            db_sess.commit()
            db_sess.close()
            new_sess = ab_orm.createdbsession(db_uri)
            # Compare the lengths of the lists, would that be a sufficient test?
            # A functional test in any case.
            assert len(new_sess.query(ab_orm.AllowedAttribute).all()) == len(attrList)

if __name__ == '__main__':
    unittest.main()

