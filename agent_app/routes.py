#!venv/bin/python3
"""Index module for the Flask app"""

from flask import render_template, flash
from flask import redirect, url_for, request
from urllib.parse import urlsplit
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
import sqlalchemy as sa
from agent_app import app, db
from models.forms import LoginForm, EditProfileForm
from models.user import User
from models.agent import Agent

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
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if (form.user_type.data == 'User'):
        if form.validate_on_submit():
            user = db.session.scalar(
                sa.select(User).where(User.username == form.username.data))
            if user is None or not user.check_password(form.password.data):
                flash('Invalid username or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))
    else:
        if form.validate_on_submit():
            user = db.session.scalar(
                sa.select(Agent).where(Agent.username == form.username.data))
            if user is None or not user.check_password(form.password.data):
                flash('Invalid agentname or password')
                return redirect(url_for('login'))
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))   
 
    return render_template('login.html', title='Sign In', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)
