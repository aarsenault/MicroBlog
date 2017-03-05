

from flask import Flask, render_template, request, session

from src.common.database import Database
from src.models.blog import Blog
from src.models.user import User
# from flask_debugtoolbar import DebugToolbarExtension

#toolbar = DebugToolbarExtension(app)

app = Flask(__name__)
app.secret_key = 'test'
app.debug = True

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

    # Need to check if already registered

    return render_template("profile.html", email=session['email'])


@app.route('/auth/create_new_blog', methods=['POST'])
def display_create_new_blog():

    return render_template("create_new_blog.html")

# registers new blog
@app.route('/auth/new_blog', methods=['POST'])
def register_blog():

    # don't actually use the author rn.
    # author = request.form['author']

    title = request.form['blog_name']
    description = request.form['description']

    # get the user
    user = User.get_by_email(session['email'])

    # enter into database
    new_blog = user.new_blog(title=title, description=description)
    new_blog.save_to_mongo()

    return render_template("profile.html", email=session['email'])

@app.route('/blogs/<string:user_id>')
@app.route('/blogs')
def user_blogs(user_id=None):
    # takes the string after blogs - gets the user_id

    # Finds the user depending on route
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        print("Trying to get user by email")
        print("email is {}".format(session['email']))
        user = User.get_by_email(session['email'])

    # get's the user's blogs, stores in blogs
    blogs = user.get_blogs()

    # renders the template while passing the blogs
    return render_template("user_blogs.html", blogs=blogs, email=user.email)


@app.route('/posts/<string:blog_id>')
def blog_posts(blog_id):

    blog = Blog.from_mongo(blog_id)

    posts = blog.get_posts()

    return render_template('posts.html', posts=posts, blog_title=blog.title)


# this is the one I made
@app.route('/profile')
def check_profile():

    if session['email'] is not None:
        return render_template('profile.html', email=session['email'])
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)