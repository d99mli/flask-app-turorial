import os
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
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        # name = form.name.mongo
        # email =
        return render_template('register.html')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
