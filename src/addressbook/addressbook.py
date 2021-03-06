#!/usr/bin/env python3
# "object" is een compatibility dingetje met Python  2
import sys
import os
import logging
import json
import logging.config
import configparser

logging_configfile = "%s/logging-addressbook.ini"%os.path.dirname(__file__)
logging.config.fileConfig(logging_configfile,disable_existing_loggers=True)


def attributes(thing):
    """
    The helper function to get all the regular attributes

    >>> import addressbook
    >>> c = addressbook.Contact("John", "Doe")
    >>> c.add_attr("email","john@Doe.org")
    >>> sorted(addressbook.attributes(c))
    ['email', 'fname', 'sname']
    >>>

    """
    myattrs = set() # Since all properties should be unique,
                    # it should not be necessary to use a set here.
                    # The set was introduced to support the method
                    # to merge contact, but we will stick to it for
                    # now.
    for attr in dir(thing):
        if attr.startswith('_'):
            continue
        if callable(getattr(thing, attr)):
            continue
        else:
            myattrs.add(attr)
    return myattrs

class Addressbook(object):
    """
    An address object.
    """
    default_name = "My Addressbook"
    # A semaphore to indicate whether the config has been read al least once already.
    config_read = False
    def __init__(self, name=None):
        """
        Initialize the addressbook object:

        >>> import addressbook
        >>> ab = addressbook.Addressbook("My Addressbook")
        >>> ab
        <class Addressbook "My Addressbook", containing 0 contacts>
        >>>
        """
        logging.config.fileConfig(logging_configfile)

        if Addressbook.config_read is False:
            self.read_config()
            self.set_config()
            Addressbook.config_read = True
        if name is None:
            name = Addressbook.default_name

        self.name       = name
        self._contacts  = []
        self._newId     = 0 # Use the underscore to prevent it be copied in a copy.

    def __add__(self, added):
        """
        The pseudo numeric addition. Returns a copy of the addressbook with the
        contact added.
        (N.B. the contacts themselves are not copied.)

        >>> import addressbook
        >>> ab = addressbook.Addressbook("My Addressbook")
        >>> ab + addressbook.Contact('John', 'Doe')
        <class Addressbook "My Addressbook", containing 1 contacts>
        >>> ab
        <class Addressbook "My Addressbook", containing 0 contacts>
        >>> ab += addressbook.Contact('John', 'Doe')
        >>> ab
        <class Addressbook "My Addressbook", containing 1 contacts>
        """
        newbook = self.copy()

        # This add_contact-method is the primitive of this "method".
        if isinstance(added,Contact):
            # Add one contact
            newbook.add_contact(added)

        elif isinstance(added,Addressbook):
            # Merge the second addressbook
            for contact in added:
                newbook.add_contact(contact)

        return newbook

    def __len__(self):
        """
        The number of contacts is a usefull length

        >>> import addressbook
        >>> ab = addressbook.Addressbook("My Addressbook")
        >>> ab += addressbook.Contact('John', 'Doe')
        >>> len(ab)
        1
        >>>


        """
        return len(self._contacts)

    def __repr__(self):
        """
        The standard representation of the Addressbook

        >>> import addressbook
        >>> addressbook.Addressbook("My Addressbook")
        <class Addressbook "My Addressbook", containing 0 contacts>
        """

        return '<class Addressbook \"%s\", containing %d contacts>'%(
            self.name, len(self)
            )

    def __iter__(self):
        """
        Return the intended iterator object

        >>> import addressbook
        >>> ab = addressbook.Addressbook("My Addressbook")
        >>> ab += addressbook.Contact('John', 'Doe')
        >>> ab += addressbook.Contact('Jane', 'Doe')
        >>> for c in ab:
        ...     print( "%s %s"%(c.fname,c.sname))
        ...
        John Doe
        Jane Doe
        >>>

        """
        return iter(self._contacts)


    def copy(self):
        """
        Make a copy of the addressbook
        >>> import addressbook
        >>> ab = addressbook.Addressbook("My Addressbook")
        >>> ac = ab
        >>> ad = ab.copy()
        >>> ac == ab
        True
        >>> ad == ab
        False
        >>> print(ab)==print(ad)
        <class Addressbook "My Addressbook", containing 0 contacts>
        <class Addressbook "My Addressbook", containing 0 contacts>
        True
        """
        newbook = Addressbook( self.name )

        # Copy the properties of the original object:
        # Got a feeling this should be simpler by first calling
        # the copy method from the superclass and then add the
        # explicit copy for the Contact()s that we added.
        # But an elaborate discussion on that sounds a bit
        # beyond the scope of this course.
        for attribute in attributes(self):
            setattr(newbook,attribute,getattr(self,attribute))

        #Copy all the existing entries:
        for contact in self:
            newbook.add_contact(contact)
        return newbook

    def add_contact(self, contact):
        """
        The base method to add a contact to an addressbook:

        >>> import addressbook
        >>> ab = addressbook.Addressbook("My Addressbook")
        >>> ab.add_contact(addressbook.Contact('John', 'Doe'))
        >>> ab.add_contact(addressbook.Contact('Jane', 'Doe'))
        >>> ab
        <class Addressbook "My Addressbook", containing 2 contacts>

        """
        thisId      = self._newId
        already_there = False
        for c in self:
            # Bluntly check if the contact is already there
            if c is contact:
                already_there = True


        if not isinstance(contact,Contact):
            raise(TypeError(3,"Only Contacts can be added to an Addressbook"))
        elif already_there == True:

            logging.warning("Contact already in addressbook %s."%self.name)
        else:
            newContact = contact
            newContact._Id = thisId
            self._newId += 1 # This increment might also be made depending
                        # on whether the contact was succesfully added
                        # the Addressbook.
            #contact.add_attr( "_Id", thisId)
            self._contacts.append(newContact)

    def del_contact(self, fname, sname, Id=None):
        """
        Delete a contact from the list.
        In case of duplicate names, none is erased if the (unique)
        Is is absent.

        >>> import addressbook
        >>> ab = addressbook.Addressbook("My Addressbook")
        >>> ab += addressbook.Contact("John", "Doe")
        >>> ab += addressbook.Contact("Jane", "Doe")
        >>> ab
        <class Addressbook "My Addressbook", containing 2 contacts>
        >>> ab.del_contact("John", "Doe")
        >>> ab
        <class Addressbook "My Addressbook", containing 1 contacts>
        >>> ab.del_contact("Jane", "Doe")
        >>> ab
        <class Addressbook "My Addressbook", containing 0 contacts>
        >>> ab.del_contact("Jane", "Doe")
        >>> ab
        <class Addressbook "My Addressbook", containing 0 contacts>

        """
        # The it becomes clearer that the handling of duplicate contacts should
        # be handled explicitly.


        Clist = self._contacts
        target = []

        #ToDo for item in enumerate(Clist):
        for (item,contact) in enumerate(Clist):
            if fname == contact.fname and sname == contact.sname:
                logging.debug("We got a hit on Id %d:\n %s"%(
                            contact._Id,
                            contact.full_print()
                            ))
                if Id is None or contact._Id == Id:
                    # The None case can result in multiple entries, the
                    # given Id will limit automatically to a single case.
                    target.append(item)

        logging.debug("target = %s"%target)


        if len(target) < 1:
            logging.warning("Found no contact %s %s to remove"%(fname,sname))

        elif len(target) > 1 and Id is None:
            # If there are more contacts with the same Id, they are
            # pointers to the same, non-anonymous contact and should
            # all be removed.
            message =  'Multiple contacts "%s %s" found.\n'%(fname,sname)
            message += 'with Ids: '
            for item in target:
                message += " [%d]"%Clist[item]._Id
            message += "\n\tNot deleting any: Please supply the ID of\n"
            message += "\tthe desired one."
            logging.warning(message)
        else:
            Clist.pop(target[0])

    def full_print(self):
        """
        return an elaborate string suitable for printing.

        >>> import addressbook
        >>> ab = addressbook.Addressbook("My Addressbook")
        >>> ab += addressbook.Contact("John", "Doe")
        >>> print(ab.full_print())
        Addressbook: "My Addressbook" with 1 contacts:
        * Contact: "Doe, John"
            fname = John
            sname = Doe
        """
        thisList = "Addressbook: \"%s\" with %d contacts:\n"%(self.name,len(self))
        for contact in self._contacts:
            thisList += "* %s"%contact.full_print()
        return thisList

    def to_list(self):
        return [ contact.to_dict() for contact in self ]

    def to_json(self):
        """

        >>> import addressbook
        >>> ab = addressbook.Addressbook()
        >>> ab += addressbook.Contact("John", "Doe")
        >>> print(ab.to_json())
        [
            {
                "sname": "Doe",
                "fname": "John"
            }
        ]
        """
        return json.dumps(self.to_list(), indent=4)

    def find_contact_by_name(self,search_fname, search_sname):
        """
        Search an addressbook for all contacts with the presented
        name and return a list of the corresponding contacts.

        >>> import addressbook
        >>> ab = addressbook.Addressbook()
        >>> ab += addressbook.Contact("John", "Doe")
        >>> ab += addressbook.Contact("Jane", "Doe")
        >>> ab += addressbook.Contact("Pietje", "Puk")
        >>> ab.find_contact_by_name("John", "Doe")
        [<class Contact "Doe, John" >]


        """
        hits=[]
        for contact in self._contacts:
            if (contact.fname == search_fname) and (contact.sname == search_sname):
                hits.append(contact)
        return hits

    @classmethod
    def read_config(cls, configfiles=None):
        """
        Read the parsed and standard configuration files
        if not None, the config file names should be a proper list:

        configfiles = [filenames]
        """
        standard_files = []
        # Expand and define the standard config files:

        for stdconfigfile in [
                "%s/addressbook.ini"%os.path.dirname(__file__) ,
                os.path.expanduser("~/.addressbook")
                ]:

            if os.path.isfile(stdconfigfile):
                standard_files.append(stdconfigfile)
                logging.debug("Add config file [%s] to loading list."%stdconfigfile)
            else:
                logging.debug("Skipping non-existing config file [%s]."%stdconfigfile)


        # a bit of a laborious way to prepend the standard filename:
        if configfiles is None:
            configfiles = standard_files

        else:
            standard_files.extend(configfiles)
            configfiles = standard_files

        # initialise the config parser:
        c_parser = configparser.ConfigParser()

        message = "Try to read the configfile(s):"
        for filename in configfiles:
                message += " %s\n"%filename
        logging.info(message)

        try:
            c_parser.read(configfiles)

        except TypeError as error:
            logging.warning("Error parsing config files: no files provided")
        except Exception as error:
            logging.error("Error parsing config files:")
            logging.error(error)
            exit(10)

        # Start reading the Config files:
        config = {}
        for section in c_parser.sections():
            # Stuff is already structured in sections:
            config[section] = {}
            for option in c_parser.options(section):
                value = c_parser.get(section, option)
                config[section][option]=value

        cls.configuration = config

        logging.debug(cls.print_config())
        return cls.configuration

    @classmethod
    def set_config(cls, config=None):
        """

        """
        if config is None:
            gen_config  = cls.configuration["Addressbook"]
            attr_config = cls.configuration["Contact attributes"]


        try:
            for attr in attr_config:
                # Now for some magick: call the class method:
                description = attr_config[attr]
                Contact.add_allowed_attr(attr,description)

        except KeyError:
            logging.warning("""
            No [Contacts attributes] section with allowed attributes was found in
            one of the used ini-files.
            """)

        try:
            Addressbook.default_name = gen_config["default_name"]
        except KeyError:
            logging.debug("""
            Addressbook default name was not changed in any config file.
            """)

    @classmethod
    def print_config(cls):
        """
        Returns a pretty formatting of the addressbook and its contacts.
        """
        config_summary =    "Config parameters ar loaded as:\n"
        config_summary +=   "<Config>\n"
        config=cls.configuration

        for section in config:
            config_summary += "[%s]:\n"%section

            for option in config[section]:
                value = config[section][option]
                config_summary += "\t%s = %s\n"%(option,value)

        config_summary +=   "</Config>\n"
        return config_summary

    @classmethod
    def allowed_attrs_dict(cls):
        """
        Implicit refer to the allowed attributes of the Contacts class.
        """
        return Contact.allowed_attrs_dict()

class Contact(object):
    """
    A Contact object.
    New: Class Attributes
    """
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

    def __init__(self, fname, sname, **kwargs):
        """
        Create the new contact instance with firstname and family/surname

        >>> import addressbook
        >>> c = addressbook.Contact('John', 'Doe',email='john@doe.org')
        >>> print(c.full_print())
        Contact: "Doe, John"
            email = john@doe.org
            fname = John
            sname = Doe

        """
        logging.config.fileConfig(logging_configfile)

        self.fname=fname
        self.sname=sname
        for attr,value in kwargs.items():
            self.add_attr(attr, value)

    def __repr__(self):
        return '<class Contact \"%s, %s\" >'%(
                self.sname, self.fname
               )

    def full_print(self):
        text = 'Contact: \"%s, %s\"'%(
                    self.sname, self.fname)
        for attribute in sorted(self.get_attrs()):
            text += '\n    %s = %s'%(attribute,getattr(self, attribute))
        return text

    def to_dict(self):
        return { attr: getattr(self,attr) for attr in self.get_attrs() }



    def copy(self):
        newContact = Contact( "%s"%self.fname, "%s"%self.sname)
        for attribute in attributes(self):
            setattr(newContact,attribute,getattr(self,attribute))

        return newContact


    def __add__(self, other):
        """
        Actually we are going to define this as a merge: return a
        new Contact with all the properties of the old one, AND new ones from
        the "other" object.
        """
        new = self.copy()

        for att in other.get_attrs() | self.get_attrs():
            if hasattr(self,att):
                continue
            else:
                new.add_attr(att,getattr(other,att))
        return new
   # @staticmethod
   #def gen_rand_passwd():
   #    pw = ''
   #    valid_chars = 'abcdefghijklmnopqrstuvwxyz'
   #    for i in range(10:


    def add_attr(self,attr_name,attr_val):
        """
        Add an attribute, but only an allowed one
        or else ...
        >>> import addressbook
        >>> d = addressbook.Contact('John', 'Doe')
        >>> d.add_attr( 'phone', "+32(0)6345617")
        >>> sorted(d.get_attrs())
        ['fname', 'phone', 'sname']
        >>>
        """

        if attr_name in self._allowed_attributes:
            setattr(self,attr_name, attr_val)
        else:
            logging.warning("'%s' is not an allowed attribute."%attr_name)

    @classmethod
    def add_allowed_attr(cls,attr_name,attr_description):
        """
        Add an allowed attribute to the class

        >>> import addressbook
        >>> c1 = addressbook.Contact("John", "Doe")
        >>> c2 = addressbook.Contact("Jane", "Doe")
        >>> c2.add_attr('bicycle', 'Gazelle')
        >>> c1.add_allowed_attr('bicycle',"type of bicycle")
        >>> c2.add_attr('bicycle', 'Gazelle')
        >>> sorted(c2.get_attrs())
        ['bicycle', 'fname', 'sname']
        >>>
        """
        if attr_name in cls._allowed_attributes:
            # Probably we found a better description.
            logging.debug("overwriting an attribute that already existed:")
            logging.debug("\t[%s] => [%s]"%(attr_name, attr_description))

        cls._allowed_attributes[attr_name] = attr_description


    def get_attrs( self):
        """
        Obsoleted by the general function?

        >>> import addressbook
        >>> c = addressbook.Contact("John", "Doe",email='John@doe.org')
        >>> sorted(c.get_attrs())
        ['email', 'fname', 'sname']
        >>>

        """
        myattrs= set()
        for a in dir(self):
            if a.startswith('_'):
                continue
            if callable(getattr(self, a)):
                continue
            else:
                myattrs.add(a)
        return myattrs

    @classmethod
    def allowed_attrs_dict(cls):
        """
        A more public method to return a copy of the dict with allowed attributes.

        >>> import addressbook
        >>> a = addressbook.Contact.allowed_attrs_dict()
        >>> b = addressbook.Contact._allowed_attributes
        >>> a == b
        True
        >>> a is b
        False
        """
        # In order to prevent messing up the more private _allowed_attributes
        # dictionary, we return a copy to the "public" scope.
        return cls._allowed_attributes.copy()

def main (args):
    """This is an entry point to run some tests on this module"""
    import doctest

    logging_configfile = "%s/logging-addressbook.ini"%os.path.dirname(__file__)
    logging.config.fileConfig(logging_configfile,disable_existing_loggers=True)

    log = logging.getLogger('root')
    log.setLevel(logging.DEBUG)
    #console = logging.StreamHandler(stream=sys.stdout)
    #console.setLevel(logging.DEBUG)
    #log.addHandler(console)

    log.info("Loading testmod")
    # Ik vermoed dat doctest de logging messages niet doorkrijgt
    doctest.report =True
    doctest.testmod()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

