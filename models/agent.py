#!venv/bin/python3
""" Agent model module """

from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from agent_app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Agent(db.Model):
    """ Agent class for Agent table """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)

    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)

    license: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable=True)

    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')


    def __repr__(self):
        return '<Agent {}>'.format(self.username)
    
    def set_password(self, password):
        """ Set user password hashed """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """ Validate password """
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    """ Post class db model"""
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    agent_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(Agent.id),
                                               index=True)

    author: so.Mapped[Agent] = so.relationship(back_populates='posts')

    def __repr__(self):
        return '<Post {}>'.format(self.body)
