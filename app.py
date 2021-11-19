import os
from flask import (
    Flask, render_template, flash, redirect,
    url_for, session, request, logging)
# from flask_pymongo import PyMongo
from data import Articles
from wtforms import (
    Form, StringField, TextAreaField, PasswordField, validators)
from passlib.hash import sha256_crypt
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

# MongoDB Connection Config

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

        return render_template('register.html')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
