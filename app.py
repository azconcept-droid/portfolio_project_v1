#!venv/bin/python3
""" Agent app application entry point """
from agent_app import app, db
import sqlalchemy as sa
import sqlalchemy.orm as so
from models.agent import Agent, Post
from models.user import User

@app.shell_context_processor
def make_shell_context():
    """ make shell context """
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Agent': Agent, 'Post': Post}
