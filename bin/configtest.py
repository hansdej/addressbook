#!/usr/bin/env python3

import addressbook
import configparser
import logging

ab = addressbook.Addressbook()
c1 = addressbook.Contact('John', 'Doe')


print(ab)
print(c1)

logging.basicConfig(
    #filename='config_test.log',
    format='%(asctime)s %(levelname)s PID=%(process)d, %(module)s:%(lineno)d: %(message)s',
    level=logging.DEBUG
    )


config_files = ['/etc/addressbook.conf',
                '~/.config/addressbook.conf',
                'addressbook.ini']
print(config_files)
c_parser = configparser.ConfigParser()
try: 
    c_parser.read(config_files)
except TypeError as e:
    logging.warning("Error parsing config file: no config file provided")
except Exception as e:    
    logging.error("Error parsing config file:\n ")
    logging.error(e.message)
    exit(10)
config_dict = {}
for section in c_parser.sections():
    config_dict[section] = {}
    for option in c_parser.options(section):
        value = c_parser.get(section, option)
        config_dict[section][option] = value

for s in config_dict:
    print("\nsection: [%s]"%s)
    for o in config_dict[s]:
        v = config_dict[s][o]
        print("\t[%s]\t= [%s]"%(o, v))
    print("\n")

 
