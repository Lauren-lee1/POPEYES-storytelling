# POPEYES: Lauren Lee, Vivian Teo, Ian Jiang
# SoftDev
# P00 -- Storytelling
# 2022-11-0
# time spent: 

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

from time import ctime      #use to get time last edited

# # delete table if needed (testing purposes)
# DB_FILE="edits.db"
# db = sqlite3.connect(DB_FILE) 
# c = db.cursor() 
# # c.execute("DELETE FROM edits")
# # # c.execute("DELETE FROM users")

# table = c.execute("SELECT * from edits")
# print(table.fetchall())

# db.commit()
# db.close()

'''
Used for both users.db and edits.db
creates users.db and edits.db if it does not already exists
'''
def create_user_table():
    # users table
    DB_FILE="users.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
    # users table
    c.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, name TEXT, pw TEXT, id_list TEXT, editing TEXT)")
    
    db.commit() #save changes
    db.close()  #close database

'''
Used for user.db
Adds users who have registered into the database
'''
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

'''
Used for user.db
checks if user is already in the database prior to registration
'''
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

'''
Used for user.db
Checks if login credentials match any in the database
'''
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


'''
Used for edits.db
Adds the story the user contributed to to their id_list
'''
def add_to_contributed(title, user):
    DB_FILE="users.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    current_id = get_id(title)
    print("-------------------------------------------------------")
    print(current_id)
    
    id_list = str(c.execute(f"SELECT id_list FROM users WHERE name = '{user}'").fetchone()[0])
    print(id_list)

    if id_list == "None":
        c.execute(f"UPDATE users SET id_list = '{current_id}' WHERE name = '{user}'")
    else:
        current_id = id_list + ", " + current_id
        c.execute(f"UPDATE users SET id_list = '{current_id}' WHERE name = '{user}'")
    
    print(c.execute("SELECT id_list FROM users").fetchall())

    db.commit()
    db.close()
    

'''
Used for edits.db
outputs a dict containing all the stories user contributed to
'''
def all_stories_contributed_to(user):
    DB_FILE="users.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    id_list = c.execute(f"SELECT id_list FROM users WHERE name = '{user}'").fetchone()[0]
    print(id_list)

    if id_list is None:
        id_list = []
    else:
        id_list = id_list.split(",")

    print(id_list)

    db.commit() #save changes
    db.close()  #close database

    ret_val = all_stories_contributed_to_helper(id_list,user)

    return ret_val

def see_full(user, story_id):
    all_contributed = all_stories_contributed_to(user)
    for x in all_contributed:
        print(type(x))
        if x == int(story_id):
            return True
    return False

def story_content(user, story_id):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    if see_full(user, story_id):
        ret_val =  c.execute(f"SELECT content FROM edits WHERE id = '{story_id}'").fetchone()[0]
    else:
        ret_val = c.execute(f"SELECT latest_change FROM edits WHERE id = '{story_id}'").fetchone()[0]
    db.commit() #save changes
    db.close()  #close database
    return ret_val

# print(all_stories_contributed_to("ian"))
# all_stories_contributed_to("ian")

def all_stories_contributed_to_helper(id_list,user):
     #now that we have a dict of the story ids the user has contributed to, we can closer users.db and extract the content from edits.db
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #our final output (huge string)
    final_dict = {}

    # for each story id in the list, we'll extract the title + content out and put it in final_text
    for story_id in id_list:
        #title
        title = c.execute(f"SELECT title FROM edits WHERE id = {story_id}").fetchone()[0]
        #content
        content = c.execute(f"SELECT content FROM edits WHERE id = {story_id}").fetchone()[0]
        #story id
        id = c.execute(f"SELECT id FROM edits WHERE id = {story_id}").fetchone()[0]
        #add to dict
        final_dict[id] = [title, content]
    db.commit() #save changes
    db.close()  #close database

    return final_dict

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

