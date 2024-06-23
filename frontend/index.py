#!venv/bin/python3
"""Routes module for the Flask app"""

from flask import render_template, flash, redirect, url_for
from frontend import app
# from app.forms import LoginForm

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
