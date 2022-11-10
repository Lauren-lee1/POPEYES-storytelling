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
app = Flask(__name__)    #create Flask object

# creates users.db and edits.db if they don't exist already
create_tables()

username = "POPEYES"
password = "chicken"
exception = "username and pw wrong"
app.secret_key = os.urandom(32)

@app.route("/", methods=['GET', 'POST'])
def disp_loginpage():
    if 'username' in session:
        return render_template('response.html')
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
    if username in  user and password in pw:
        if request.method == 'POST':
            session['username'] = request.form['username']
        if request.method == 'GET':
            session['username'] = request.args['username']
        print(session)
        return render_template('home.html', username = username)
    #empty pw or user
    if "" == user and "" == pw:
        return render_template('login.html', message = "Please type in a username and password")
    elif "" == user:
        return render_template('login.html', message = "Please type in a username")
    elif "" == pw:
        return render_template('login.html', message = "Please type in a password")
    #wrong pw or user
    if user != username and pw != password:
        return render_template('login.html', message = "Please input a correct username and password")
    elif user != username:
        return render_template('login.html', message = "Please input a correct username")
    elif pw != password:
        return render_template('login.html', message = "Please input a correct password")
    #unidentified error
    else:
        return render_template('login.html', message = "unidentified")

@app.route("/home", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['pass']
    if request.method == 'GET':
        user = request.args['username']
        pw = request.args['pass']

    # ##adds data into db
    # if user_does_not_exists(username):
    #     # add user to students.db
    #     add_user(username, password)

    
    return render_template('home.html', username = username)

@app.route("/logout", methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')
    return redirect('http://127.0.0.1:5000/')
  



    
if __name__ == "__main__": #false if this file imported as module
    #enable debugging, auto-restarting of server when this file is modified
    app.debug = True 
    app.run()
