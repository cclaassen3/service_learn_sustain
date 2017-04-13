import flask
import flask_login
import MySQLdb

# -------------------- define app --------------------

app = flask.Flask(__name__)
user = None

class User:
    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type

db = MySQLdb.connect(host="academic-mysql.cc.gatech.edu", user="cs4400_Group_20", passwd="3lZwg9Kk", db="cs4400_Group_20")
cursor = db.cursor()

# -------------------- routes --------------------

@app.route('/')
def home():
    return flask.redirect('login')

@app.route('/index')
def index():
    if not user: return flask.redirect('login')
    return flask.render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():

    global user
    if user:
    #if 'username' in session:
        return flask.redirect('/index')

    elif flask.request.method == 'GET':
        return flask.render_template('login.html')

    elif flask.request.method == "POST":
        attemptedUser = flask.request.form['username']
        attemptedPass = flask.request.form['password']
        try:
            cursor.execute("SELECT COUNT(1) FROM users WHERE name = %s", attemptedUser)
        except: 
            print("Not in db")
        #TODO ensure user in database and create appropriate instance of user
        user = User('dummy_username', 'omnipotent')
        return flask.redirect('index')

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if flask.request.method == 'GET':
        return flask.render_template('registration.html')
        insertedUser = flask.request.form['username']
        insertedPass = flask.request.form['password']
        insertedEmail = flask.request.form['email']
        cursor.execute("INSERT INTO user(username, password, email) VALUES(insertedUser, insertedPass, insertedEmail")
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

