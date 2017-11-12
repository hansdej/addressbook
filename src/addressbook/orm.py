#from sqlalchemy import Column, Integer, String, Table
import logging
import logging.config
#import configparser
#import addressbook
import os

import sqlalchemy as alch
from sqlalchemy.ext.declarative import declarative_base
import sqlalchemy.orm as orm
from sqlalchemy.orm import * # Less hassle with raised errors
"""
This ORM works slightly different from the first addressbook, this is done
for convenience.
* The addressbook class is not implemented explicitly: it will be the instance
    that is indicated bij the database uri.
* The allowed attributes table is no longer an attribute dict of the Contact
    class, but tied to the addressbook entity, actually it feels as if this
    helps to keep the addressbook consistenti more intrinsically: this way,
    this "restrictment" information is stored together with the data and no
    longer also in the code (which is a source of possible screw-ups.)"""

logging_configfile = "%s/logging/orm.ini"%os.path.dirname(__file__)
logging.config.fileConfig(logging_configfile,disable_existing_loggers=True)

ormlog = logging.getLogger('ormlogger')

Base = declarative_base()
# For testing and initialisation purposes.
_allowed_attributes ={
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
class Addressbook(Base):
    __tablename__ = 'addressbooks'
    default_name = "My Addressbook"
    config_read = False
    max_name_len =30
    session = None

    id      = alch.Column( alch.Integer, primary_key=True, autoincrement=True)
    name    = alch.Column( alch.String(max_name_len))
    contacts= orm.relationship('AddressbookEntry',
            back_populates='addressbook')

    def __init__(self,name=None):
        '''
        Initialise the database linked addressbook.
        '''
        max_name_len = Addressbook.max_name_len
        if name is None:
            name = Addressbook.default_name
        elif len(name) > max_name_len:
            name = name[:max_name_len]
            message = "Addressbook's maximum length of %d "%max_name_len
            message += "characters exceeded, truncated to \"%s\"."%name
            logging.warning(message)

        self.name = name

    def __add__(self,added):
        if isinstance(added, Contact):
            contact = added
            self.add_contact(contact)

        elif isinstance(added, Addressbook):
            num = 0
            for contact in added:
                #contact = contactentry.contact
                self.add_contact(contact)
                print(contact)
                num +=1
            message = "Added %d contacts from %s "%(num,added.name)
            message += " to %s"%self.name
            ormlog.info(message)

    def add_contact(self,contact):
            if Addressbook.session is None:
                # the session needs to be set, we have assigned the Contact class
                # as the class that contains the pointer to the session since the
                # Contacts are the most essential entities in an addressbook.
                Addressbook.session = contact.session
            session=contact.session

            # Next: create a new entry, add it to the database session whereupon it
            # can be added to the contact that is already in the session.
            # Whether the commit is necessary can be a point of discussion.
            newentry = AddressbookEntry(addressbook=self, contact=contact)
            session.add(newentry)
            self.contacts.append(newentry)

            # The logging message:
            message = "Added %s %s to "%(contact.fname,contact.sname)
            message +="to \"%s\""%self.name
            ormlog.info(message)

    def find_contacts(self,fname,sname):
        '''
        Find the contact with the parsed fname and sname.
        '''
        contacts = self.session.query(Contact).join(
                "addressbooks","addressbook").filter(
                        Addressbook.id==self.id,
                        Contact.fname == fname,
                        Contact.sname == sname).all()
        return contacts

    def unlink_contacts(self,fname,sname):
        '''
        Unlink the contact from this addressbook.
        '''
        contacts = self.find_contacts(fname,sname)
        if len(contacts) <1:
                message = "No Contact %s %s to unlink "%(fname,sname)
                message += "from addressbook \"%s\""%self.name
                ormlog.warning(message)
        else:
            for c in contacts:
                contact_links = self.session.query(AddressbookEntry).filter_by(
                        addressbook_id=self.id,
                        contact_id=c.id).all()
                for link in contact_links:
                    message = "Unlinking %s %s "%(c.fname,c.sname)
                    message += "(link.id=%d) "%link.id
                    message += "from addressbook \"%s\""%self.name
                    ormlog.info(message)
                    self.session.delete(link)

    def __len__(self):
        return len(self.contacts)

    def __repr__(self):
        message  = "<class Addressbook \"%s\","%self.name
        message += " containing %d Contacts>"%len(self)
        return message

    def __iter__(self):
        '''
        Iterate over all contacts in the addressbook.
        '''
        return iter([entry.contact for entry in self.contacts])

class AddressbookEntry(Base):
    __tablename__ = 'ab_entries'
    '''
    The relational table that links multiple contacts to multiple addressbooks.
    '''
    id              = alch.Column( alch.Integer, primary_key=True, autoincrement=True)

    contact_id      = alch.Column( alch.Integer, alch.ForeignKey('contacts.id'))
    contact         = orm.relationship( "Contact", back_populates="addressbooks")

    addressbook_id  = alch.Column( alch.Integer, alch.ForeignKey('addressbooks.id'))
    addressbook     = orm.relationship( "Addressbook", back_populates="contacts")

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
    >>> orm.createdb("sqlite:///ab.db")
    >>> ab_sess=orm.createdbsession("sqlite:///ab.db")
    >>> c = orm.Contact("John", "Doe")
    >>> c.add_to_addressbook(ab_sess)
    >>> ab_sess.close()
    >>> import os
    >>> os.rename('ab.db', 'ab-orm.db')
    >>> db_sess=orm.createdbsession("sqlite:///ab-orm.db")
    >>> db_sess.query(orm.Contact).filter_by(fname='John',sname='Doe').first()
    <class Contact: "Doe, John" >

    '''
    __tablename__ = 'contacts'
    # These are class attributes: The bookkeeping is done in the internals of
    # declarative base: The 'id' of every separate instance points to the
    # same database column, but when called upon, the correct primary_key
    # of an instance will be `returned'.
    id    = alch.Column( alch.Integer, primary_key=True, autoincrement=True )
    fname = alch.Column( alch.String(30))
    sname = alch.Column( alch.String(30))

    attributes = orm.relationship('Attribute',
                    back_populates ='contact',
                    cascade='delete')

    addressbooks = orm.relationship('AddressbookEntry',
                     back_populates ='contact')
    # Hence all Contacts will be added to the same session that is assigned
    # to this class property the same addressbook.
    session=None

    def __init__(self,session, fname,sname):
        self.fname=fname
        self.sname=sname
        self.session = session
        # Issue a warning if we already have such a contact in the database.
        searchIt = session.query(Contact).filter_by(
                            fname=self.fname, sname=self.sname).first()
        if searchIt is not None:
            message = "A Contact %s %s already "%(self.fname,self.sname)
            message += "exists in the database, but adding it anyway."
            ormlog.warning(message)
        # try to add the Contact and roll back if this fails.
        try:
            session.add(self)
            ormlog.info("Contact %s %s successfully added to SQL"%(
                                            self.fname, self.sname))
        except Exception as e:
            session.rollback()
            session.flush()
            message =  "While trying to add Contact %s %s "%( self.fname, self.sname)
            message += "to the SQL addressbook, the  exception \"%s\"occured."%e
            ormlog.error(message)

    def __repr__(self):
        return '<class Contact: \"%s, %s\" >'%( self.sname, self.fname )


    def add_attr(self,attr_name,attr_val):

        # Verify if a session is connected yet.
        if self.session is None:
            message = "Trying to add %s, %s to %s"%(self,attr_name,attr_val)
            message += "without a session."
            ormlog.error(message)
            raise Exception("No session connected yet")

        session = self.session
        # Query the allowed attributes for the desired attribute as a test of
        # its presence.
        allowed_attr = session.query(AllowedAttribute).filter_by(
                                        attr_name=attr_name).first()
        if allowed_attr is None:
            ormlog.warning("'%s' is not an allowed attribute."%attr_name)
        else:
            attr = Attribute(contact=self,
                        allowed_attribute= allowed_attr,
                        value=attr_val )
            session.add(attr)
            self.attributes.append(attr)
    def find_attr(self, attr_name):
        #etcetera etcetera
        pass

    def remove_attr(self,attr_name):
        pass

    def change_attr(self,attr_name,attr_desc):
        pass

    def add_allowed_attr(self,attr_name,attr_description):
        '''
        Add an allowed attribute via the Contact instance.
        This is the old behaviour.
        '''
        AllowedAttribute(self.session,attr_name,attr_description)

    def remove_allowed_attr(self,attr_name):
        s = self.session
        remove = s.query(AllowedAttribute).filter_by(attr_name=attr_name).first()
        if remove is None:
            message = "Allowed attribute %s was not found"%attr_name
            ormlog.warning(message)
        else:
           message = "Removing allowed attribute %s."%remove.attr_name
           ormlog.info(message)
           s.delete(remove)

    def change_allowed_attr(self,attr_name,new_attr_name=None,attr_description=None):
        """
        Change the name of the attribute or its description without changing the id
        that connects it to (possibly) a lot of contact attributes can be usefull.
        """
        pass

class AllowedAttribute(Base):
    '''
    The allowed Attribute that is to be stored in the 'allowed_attributes'
    table with primary key, with its name and description.
    '''
    __tablename__ = 'allowed_attributes'
    id             = alch.Column( alch.Integer, primary_key=True, autoincrement=True)
    attr_name = alch.Column( alch.String(30)   )
    attr_desc = alch.Column( alch.String(255)  )
    attributes     = orm.relationship('Attribute', back_populates = 'allowed_attribute',
                                cascade='delete')
    def __init__(self,session,attr_name,attr_desc):
        """
        Add an allowed attribute to the database.
        """
        # Should contain a check wheter the property is already added.
        self.attr_name=attr_name
        self.attr_desc=attr_desc
        if session == None:
            message =  "Trying to add %s to the allowed atributes"%attr_name
            message += "With no open session."
            ormlog.error(message)
            raise Exception("No session connected yet")

        try:
            session.add(self)
            message = "Allowed Attribute [%s] "%( attr_name)
            message += "successfully added to SQL addressbook."
            ormlog.info(message)
        except Exception as e:
            DBsession.rollback()
            DBsession.flush()
            message =  "While trying to add the allowed attribute "
            message += attr_name
            message += " to the SQL addressbook, the  exception \"%s\"occured."%e
            ormlog.error(message)
    def __repr__(self):
        return "<class AllowedAttribute: [%s]:\"%s\">"%(
                self.attr_name,self.attr_desc)

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

    #def __init__ (self,attribute,value):
        # Attributes are initialised only for contacts.
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
    dbFilename='addressbook_alchemy.db'
    dburi='sqlite:///'+dbFilename
    createdb(dburi)
    session=createdbsession(dburi)
    # using first() instead of one() because the None of the first is easier to
    # handle than the error of the latter.

    c =session.query(Contact).filter_by(fname='John',sname="Doe").first()
    if c is None:
        # No contact found: generating it.
        c = Contact(session,fname='John',sname="Doe")
        session.commit()
    # Same story for the AllowedAttribute.
    aa = session.query(AllowedAttribute).filter_by(attr_name='email').first()
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

