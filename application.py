import flask
import flask_login

# -------------------- define app --------------------

app = flask.Flask(__name__)



# -------------------- routes --------------------

@app.route('/')
def home():
    return flask.redirect('login')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return flask.render_template('login.html')
    elif flask.request.method == "POST":
        #TODO ensure user in database
        return flask.redirect('index')

@app.route('/index')
def index():
    return flask.render_template('index.html')




# -------------------- run app --------------------

if __name__ == '__main__': app.run()

