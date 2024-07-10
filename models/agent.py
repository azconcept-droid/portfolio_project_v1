#!venv/bin/python3
""" Agent model module """

from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from agent_app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


followers = sa.Table(
    'followers',
    db.metadata,
    sa.Column('follower_id', sa.Integer, sa.ForeignKey('agent.id'),
              primary_key=True),
    sa.Column('followed_id', sa.Integer, sa.ForeignKey('agent.id'),
              primary_key=True)
)


class Agent(UserMixin, db.Model):
    """ Agent class for Agent table """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)

    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)

    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)

    license: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256), nullable=True)

    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
    
    about_me: so.Mapped[Optional[str]] = so.mapped_column(sa.String(140))
    
    last_seen: so.Mapped[Optional[datetime]] = so.mapped_column(
        default=lambda: datetime.now(timezone.utc))
    
    following: so.WriteOnlyMapped['Agent'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')

    followers: so.WriteOnlyMapped['Agent'] = so.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')


    def __repr__(self):
        return '<Agent {}>'.format(self.username)
    
    def set_password(self, password):
        """ Set user password hashed """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """ Validate password """
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    def follow(self, agent):
        if not self.is_following(agent):
            self.following.add(agent)

    def unfollow(self, agent):
        if self.is_following(agent):
            self.following.remove(agent)

    def is_following(self, agent):
        query = self.following.select().where(Agent.id == agent.id)
        return db.session.scalar(query) is not None

    def followers_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)

    def following_count(self):
        query = sa.select(sa.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)
    
    def following_posts(self):
        Author = so.aliased(Agent)
        Follower = so.aliased(Agent)
        return (
            sa.select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower), isouter=True)
            .where(sa.or_(
                Follower.id == self.id,
                Author.id == self.id,
            ))
            .group_by(Post)
            .order_by(Post.timestamp.desc())
        )


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


@login.user_loader
def load_user(id):
    return db.session.get(Agent, int(id))
