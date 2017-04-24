from flask import render_template, json, request, Response
from datetime import datetime
import flask_login
import MySQLdb
import easygui
import flask
import db


# -------------------- define app --------------------

app = flask.Flask(__name__)
permissions_enabled = False
user = None
poiLocation = None

class User:
    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type


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
        if user_type == 'unapprovedCO': return flask.render_template('login.html', error="Account Not Yet Approved by Admin")
        if not user_type: return flask.render_template('login.html', error="Invalid Credentials")
        global user
        user = User(attemptedUser, user_type)
        return flask.redirect(user_type)

@app.route('/register', methods=["POST", "GET"])
def registration():
    if request.method == "GET":
        return flask.render_template('registration.html', cities=db.retrieveCities(), states=db.retrieveStates())

    if request.method == "POST":
        insertedUser = request.form['username']
        insertedPass = request.form['password']
        confirmedPass = request.form['confpassword']
        insertedEmail = request.form['email']
        insertedType = request.form['usertype']
        if not insertedUser or not insertedPass or not insertedEmail or not insertedType: return flask.render_template('registration.html', cities=db.retrieveCities(), states=db.retrieveStates(), error="Please Complete All Fields")
        if insertedPass != confirmedPass: return flask.render_template('registration.html', error="Passwords Do Not Match")

        #ensure username and email not already taken
        if db.existsUsername(insertedUser): return flask.render_template('registration.html', cities=db.retrieveCities(), states=db.retrieveStates(), error="Username Already Exists")
        elif db.existsEmail(insertedEmail): return flask.render_template('registration.html', cities=db.retrieveCities(), states=db.retrieveStates(), error="Email Already Exists")

        #parse city official info
        city = request.form['city'].replace('+', ' ')
        state = request.form['state'].replace('+', ' ')
        title = request.form['title']
        if insertedType == 'City Official':
            if not city or not state or not title: return flask.render_template('registration.html', cities=db.retrieveCities(), states=db.retrieveStates(), error="Please fill out all City Official Fields")
            if not db.existsCityState(city, state): return flask.render_template('registration.html', cities=db.retrieveCities(), states=db.retrieveStates(), error="Invalid City State Combination")

        #add to DB
        accepted = db.register(insertedUser, insertedEmail, insertedPass, insertedType)
        if accepted and insertedType == 'City Official': db.addCityOfficial(insertedUser, city, state, title)
        if not accepted: return flask.render_template('registration.html', cities=db.retrieveCities(), states=db.retrieveStates(), error="Registration Failure")
        return flask.redirect('login')

@app.route('/poi-details', methods=["POST", "GET"])
def poiDetails(): 
    global poiLocation
    if request.method == "GET":
        poiLocationName = str(poiLocation)
        data = db.retrieveDataForLocation(poiLocationName)
        return flask.render_template('poi-details.html', poilocation = poiLocationName, data_points = data, types = db.retrieveDataTypes())
    elif flask.request.method == 'POST':
        datatype = request.form['poi_type']
        print datatype
        rangestart = request.form['rangestart']
        print rangestart
        rangeend = request.form['rangeend']
        print rangeend
        date1 = request.form['datetime1']
        print date1
        date2 = request.form['datetime2']
        print date2
        data = db.retrieveDataForPOIDetails(poiLocation, date1, date2, rangestart, rangeend, datatype)
        print data
        return flask.render_template('poi-details.html', poilocation = poiLocation, data_points = data, types = db.retrieveDataTypes())

@app.route('/logout')
def logout():
    return flask.redirect('/login')

@app.route('/cityScientist')
def cityScientist():
    if permissions_enabled and not user: return flask.redirect('login')
    return flask.render_template('cityscientist.html')

@app.route('/cityOfficial')
def cityOfficial():
    if permissions_enabled and not user: return flask.redirect('login')
    return flask.render_template('cityofficial.html')

@app.route('/admin')
def admin():
    if permissions_enabled and not user: return flask.redirect('login')
    return flask.render_template('admin.html')

@app.route('/search-data-point', methods=['GET', 'POST'])
def search_data_points():

    if permissions_enabled and not user: return flask.redirect('login')

    if flask.request.method == 'GET':
        return flask.render_template('search-data-point.html', locations=db.retrievePOILocations(), datatype = db.retrieveDataTypes(), cities = db.retrieveCities(), states = db.retrieveStates(), data_points="")

    elif flask.request.method == 'POST':
        location = request.form['poi_location'].replace('+', ' ')
        city = request.form['city'].replace('+', ' ')
        state = request.form['state'].replace('+', ' ')
        zipcode = request.form['zip_code']
        date1 = request.form['datetime1']
        date2 = request.form['datetime2']
        flagged = False
        if request.form['flagged'] == "flagged_only":
            flagged = True

        dictionary = {}
        if location: dictionary['location_name'] = str(location)
        if city: dictionary['City'] = str(city)
        if state: dictionary['State'] = str(state)
        if zipcode: dictionary['zip_code'] = str(zipcode)
        if date1: dictionary['min_date'] = str(date1)
        if date2: dictionary['max_date'] = str(date2)
        if flagged: dictionary['flagged'] = int(flagged)
        
        data_points = db.retrieveFilteredDataPoints(dictionary)

        global poiLocation
        poilocation = location
        return render_template('search-data-point.html', locations=db.retrievePOILocations(), datatype = db.retrieveDataTypes(), cities = db.retrieveCities(), states = db.retrieveStates(), data_points= data_points)
        #if not db.existsCityState(city, state): return flask.render_template('add_new_poi_location.html', cities=db.retrieveCities(), states=db.retrieveStates(), error="Invalid City State Combination")

@app.route('/add-new-poi-location', methods=['GET', 'POST'])
def add_new_poi_location():
    if permissions_enabled and not user: return flask.redirect('login')
    if permissions_enabled and user.user_type != 1: return flask.render_template('unauthorized.html')
    if flask.request.method == 'GET':
        return flask.render_template('add_new_poi_location.html', cities=db.retrieveCities(), states=db.retrieveStates())
    elif flask.request.method == 'POST':
        locationName = request.form['location_name']
        city = request.form['city'].replace('+', ' ')
        state = request.form['state'].replace('+', ' ')
        zipCode = request.form['zip_code']
        if not locationName or not zipCode: return flask.render_template('add_new_poi_location.html', cities=db.retrieveCities(), states=db.retrieveStates(), error="Empty Fields not Allowed")
        if not db.existsCityState(city, state): return flask.render_template('add_new_poi_location.html', cities=db.retrieveCities(), states=db.retrieveStates(), error="Invalid City State Combination")
        success = db.addNewPOILocation(locationName, city, state, zipCode)
        if not success: return flask.render_template('add_new_poi_location.html', cities=db.retrieveCities(), states=db.retrieveStates(), error="Failed to Add POI Location")
        return flask.redirect('/cityScientist')

@app.route('/add-new-data-point', methods=['GET', 'POST'])
def add_new_data_point():
    if permissions_enabled and not user: return flask.redirect('login')
    if permissions_enabled and user.user_type != 1: return flask.render_template('unauthorized.html')
    if flask.request.method == 'GET':
        return flask.render_template('add_new_data_point.html', locations=db.retrievePOILocations(), data_types=db.retrieveDataTypes())
    elif flask.request.method == 'POST':
        poiLocation = request.form['poi_location'].replace('+', ' ')
        date_time = request.form['datetime'].replace('T', ' ')
        dataType = request.form['data_type'].replace('+', ' ')
        value = request.form['value']
        if not date_time or not value: return flask.render_template('add_new_data_point.html', locations=db.retrievePOILocations(), data_types=db.retrieveDataTypes(), error="Empty Fields not Allowed")
        if datetime.now() < datetime.strptime(str(date_time), '%Y-%m-%d %H:%M'): 
            return flask.render_template('add_new_data_point.html', locations=db.retrievePOILocations(), data_types=db.retrieveDataTypes(), error="Date/Time Cannot be in the Future")
        success = db.addNewDataPoint(poiLocation, date_time, dataType, value)
        if not success: return flask.render_template('add_new_data_point.html', locations=db.retrievePOILocations(), data_types=db.retrieveDataTypes(), error="Failed to Add Data Point")
        return flask.redirect('/cityScientist')

@app.route('/manage-data-points')
def manage_data_points():
    data_points = db.retrieveDataPoints()
    return render_template('manage_data_points.html', datapoints=data_points)

@app.route('/change-data-point-filter', methods=['POST'])
def change_data_point_filter():
    db.data_point_filter = [str(x) for x in request.form['filter'].split("_")]
    return flask.redirect('/manage-data-points')

@app.route('/change-poi-report-filter', methods=['POST'])
def change_poi_report_filter():
    db.poi_report_filter = [str(x) for x in request.form['filter'].split("_")]
    return flask.redirect('/poi-report')

@app.route('/accept-data-points', methods=['POST'])
def accept_data_points():
    items = db.retrieveDataPoints()
    selected = [int(x) for x in request.form.getlist("selected")]
    for index in selected:
        db.acceptDataPoint(items[index][0], items[index][3])
    return flask.redirect('/manage-data-points')

@app.route('/reject-data-points', methods=['POST'])
def reject_data_points():
    items = db.retrieveDataPoints()
    selected = [int(x) for x in request.form.getlist("selected")]
    for index in selected:
        db.rejectDataPoint(items[index][0], items[index][3])
    return flask.redirect('/manage-data-points')

@app.route('/manage-city-officials')
def manage_city_officials():
    city_officials = db.retrieveCityOfficials()
    return render_template('manage_city_officials.html', cityofficials=city_officials)

@app.route('/accept-city-officials', methods=['POST'])
def accept_city_officials():
    items = db.retrieveCityOfficials()
    selected = [int(x) for x in request.form.getlist("selected")]
    for index in selected:
        db.acceptCityOfficial(items[index][0])
    return flask.redirect('/manage-city-officials')

@app.route('/reject-city-officials', methods=['POST'])
def reject_city_officials():
    items = db.retrieveCityOfficials()
    selected = [int(x) for x in request.form.getlist("selected")]
    for index in selected:
        db.rejectCityOfficial(items[index][0])
    return flask.redirect('/manage-city-officials')

@app.route('/poi-report')
def poi_report():
    return flask.render_template('poi_report.html', rows=db.retrievePOIReportRows())



# -------------------- run app --------------------

if __name__ == '__main__': 
    db.setUp()
    app.run()

