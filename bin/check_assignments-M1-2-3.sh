#!/bin/bash

echo "going through python functions:"
python3 check_assignments-Module-1.py

echo "===================================="
echo 'The solution to Exercise 1.7.4.1:
    Argument parsing:
    Copy or link the argparse_exercise.py twice:
    create_contact -> argparse_exercise.py
    create_addrbook -> argparse_exercise.py
    -----------
    ' 

COMMAND='./create_contact --firstname John --surname Doe --attr email john@doe.org'
echo $COMMAND
$COMMAND
echo ""
COMMAND='./create_addrbook --name "MyAddressbook" '
echo "Executing: $COMMAND"
$COMMAND
echo "===================================="
echo 'Exercise 2.6.1.[1-6]
      doctest: execute the module addressbook/src/addressbook.py
      '

COMMAND='../src/addressbook/addressbook.py'
echo "Executing: $COMMAND"
$COMMAND
echo 'Doctest finished (successfully?)

    '

echo "===================================="
echo 'Exercise 2.6.1.7
    Advantages of Doctest:
    * Simple demonstration of code usage.
    * Quick testing ability of small & fast modifications.
    * Enables test driven development close to the code itself.
    * ...
    Disadvantage
    * For complex tests it clutters the docstring.'
echo "===================================="

echo '
    Exercise 2.6.2.[1-5]
    Unittest: illustrated via ../test/test_with_unittest.py
    '
COMMAND='../test/test_with_unittest.py'
echo "Executing: $COMMAND"
$COMMAND

echo "===================================="

echo '
    Exercise 2.6.3.[1-4]
    Pytest: implemented and illustrated via shell command:
    '
cd ../
COMMAND="python3 -m pytest -v "
echo "Executing: $COMMAND"
$COMMAND
cd -

echo "===================================="

echo "Continuing to Module 3:"
python3 check_assignments-Module-3.py 

echo "Continuing to Module 4:"
echo "The console loglevel is set to WARNING to prevent a \`shitload\' of SQL messages"
echo "This can be modified in src/addressbook/logging:"
echo "The files addressbook.ini and orm.ini"

python3 check_assignments-Module-4.py 

