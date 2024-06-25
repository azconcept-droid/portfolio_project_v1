#!venv/bin/python3
"""Index module for the Flask app"""

from flask import render_template, flash, redirect, url_for
from frontend import app
from models.forms import LoginForm


@app.route('/')
@app.route('/index')
def index():
    """Default route, home page"""

    # Mockup for users
    agent = {'agentname': 'Azeez'}

    # Mockup for posts
    posts = [
        {
            'author': {'agentname': 'James'},
            'property': 'House',
            'image': 'image_url',
            'video': 'short video shut',
            'Location': 'Idimu, Lagos',
            'address': '100, kdckscscje, djncjie'
        },
        {
            'author': {'agentname': 'Ajoke'},
            'property': 'Land',
            'image': 'image_url',
            'video': 'short video shut',
            'Location': 'Iwo road, Ibadan',
            'address': "45, jhjksdhcei, jdkdjios"
        },
        {
            'author': {'agentname': 'Usama'},
            'property': '2 Bedroom flat',
            'image': 'image_url',
            'video': 'short video shut',
            'Location': 'Sango, Ogun state',
            'address': '3 ahjlkdldsk street, bklsjcdlksj'
        }
    ]

    return render_template('index.html', title='Home', agent=agent, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login method """
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
