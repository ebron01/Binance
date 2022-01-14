import sqlite3
import pandas as pd
import sqlalchemy

connection = sqlite3.connect('/OurDataBase.db') #creates a new database if there is none.
cursor = connection.cursor()#we can execute sql commands with this cursor.

#sqlite datatypes INT, REAL, TEXT, BLOBS, NULL
"""Executed only once"""
#cursor.execute("CREATE TABLE employees(name TEXT, surname TEXT, salary REAL)")
#connection.commit()

"""Executed only once"""
# cursor.execute("INSERT INTO employees VALUES('Maria', 'Mayer', 100000)")
# connection.commit()

cursor.execute("SELECT * FROM employees")
print(cursor.fetchall()) #makes the query visible, to see again must execute one line above again

name = 'King'
surname = 'Arthur'
salary = 50000
cursor.execute("INSERT INTO employees VALUES(?, ?, ?)", (name, surname, salary))
connection.commit()

class SQLinput:
    def __init__(self, name, surname, salary):
        self.name = name
        self.surname = surname
        self.salary = salary

inst = SQLinput('Denzel', 'Sullivan', 5000)
name, surname, salary = inst.name, inst.surname, inst.salary
cursor.execute("INSERT INTO employees VALUES(?, ?, ?)", (name, surname, salary))
connection.commit()
cursor.execute("SELECT * FROM employees")
print(cursor.fetchall()) #makes the query visible, to see again must execute one line above again