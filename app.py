import os
from datetime import datetime
from functools import wraps
from flask import (
    Flask, render_template, flash, redirect,
    url_for, session, request, logging)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from passlib.hash import sha256_crypt
from wtforms import (
    Form, StringField, TextAreaField, PasswordField, validators)
from data import Articles
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# MongoDB Connection Config
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)

Articles = Articles()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/articles')
def articles():
    return render_template('articles.html', articles=Articles)


@app.route('/article/<page_id>')
def article(page_id):
    return render_template('article.html', id=page_id)


@app.route("/get_users")
def get_users():
    users = mongo.db.users.find()
    return render_template('users.html', users=users)


class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(
        min=4, max=25, message="Username must be between 4 and 25 characters.")
    ])
    email = StringField('Email', [
        validators.Length(min=6, max=35),
        validators.Regexp(
            '^[a-zA-Z0-9.!#$%&*+/=?_~-]+@[a-zA-Z0-9-]+(?:\\.[a-zA-Z0-9-]+)*$',
            message="Must be a valid e-mail")
    ])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get('username').lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        registration = {
            "name": request.form.get("name").lower(),
            "email": request.form.get("email").lower(),
            "username": request.form.get("username").lower(),
            "password": sha256_crypt.hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(registration)

        # put the new user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration successful!", 'success')

        return redirect(url_for('login'))

    return render_template('register.html', form=form)


# User Log in
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        # Check if user exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # Ensure hashed password matches user input
            if sha256_crypt.verify(
                request.form.get("password"), existing_user["password"]):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(
                    request.form.get("username")), 'success')
                return redirect(url_for('dashboard'))
            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # Username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template('login.html', form=form)


# Check if user logged in (function decorator)
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'user' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please login!', 'danger')
            return redirect(url_for('login'))
    return wrap


# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


# Dashboard, for logged in users
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')


# Article form class
class ArticleForm(Form):
    title = StringField('Title', [validators.Length(min=1, max=100)])
    body = TextAreaField('Body',
        [validators.Length(min=10)], render_kw={'rows': 20})


# Add article (to db)
@app.route('/add_article', methods=['GET', 'POST'])
@is_logged_in
def add_article():
    form = ArticleForm(request.form)
    if request.method == 'POST' and form.validate():

        one_article = {
            "title": request.form.get("title").lower(),
            "body": request.form.get("body").lower(),
            "author": session["user"],
            "create_date": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

        mongo.db.articles.insert_one(one_article)
        flash('Article Created!', 'success')
        return redirect(url_for('dashboard'))

    return render_template('add_article.html', form=form)


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
