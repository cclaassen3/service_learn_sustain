import flask
import flask_login
import db
from flask import render_template, json, request, Response
import MySQLdb
import easygui

# -------------------- define app --------------------

app = flask.Flask(__name__)
user = None

class User:
    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type

# -------------------- routes -------------------

@app.route('/')
def home():
	db.setUp()
	return flask.render_template('login.html')

@app.route('/index')
def index():
    if not user: return flask.redirect('login')
    return flask.render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == "POST":
        attemptedUser = flask.request.form['username']
        attemptedPass = flask.request.form['password']
        message = db.login(attemptedUser, attemptedPass)
        if message == 0: 
        	m1 = "Invalid Credentials"
        	return flask.render_template('login.html', error=m1)
        if message == 1:
        	m1 = 1
        	return flask.render_template('cityscientist.html')
        if message == 2:
        	m2 = 2
        	return flask.render_template('cityofficial.html')
        #else: 
        #return flask.render_template('index.html')
        #TODO ensure user in database and create appropriate instance of user

@app.route('/registration')
def registration():
		return flask.render_template('registration.html')

@app.route('/postReg', methods=["POST", "GET"])
def postReg(): 
		if request.method == "POST":
			insertedUser = request.form['username']
			insertedPass = request.form['password']
			insertedEmail = request.form['email']
			insertedType = request.form['usertype']
			db.register(insertedUser, insertedEmail, insertedPass, insertedType)
			return flask.render_template('login.html')
        #elif flask.request.method == 'POST':
        #return flask.redirect('index')

@app.route('/add-new-poi-location', methods=['GET', 'POST'])
def add_new_poi_location():
    if flask.request.method == 'GET':
        # if user and user.user_type == "omnipotent":
        #     return flask.render_template('add_new_poi_location.html')
        # else: 
        #     return flask.redirect('index')
        return flask.render_template('add_new_poi_location.html')
    elif flask.request.method == 'POST':
        #return flask.redirect('index')
        return "new poi location added!"

@app.route('/add-new-data-point', methods=['GET', 'POST'])
def add_new_data_point():
    if flask.request.method == 'GET':
        return flask.render_template('add_new_data_point.html')
    elif flask.request.method == 'POST':
        return "new data point added!"


# -------------------- run app --------------------

if __name__ == '__main__': app.run()

