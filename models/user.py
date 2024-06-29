#!venv/bin/python3
""" User module """

from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from agent_app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    """ User class db model """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        """ Print the user object """
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        """ Set user password hashed """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """ Validate password """
        return check_password_hash(self.password_hash, password)
