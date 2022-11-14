# POPEYES: Lauren Lee, Vivian Teo, Ian Jiang
# SoftDev
# P00 -- Storytelling
# 2022-11-0
# time spent: 

import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

from db_user import *

from time import ctime      #use to get time last edited

def create_edits_table():
    # edits table
    DB_FILE="edits.db"

    db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
    c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

    c.execute("CREATE TABLE IF NOT EXISTS edits(id INTEGER PRIMARY KEY, title TEXT, content TEXT, time TEXT, latest_change TEXT)")
    
    db.commit() #save changes
    db.close()  #close database

'''
Used for edits.db
Creates new story
'''
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

'''
Used for edits.db
Gets id of current story
    used for add_to_contributed(id,user)
'''
def get_id(title):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    #get id of story with given title
    current_id = c.execute(f"SELECT id FROM edits WHERE title = '{title}'").fetchone()

    db.commit()
    db.close()
    return str(current_id[0])

'''
Used for edits.db
Checks if story exists
'''
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

def see_full(user, story_id):
    all_contributed = all_stories_contributed_to(user)
    for x in all_contributed:
        print(type(x))
        if x == int(story_id):
            return True
    return False

def get_title(story_id):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    title = c.execute(f"SELECT title FROM edits WHERE id = '{story_id}'").fetchone()[0]
    db.commit() #save changes
    db.close()  #close database

    return title


def get_all_stories(user):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()

    all_stories = c.execute(f"SELECT title FROM edits").fetchall()
    for tupl in range(len(all_stories)):
        ret_tupl = ""
        for y in all_stories[tupl]:
            ret_tupl = ret_tupl + y
        all_stories[tupl] = ret_tupl

    #assumes title is same but we should allow diff
    user_view = {}
    for x in all_stories:
        print(x)
        id = c.execute(f"SELECT id FROM edits WHERE title = '{x}'").fetchone()[0]
        user_view[x] = id
    db.commit() #save changes
    db.close()  #close database

    return user_view

def edit_story(user,text,id):
    DB_FILE="edits.db"
    db = sqlite3.connect(DB_FILE)
    c = db.cursor()    

    print(id)
    # add to edits the latest change and replace content
    content = c.execute(f"SELECT content FROM edits WHERE id = {id}").fetchone()[0]
    content += " " + text
    c.execute(f"UPDATE edits SET latest_change = '{text}' WHERE id = {id}")
    c.execute(f"UPDATE edits SET content = '{content}' WHERE id = {id}")

    # add this story to the list of contributed in users.db
    title = c.execute(f"SELECT title FROM edits WHERE id = {id}").fetchone()[0]
    add_to_contributed(title, user) # update the list of contributed stories

    db.commit() #save changes
    db.close()  #close database

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