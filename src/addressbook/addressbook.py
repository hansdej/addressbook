#!/usr/bin/env python3
# "object" is een caompatibility dingetje met Python  2
import sys
import os
import logging
import configparser
import csv
#import json

def attributes(thing):
    """
    The helper function to get all the regular attributes
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
    default_name = "Myn Addressbook"
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
        if Addressbook.config_read is False:
            self.read_config()
            self.set_config()
        if name is None:
            name = Addressbook.default_name

        self.name       = name
        self._contacts  = []
        self._newId     = 0 # Use the underscore to prevent it be copied in a copy.

    def __add__(self, added):
        newbook = self.copy()

        if isinstance(added,Contact):
            # Add one contact 
            newbook.add_contact(added)

        elif isinstance(added,Addressbook):
            # Merge the second addressbook
            for contact in added:
                newbook.add_contact(contact)

        return newbook        
		
    def __len__(self):
        """ The number of contacts is a usefull length """
        return len(self._contacts)
	
    def __repr__(self):
        return '<class Addressbook \"%s\", containing %d contacts>'%(
            self.name, len(self)
            )

    def __iter__(self):
        # Should return an iterator object
        return iter(self._contacts)


    def copy(self):
        """
        Make a copy of the addressbook
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
        newContact  = contact.copy()
                        # We could also iterate through the existing
                        # list of contacts and check with "is" if the
                        # contact is already there and then refuse to
                        # add this contact to the list an additional
                        # time again, but that 's a bit too complex
                        # for now.
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
        for item in range(len(Clist)):
            if fname == Clist[item].fname and sname == Clist[item].sname:
                logging.debug("We got a hit on Id %d:\n %s"%(
                            Clist[item]._Id,
                            Clist[item].full_print()
                            ))
                if Id is None or Clist[item]._Id == Id:    
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
        list = "%s\n"%self
        for contact in self._contacts: 
            list += contact.full_print()
        return list    


    def read_config(self, configfiles=None):
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

        self.configuration = config        

        logging.debug(self.print_config())
        return self.configuration

    def set_config(self, config=None):
        """
        """
        if config is None:
            config = self.configuration

        allowed_attributes = "Contact attributes"
        
        try:
            for attr in config[allowed_attributes]:
                # Now for some magick: call the class method:
                description = config[allowed_attributes][attr]
                Contact.add_allowed_attr(attr,description)
        
        except:
            logging.warning("""
            No [Contacts attributes] section with allowed attributes was found in
            one of the used ini-files.
            """)

        try:
            Addressbook.default_name=config["Addressbook"]["default_name"]
        except:
            logging.debug("""
            Addressbook default name was not changed in any config file.
            """)

    def print_config(self):
        config_summary =    "Config parameters ar loaded as:\n"
        config_summary +=   "<Config>\n"
        config=self.configuration

        for section in config:
            config_summary += "[%s]:\n"%section

            for option in config[section]:
                value = config[section][option]
                config_summary += "\t%s = %s\n"%(option,value)

        config_summary +=   "</Config>\n"
        return config_summary

        


    def import_csv(self,csvfilename):

        if os.path.exists(csvfilename):

            with open(csvfilename, 'rU') as csvfile: 
                csv_content = csv.reader(csvfile,delimiter=',', quotechar='"')
                for row in csv_content:
                    fname = row[4]
                    sname = row[6]
                    email = row[14]
                    newcontact = Contact(fname, sname)
                    newcontact.add_attr('email',email)
                    self.add_contact( newcontact)
	
    def export_json(self):
        # create the proper list 
        #jsondict = {"Addressbook"}
        pass
        
	
class Contact(object):
    """
    A Contact object.
    New: Class Attributes
    """
    _allowed_attributes ={
       'Id'    :"Id number",
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

    def __init__(self, fname, sname):
        """
        Create the new contact instance

        >>> import addressbook
        >>> c1 = addressbook.Contact('John', 'Doe')
        >>> c1
        <class Contact "Doe, John" >
        """

        self.fname=fname
        self.sname=sname

    def __repr__(self):
        return '<class Contact \"%s, %s\" >'%(
                self.sname, self.fname
               )

    def full_print(self):
        text = '<Contact: \"%s, %s\">\n'%(
                    self.sname, self.fname)
        for attribute in sorted(self.get_attrs()):
            text += '\t%s = %s\n'%(attribute,getattr(self, attribute))
        return text



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
                
        for att in  other.get_attrs() | self.get_attrs() :
            if hasattr(self,att) :
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
        Example and doctest:

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

def main (args):    
    """This is an entry point to run some tests on this module"""
    import doctest

    logging.basicConfig(
            level = logging.DEBUG
            )

    log = logging.getLogger(__name__)
    log.setLevel(logging.DEBUG)
    console = logging.StreamHandler(stream=sys.stdout)
    console.setLevel(logging.DEBUG)
    log.addHandler(console)


    logging.info("Loading testmod")
    # Ik vermoed dat doctest de logging messages niet doorkrijgt
    doctest.report =True
    doctest.testmod()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))

