import flask
import flask_login

# -------------------- define app --------------------

app = flask.Flask(__name__)
user = None

class User:
    def __init__(self, username, user_type):
        self.username = username
        self.user_type = user_type

#db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")
#cursor = db.cursor()

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
        #attemptedUser = flask.request.form['username']
        #attemptedPass = flask.request.form['password']
        #cursor.execute("SELECT COUNT(1) FROM users WHERE name = %s", attemptedUser)

        #TODO ensure user in database and create appropriate instance of user
        user = User('dummy_username', 'admin')
        return flask.redirect('index')

@app.route('/registration')
def registration():
		return flask.render_template('registration.html')


# -------------------- run app --------------------

if __name__ == '__main__': app.run()

