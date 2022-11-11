# POPEYES: Lauren Lee, Vivian Teo, Ian Jiang
# SoftDev
# P00 -- Storytelling
# 2022-11-0
# time spent: 

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

from time import ctime      #use to get time last edited

#delete table if needed (testing purposes)
# DB_FILE="edits.db"
# db = sqlite3.connect(DB_FILE) 
# c = db.cursor() 
# # c.execute("DROP TABLE edits")
# # c.execute("DELETE FROM users")

# table = c.execute("SELECT * from edits")
# print(table.fetchall())
# db.commit()
# db.close()
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
    
    #prints users table
    table = c.execute("SELECT * from users")
    print(table.fetchall())

    db.commit() #save changes
    db.close()  #close database

def user_does_not_exists(user):
    DB_FILE="users.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    
    namie = c.execute("SELECT name FROM users WHERE name = '"+ user + "'").fetchone()
    # print(namie)
    if namie is None:
        exists = False
    else:
        exists = True

    # prints users table
    table = c.execute("SELECT * from users")
    print(table.fetchall())
    
    print(exists)

    db.commit() #save changes
    db.close()  #close database
    return exists == False

def correct_account(user, passw):
    DB_FILE="users.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    
    # check if username is in table
    namie = c.execute("SELECT name FROM users WHERE name = '"+ user + "'").fetchone()
    print(namie)
    if namie is None:
        exists = False
    else:
        exists = True

    # check if password is in table
    passie = c.execute("SELECT pw FROM users WHERE pw = '"+ passw + "'").fetchone()
    print(passie)
    if passie is None:
        exists = False

    # prints table
    table = c.execute("SELECT * from users")
    print(table.fetchall())
    
    print(exists)

    db.commit() #save changes
    db.close()  #close database
    return exists

def add_story(title, text):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #adds story into database
    c.execute(f"INSERT INTO edits (title, content, time, latest_change) VALUES ('{title}', '{text}', '{ctime()}', '{text}')")

    #print content into terminal
    print(c.execute("SELECT content FROM edits").fetchall())
    db.commit() #save changes
    db.close() #close database

# def add_to_contributed(id, user):
#     DB_FILE="users.db"
#     db = sqlite3.connect(DB_FILE)
#     c = db.cursor()

#     id_list = c.execute(f"SELECT id_list FROM users WHERE name = '{user}'").fetchone()
#     if id_list is None:
#         c.execute(f"UPDATE users SET id_list = '{id}' WHERE name = '{user}'")
#     else:
#         c.execute(f"UPDATE users SET id_list = '{id_list}{id}' WHERE name = '{user}'")
    
#     db.commit()
#     db.close()
    
#used for add_to_contributed(id,user)
def get_id(title):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #get id of story with given title
    id = c.execute(f"SELECT id FROM edits WHERE title = '{title}'").fetchone()

    db.commit()
    db.close()
    return id

def story_does_not_exist(title):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    
    titlie = c.execute(f"SELECT title FROM edits WHERE title = '{title}'").fetchone()
    if titlie is None:
        exists = False
    else:
        exists = True
    
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

