import os
import sys
import sqlite3


class MetaSingleton(type):
    """ Insures only a single connection to the database is available at the time. """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton,cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Ledger_bk(MetaSingleton):
    connection = None
    def __init__(self):
        os.chdir(os.path.dirname(os.path.realpath(__file__)))
        self.cursor, self.connection = self.connect()
        
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Contact(id INTEGER PRIMARY KEY,Name TEXT,Age INTEGER, Gender TEXT,Phone INTEGER,Mail TEXT,Address TEXT)")
    
    
    def connect(self):
        """ Makes sure to make a connection to the database, if no connection is active. """
        if self.connection is None:
            self.connection = sqlite3.connect("ledger.db")
            self.cursor = self.connection.cursor()
        return self.cursor, self.connection
        
        
    def viewall(self):
        self.cursor.execute("SELECT * FROM Contact")
        rows = self.cursor.fetchall()
        return rows


    def search(self, Name="",Age="",Gender="",Phone="",Mail="",Address=""):
        self.cursor.execute("SELECT * FROM Contact WHERE Name=? OR Age=? OR Gender=? OR Phone=? OR Mail=? OR Address=?",(Name,Age,Gender,Phone,Mail,Address))
        rows = self.cursor.fetchall()
        return rows


    def add(self, Name,Age,Gender,Phone,Mail,Address):
        self.cursor.execute("INSERT INTO Contact VALUES(NULL,?,?,?,?,?,?)",(Name,Age,Gender,Phone,Mail,Address))
        self.connection.commit()


    def update(self, id,Name,Age,Gender,Phone,Mail,Address):
        self.cursor.execute("UPDATE Contact SET Name=?,Age=?,Gender=?,Phone=?,Mail=?,Address=? WHERE id=?",(Name,Age,Gender,Phone,Mail,Address,id))
        self.connection.commit()


    def delete(self, id):
        self.cursor.execute("DELETE FROM Contact WHERE id=?",(id,))
        self.connection.commit()


"""
IN MAIN SCRIPT

from ledger_bk import Ledger_bk

database = Ledger_bk()
...
do what you need to do with the database like:

database.viewall()

close connections a single time, preferably when the project exits 

if sys.exit():
    database.cursor.close()
    database.connection.close()

"""
