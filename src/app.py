

from flask import Flask, render_template, request, session

from src.common.database import Database
from src.models.user import User

app = Flask(__name__)
app.secret_key = 'test'
debug=True

# flask method that runs only once
@app.before_first_request
def initialize_database():
    Database.initialize()

# this acts as the homepage
# Route with nothing in it left
@app.route('/')
def home_template():
    return render_template('home.html')


@app.route('/login') # www.mysite.com/api/login
def login_template():

    # Flask knows that templates live in the templates folder
    return render_template('login.html')

@app.route('/register') # www.mysite.com/api/register
def register_template():

    # Flask knows that templates live in the templates folder
    return render_template('register.html')

# the methods array says will be accepted
@app.route('/auth/login', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if User.login_valid(email=email, password=password):
        User.login(user_email= email)

        # passing in extra values allows the rendered page to use also
        return render_template('profile.html', email= session['email'])

    else:
        session['email'] = None


# registers the user
@app.route('/auth/register', methods=['POST'])
def register_user():
    email = request.form['email']
    password = request.form['password']

    # method sets the session email already
    User.register(email, password)

    return render_template("profile.html", email=session['email'])

if __name__ == '__main__':
    app.run()