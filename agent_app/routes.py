#!venv/bin/python3
"""Index module for the Flask app"""

from flask import render_template, flash
from flask import redirect, url_for, request
from urllib.parse import urlsplit
from flask_login import current_user, login_user, logout_user
from flask_login import login_required
import sqlalchemy as sa
from agent_app import app, db
from models.forms import LoginForm, EditProfileForm, RegistrationForm
from models.forms import PostForm, EmptyForm
from models.user import User
from models.agent import Agent, Post
from datetime import datetime, timezone


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    """Default route, home page"""

    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))

    # Mockup for users
    # agent = {'agentname': 'Azeez'}

    # Mockup for posts
    # posts = [
    #     {
    #         'author': {'agentname': 'James'},
    #         'body': 'Awesome house',
    #         'property': 'House',
    #         'image': 'image_url',
    #         'video': 'short video shut',
    #         'Location': 'Idimu, Lagos',
    #         'address': '100, kdckscscje, djncjie'
    #     },
    #     {
    #         'author': {'agentname': 'Ajoke'},
    #         'body': 'Big land in a good location',
    #         'property': 'Land',
    #         'image': 'image_url',
    #         'video': 'short video shut',
    #         'Location': 'Iwo road, Ibadan',
    #         'address': "45, jhjksdhcei, jdkdjios"
    #     },
    #     {
    #         'author': {'agentname': 'Usama'},
    #         'body': 'Beautiful flat',
    #         'property': '2 Bedroom flat',
    #         'image': 'image_url',
    #         'video': 'short video shut',
    #         'Location': 'Sango, Ogun state',
    #         'address': '3 ahjlkdldsk street, bklsjcdlksj'
    #     }
    # ]
    # posts = [
    #     {
    #         'author': {'username': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]

    posts = db.session.scalars(current_user.following_posts()).all()
    return render_template('index.html', title='Home', form=form, posts=posts)
    # return render_template('index.html', title='Home', agent=agent, posts=posts)


@app.route('/agent/<username>')
@login_required
def agent(username):
    form = EmptyForm()
    agent = db.first_or_404(sa.select(Agent).where(Agent.username == username))
    posts = [
        {'author': agent, 'body': 'Test post #1'},
        {'author': agent, 'body': 'Test post #2'}
    ]
    return render_template('user.html', agent=agent, posts=posts, form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login function """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    user = object
    user_type = form.user_type.data
    print(user_type)
    print(user_type == "customer" or user_type == "Customer")
    next_page = ""
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(Agent).where(Agent.username == form.username.data))
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        try:
            next_page = request.args.get('next')[1:]
        except TypeError:
            next_page = url_for('index')
        print(next_page)
        if next_page is None or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(url_for(next_page))

    return render_template('login.html', title='Login', form=form)


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()


@app.route('/logout')
def logout():
    """ Logout function """
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    user = object

    if form.validate_on_submit():
        user = Agent(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered agent!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """ Edit profile function """
    form = EditProfileForm(current_user.username)
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


@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(Agent).where(Agent.username == username))
        if user is None:
            flash(f'Agent {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('agent', username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f'You are following {username}!')
        return redirect(url_for('agent', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(Agent).where(Agent.username == username))
        if user is None:
            flash(f'User {username} not found.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('agent', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'You are not following {username}.')
        return redirect(url_for('agent', username=username))
    else:
        return redirect(url_for('index'))


@app.route('/explore')
@login_required
def explore():
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.session.scalars(query).all()
    return render_template('index.html', title='Explore', posts=posts)
