#!/bin/sh -v
#./argparse_exercise -f John -s Doe --attr phone +316342131
#./create_contact -f John -s Doe 
echo("Test Python advanced: Exercise 7.4")
# Requires the (soft) linking of the python script to both 
# the names that are called below.
# ln -s argparse_exercise create_contact
# ln -s argparse_exercise create_addressbook


./create_contact -f John -s Doe --attr phone +316342131
./create_addrbook -n MyAddressbook
