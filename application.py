import flask
import flask_login

# -------------------- define app --------------------

app = flask.Flask(__name__)

#db = MySQLdb.connect(host="localhost", user="root", passwd="", db="test")
#cursor = db.cursor()

# -------------------- routes --------------------

@app.route('/')
def home():
    return flask.render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
        #TODO ensure user in database
        if 'username' in session:
        	return flask.render_template('index.html')
        if request.method == 'POST':
        	attemptedUser = request.form['username']
        	attemptedPass = request.form['password']
        	#cursor.execute("SELECT COUNT(1) FROM users WHERE name = %s", attemptedUser)
        	return flask.redirect('/')
# -------------------- run app --------------------

@app.route('/registration')
def registration():
		return flask.render_template('registration.html')

if __name__ == '__main__': app.run()

