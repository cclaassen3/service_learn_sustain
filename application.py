import flask
import flask_login

#define app
app = flask.Flask(__name__)

#set up login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

#mock database TODO retrieve dynamically from DB
users = {'carina': {'pw': 'pw'}}

#user class definition
class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['pw'] == users[email]['pw']

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if flask.request.method == 'GET':
        return '''
               <div class="login-page">
                  <div class="form">
                    <form class="register-form">
                      <input type="text" placeholder="name"/>
                      <input type="password" placeholder="password"/>
                      <input type="text" placeholder="email address"/>
                      <button>create</button>
                      <p class="message">Already registered? <a href="#">Sign In</a></p>
                    </form>
                    <form class="login-form">
                      <input type="text" placeholder="username"/>
                      <input type="password" placeholder="password"/>
                      <button>login</button>
                      <p class="message">Not registered? <a href="#">Create an account</a></p>
                    </form>
                  </div>
                </div>
               '''

    email = flask.request.form['email']
    if flask.request.form['pw'] == users[email]['pw']:
        user = User()
        user.id = email
        flask_login.login_user(user)
        return "logged in!"
        #return flask.redirect(flask.url_for('protected'))

    return 'Bad login'

@app.route('/testing', methods=['GET', 'POST'])
def testing():
    return flask.render_template('login.html')

# @app.route('/protected')
# @flask_login.login_required
# def protected():
#     return 'Logged in as: ' + flask_login.current_user.id

# @app.route('/logout')
# def logout():
#     flask_login.logout_user()
#     return 'Logged out'

# @login_manager.unauthorized_handler
# def unauthorized_handler():
#     return 'Unauthorized'

@app.route('/')
def home():
    return "Hello world :)"


if __name__ == '__main__': app.run()

