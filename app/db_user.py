# POPEYES: Lauren Lee, Vivian Teo, Ian Jiang
# SoftDev
# P00 -- Storytelling
# 2022-11-0
# time spent: 

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O


# #delete table if needed (testing purposes)
# DB_FILE="users.db"
# db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
# db.execute("DROP TABLE if exists users")

def create_tables():
    # users table
    DB_FILE="users.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    # users table
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, pw TEXT, id_list TEXT, editing TEXT)")
    
    db.commit() #save changes
    db.close()  #close database

    # edits table
    DB_FILE="edits.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    c.execute("CREATE TABLE IF NOT EXISTS edits(id INTEGER PRIMARY KEY, title TEXT, content TEXT, time TEXT, latest_change TEXT)")
    
    db.commit() #save changes
    db.close()  #close database

def add_user(user, passw):
    DB_FILE="users.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    # add newly registered people in

    c.execute("INSERT INTO users (name, pw) VALUES ('"+user+"', '"+passw+"')")
    table = c.execute("SELECT * from users")
    print(table.fetchall())
    db.commit() #save changes
    db.close()  #close database

def user_does_not_exists(user):
    DB_FILE="users.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    
    num = c.execute("SELECT 1 FROM users WHERE name = '"+ user + "'")
    print(num.fetchone())
    if num is None:
        exists = False
    else:
        exists = True

    print(exists)
    db.commit() #save changes
    db.close()  #close database
    return exists == False


'''
# with open('students.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         c.execute("INSERT INTO students VALUES ('" + row['name'] + "', " + row['age'] + "," + row['id'] + ")")

students_table = c.execute("SELECT * FROM students")
print(students_table.fetchall())

# courses table
DB_FILE="courses.db"

db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

db.execute("DROP TABLE if exists courses")
c.execute("CREATE TABLE courses(code TEXT, mark INTEGER, id INTEGER)")

with open('courses.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        c.execute("INSERT INTO courses VALUES ('" + row['code'] + "', " + row['mark'] + "," + row['id'] + ")")

courses_table = c.execute("SELECT * FROM courses")
'''


# command = ""          # test SQL stmt in sqlite3 shell, save as string
# c.execute(command)    # run SQL statement

#==========================================================

