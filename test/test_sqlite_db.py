#!/usr/bin/env python3
import addressbook
import sqlite3
import pytest
from os.path import isfile, getsize

def isSQLite3(filename):

    if not isfile(filename):
        return False
    if getsize(filename) < 100: # SQLite database file header is 100 bytes
        return False

    with open(filename, 'rb') as fd:
        header = fd.read(100)

    return header[:16] == b'SQLite format 3\x00'

def test_create_database(tmpdir):
    """
    Test the creation of a plain database.
    """

    dbfile = "%s/test.db"%tmpdir
    # Before we can test if it is a proper sqlite file, we set it up first.
    con = sqlite3.connect(dbfile)
    addressbook.db.initialize_addressbook_db_schema(con)
    assert isSQLite3(dbfile)

def test_create_table_in_db(tmpdir):
    dbfile = "%s/test.db"%tmpdir
    testTableName = "tesTable"

    con = sqlite3.connect(dbfile)
    cursor = con.cursor()

    query = "CREATE TABLE table ( id INTEGER, name CHAR(30) );"
    query = query.replace('table',testTableName)
    cursor.execute(query)
    con.commit()
    con.close()

    newCon = sqlite3.connect(dbfile)
    cursor = newCon.cursor()
    # Get all tables:
    query = "SELECT name FROM sqlite_master WHERE type='table'"
    cursor.execute(query)
    tables = [row[0] for row in cursor.fetchall()]
    # And finally test if the table is in the database indeed.

    assert testTableName in tables

def test_create_record_table_in_db(tmpdir):
    dbfile = "%s/test.db"%tmpdir
    testTableName = "tesTable"
    testId = 42
    testName = "Ford Prefect"

    con = sqlite3.connect(dbfile)
    cursor = con.cursor()

    query = "CREATE TABLE table ( id INTEGER, name CHAR(30) );"
    query = query.replace('table',testTableName)
    cursor.execute(query)

    query = "INSERT INTO table (id,name) VALUES (?,?)"
    query = query.replace('table',testTableName)
    params = (testId, testName)
    cursor.execute(query,params)
    con.commit()
    con.close()

    newCon = sqlite3.connect(dbfile)
    cursor = newCon.cursor()
    query = "SELECT * FROM table"
    query = query.replace('table',testTableName)
    records = cursor.execute(query).fetchall()

    assert (testId,testName) in records
if __name__ == '__main__':
    pytest.main()

