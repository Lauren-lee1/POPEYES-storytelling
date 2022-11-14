# POPEYES: Lauren Lee, Vivian Teo, Ian Jiang
# SoftDev
# P00 -- Storytelling
# 2022-11-0
# time spent: 



#the conventional way:
import re
from flask import Flask, render_template, request, session, redirect
import os
from db_user import *
#from db_edits import *
app = Flask(__name__)    #create Flask object

# creates users.db and edits.db if they don't exist already
# create_user_table()
# create_edits_table()
create_tables()

exception = "username and pw wrong"
app.secret_key = os.urandom(32)

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    if 'username' in session:
        return render_template('home.html', username = session['username'], all_stories = get_all_stories(session['username']),  stories = all_stories_contributed_to(session['username']))
    return render_template('login.html', message = "Type in a username and password")  


@app.route("/auth", methods=['GET', 'POST'])
def authenticate():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['pass']
    if request.method == 'GET':
        user = request.args['username']
        pw = request.args['pass']

    #pw and user correct
    if correct_account(user,pw):

        #make sessions
        if request.method == 'POST':
            session['username'] = request.form['username']
        if request.method == 'GET':
            session['username'] = request.args['username']
        print(session)

        return render_template('home.html', username = user, message = "",all_stories = get_all_stories(session['username']), stories = all_stories_contributed_to(user))
    #pw/user incorrect
    else:
        return render_template('login.html', message = "Please input a correct username and password")


    #empty pw or user
    if "" == user and "" == pw:
        return render_template('login.html', message = "Please type in a username and password")
    elif "" == user:
        return render_template('login.html', message = "Please type in a username")
    elif "" == pw:
        return render_template('login.html', message = "Please type in a password")    
    #unidentified error
    else:
        return render_template('login.html', message = "unidentified")

@app.route("/home", methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return render_template('home.html', username = session['username'], all_stories = get_all_stories(session['username']),  stories = all_stories_contributed_to(session['username']))
    else:
        if request.method == 'POST':
            user = request.form['username']
            pw = request.form['pass']
        if request.method == 'GET':
            user = request.args['username']
            pw = request.args['pass']

        if user == "" or pw == "":
            return render_template('login.html', message = "You cannot leave username and password blank")
        ##adds data into db
        if user_does_not_exists(user):
            # add user to students.db
            add_user(user, pw)

            # make sessions
            if request.method == 'POST':
                session['username'] = request.form['username']
            if request.method == 'GET':
                session['username'] = request.args['username']
            print(session)

            return render_template('home.html', username = user, message = "", all_stories = get_all_stories(session['username']), stories = all_stories_contributed_to(user))
        else:
            return render_template('login.html', message = "User already exists")

@app.route("/submit", methods=['GET', 'POST'])
def submit_story():
    if request.method == 'POST':
        text = request.form['text']
        title = request.form['title']
    if request.method == 'GET':
        text = request.args['text']
        title = request.args['title']   

    if 'username' in session:
        if story_does_not_exist(title):
            add_story(title, text) # add the text to the database
            add_to_contributed(title, session['username']) # update the list of contributed stories
            message = ""
        else:
            message = "story already exists"
        print(session)
        return render_template('home.html', username = session['username'], message = message, all_stories = get_all_stories(session['username']), stories = all_stories_contributed_to(session['username']))

    else:
        return render_template('login.html', message = "Type in a username and password")  

@app.route("/story/<path:id>", methods=['GET', 'POST'])
def view_story(id):
    if 'username' in session:
        title = get_title(id)
        content = story_content(session['username'],id )
        return render_template('story.html', content = content, title = title, id = id, message = '')  
    else:
        return render_template('login.html', message = "Type in a username and password")  

@app.route("/edit/<path:id>", methods=['GET', 'POST'])
def add_to_story(id):
    if request.method == 'POST':
        text = request.form['text']
    if request.method == 'GET':
        text = request.args['text']

    if 'username' in session:
        if(see_full(session['username'], id)) == True:
            title = get_title(id)
            content = story_content(session['username'],id )
            print("************")
            return render_template('story.html', content = content, title = title, id = id, message = 'you cannot edit this story')  
        else:
            edit_story(session['username'], text, id)
            print(session)
            print("test")
            return render_template('home.html', username = session['username'], message = "", all_stories = get_all_stories(session['username']), stories = all_stories_contributed_to(session['username']))
    else:
        return render_template('login.html', message = "Type in a username and password")  



@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect('http://127.0.0.1:5000/')
  



    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
