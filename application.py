from flask import render_template, json, request, Response
import flask_login
import MySQLdb
import easygui
import flask
import db


# -------------------- define app --------------------

app = flask.Flask(__name__)
user = None

class User:
    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type

'''
  user_types:
    1 --> City Scientist
    2 --> City Official
    3 --> Admin
'''

# -------------------- routes -------------------

@app.route('/')
def home():
    return flask.redirect('login')

@app.route('/index')
def index():
    return flask.render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == "GET":
        return flask.render_template("login.html")
    elif flask.request.method == "POST":
        attemptedUser = flask.request.form['username']
        attemptedPass = flask.request.form['password']
        user_type = db.login(attemptedUser, attemptedPass)
        if not user_type: return flask.render_template('login.html', error="Invalid Credentials")
        global user
        user = User(attemptedUser, user_type)
        if user_type == 1: return flask.render_template('cityscientist.html')
        elif user_type == 2: return flask.render_template('cityofficial.html')
        elif user_type == 3: return flask.render_template('admin')

@app.route('/register', methods=["POST", "GET"])
def registration():
    if request.method == "GET":
        return flask.render_template('registration.html')
    if request.method == "POST":
        insertedUser = request.form['username']
        insertedPass = request.form['password']
        insertedEmail = request.form['email']
        insertedType = request.form['usertype']
        accepted = db.register(insertedUser, insertedEmail, insertedPass, insertedType)
        if not accepted: return flask.render_template('registration.html', error="Registration Failure")
        return flask.render_template('login.html')

@app.route('/add-new-poi-location', methods=['GET', 'POST'])
def add_new_poi_location():
    if not user: return flask.redirect('login')
    if user.user_type != 1: return flask.render_template('unauthorized.html')
    if flask.request.method == 'GET':
        return flask.render_template('add_new_poi_location.html')
    elif flask.request.method == 'POST':
        locationName = request.form['location_name']
        city = request.form['city']
        state = request.form['state']
        zipCode = request.form['zip_code']
        db.addNewPOILocation(locationName, city, state, zipCode)
        return "new poi location added!"

@app.route('/add-new-data-point', methods=['GET', 'POST'])
def add_new_data_point():
    if not user: return flask.redirect('login')
    if user.user_type != 1: return flask.render_template('unauthorized.html')
    if flask.request.method == 'GET':
        return flask.render_template('add_new_data_point.html')
    elif flask.request.method == 'POST':
        poiLocation = request.form['poi_location']
        date = request.form['date']
        dataType = request.form['data_type']
        value = request.form['value']
        db.addNewDataPoint(poiLocation, date, dataType, value)
        return "new data point added!"


# -------------------- run app --------------------

if __name__ == '__main__': 
    db.setUp()
    app.run()

