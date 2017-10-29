#from sqlalchemy import Column, Integer, String, Table
import logging
import logging.config
import configparser
import addressbook
import os

import sqlalchemy as alch
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm as orm
from sqlalchemy.orm import * # Less hassle with raised errors

'''
This ORM works slightly different from the first addressbook, this is done
for convenience.
* The addressbook class is not implemented explicitly: it will be the instance
    that is indicated bij the database uri.
* The allowed attributes table is no longer an attribute dict of the Contact
    class, but tied to the addressbook entity, actually it feels as if this
    helps to keep the addressbook consistenti more intrinsically: this way,
    this "restrictment" information is stored together with the data and no
    longer also in the code (which is a source of possible screw-ups.)

'''


logging_configfile = "%s/logging/orm.ini"%os.path.dirname(__file__)
logging.config.fileConfig(logging_configfile,disable_existing_loggers=True)

ormlog = logging.getLogger('ormlogger')

Base = declarative_base()

_allowed_attributes ={

    '''
    A helper that enables a quick first fill list for a new addressbook.
    '''

       'Id'   :"Id number",
       'fname':"First name",
       'sname':"Family name",
       'email':"Email address",
       'email_home': 'Home email address',
       'email_work': 'Work email address',
       'addr': 'Address',
       'addr_work': 'Work address',
       'addr_home': 'Home address',
       'mobile': 'Mobile phone number',
       'phone': 'Phone number',
       'notes': 'Additional notes',
       'gender': 'Gender (m/f)',
       'company': 'Affiliated company',
       'birthday': 'Birthday',
}

class Contact(Base):
    '''
    A Contact will be stored in the contacts table with primary key, Forename
    and surname.
    Via its attributes, it is connected to an AllowedAttribute in the
    allowed_attributes table in a "Many-to-Many" relationship. These attributes
    are stored together with those of other Contact instances in a third table.
    This table connects to these both tables and acts as/is an "association table"
    with the primary keys from both "sides" stored as mapping, foreign keys and
    the attribute value.

    >>> import addressbook.orm as orm
    >>> orm.createdb("sqlite://")
    >>> ab_sess=orm.createdbsession("sqlite://")
    >>> c = orm.Contact("John", "Doe")
    >>> c.add_to_addressbook(ab_sess)

    '''
    __tablename__ = 'contacts'
    # These are class attributes: The bookkeeping is done in the internals of
    # declarative base: The 'id' of every separate instance points to the
    # same database column, but when called upon, the correct primary_key
    # of an instance will be `returned'.
    id    = alch.Column( alch.Integer, primary_key=True, autoincrement=True )
    fname = alch.Column( alch.String(30))
    sname = alch.Column( alch.String(30))
    allow_duplicates = True
    attributes = orm.relationship('Attribute', back_populates ='contact',
                    cascade='delete')
    session=None

    def __init__(self, fname,sname, session=None):
        self.fname=fname
        self.sname=sname
        self.session = session

    def __repr__(self):
        return '<class Contact: \"%s, %s\" >'%( self.sname, self.fname )

    def add_to_addressbook(self,DBsession):
        # The addressbook is db_uri used as an equivalent.
        self.session=DBsession

        # Issue a warning if we already have such a contact in the database.
        searchIt = DBsession.query(Contact).filter_by(fname=self.fname,sname=self.sname).first()
        if searchIt is not None:
            ormlog.warning("A Contact %s %s is already the database"%(self.fname,self.sname))

        try:
            DBsession.add(self)
            DBsession.commit()
            ormlog.info("Contact %s %s successfully added to SQL"%(
                                self.fname, self.sname))
        except Exception as e:
            DBsession.rollback()
            DBsession.flush()
            message = "While trying to add Contact %s %s to SQL "%(
                                self.fname, self.sname)
            message += "the  exception \"%s\"occured."%e
            ormlog.error(message)
            # How can I add the raises exception to the messag?

    def add_attribute(self,attr_name,attr_val):

        # kijk of het attribuut in de allowed attributes staat.
        if self.session is None:
            raise Exception("No session")

        allowed_attr = session.query(AllowedAttribute).filter_by(
                                        attribute_name=attr_name).first()
        if allowed_attr is None:
            ormlog.warning("'%s' is not an allowed attribute."%attr_name)
        else:
            attr=Attribute( value = attr_val,
                            allowed_attribute = allowed_attr,
                            contact=self)

class AllowedAttribute(Base):
    '''
    The allowed Attribute that is to be stored in the 'allowed_attributes'
    table with primary key, with its name and description.
    '''
    __tablename__ = 'allowed_attributes'
    id             = alch.Column( alch.Integer, primary_key=True, autoincrement=True)
    attribute_name = alch.Column( alch.String(30)   )
    attribute_desc = alch.Column( alch.String(255)  )
    attributes     = orm.relationship('Attribute', back_populates = 'allowed_attribute',
                                cascade='delete')
    def __init__(self,name,desc):
        # Should contain a check wheter the property is already added.
        self.attribute_name=name
        self.attribute_desc=desc

class Attribute(Base):
    __tablename__ = 'attributes'
    '''
    The Attribute is stored in the attributes association table. Every one its own,
    unique primary key and the two foreighn keys to map them to a Contact and an
    AllowedAttribute. The contact and attribute property of each Attribute needs
    explicit linking to the appropriate instances, for which (probably) the ForeignKey
    is used.
    '''
    id                   = alch.Column( alch.Integer, primary_key=True, autoincrement=True)
    value                = alch.Column( alch.String(255))

    # The linking
    contact_id           = alch.Column( alch.Integer, alch.ForeignKey('contacts.id'))
    contact              = orm.relationship( "Contact", back_populates="attributes")

    allowed_attribute_id = alch.Column( alch.Integer, alch.ForeignKey('allowed_attributes.id'))
    allowed_attribute    = orm.relationship( "AllowedAttribute", back_populates="attributes")
    #def __init__ (self,attribute,value, **kwargs):
    #    self.allowed_attribute = attribute
    #    self.value = value

def connectdb(db_uri):
    return alch.create_engine(db_uri)

def createdb(db_uri):
    engine = connectdb(db_uri)
    Base.metadata.create_all(engine)

def createdbsession(db_uri):
    engine = connectdb(db_uri)
    Base.metadata.bind = engine
    DBSession = orm.sessionmaker(bind=engine)
    return DBSession()

def add_contact(session,contact):
    session.add(contact)

def main(args):
    '''
    Wat moeten we hier doen?

    Basisfunctionaliteit:
    Schrijf Contact naar dB
    Maak allowed attributen aan
    Schrijf Attributen naar DB
        Link met contact
        link met AllowedAttribuut
    '''
    # Implicitly the Addressbook object is replaced by the database file
    # Lets stick to this and remember that for real applications.
    dbFileName='addressbook_alchemy.db'
    dburi='sqlite:///'+dbFilename
    createdb(dburi)
    session=createdbsession(dburi)
    # using first() instead of one() because the None of the first is easier to
    # handle than the error of the latter.

    c =session.query(Contact).filter_by(fname='John',sname="Doe").first()
    if c is None:
        # No contact found: generating it.
        c = Contact(fname='John',sname="Doe")
        session.add(c)
        session.commit()
    # Same story for the AllowedAttribute.
    aa = session.query(AllowedAttribute).filter_by(attribute_name='email').first()
    if aa is None:
        # Apparently this is missing, so we add it.
        aa = AllowedAttribute('email','Email Address')
        session.add(aa)
        session.commit()
    # Add a few new attributes to the contact. 
    # How to do this?
    # -> verify if it is allowed
    # -> link to the proper allowed contact



    return 0

if __name__ == 'main':
    sys.exit(main(sys.argv))

