# Author: Floreint-Eduard Decu
# Date: July 2020

import datetime
from api import db

# api is the app module
# db is the SQLAlchemy (ORM DATABASE) instantiated in __init__.py

#  Association tables
# Relationship between a user and its followers 
following = db.Table('followers',
            db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
            db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
# Relationship between a post and the users who liked a post
post_likes = db.Table('postlikes',
            db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
            db.Column('post_id', db.Integer, db.ForeignKey('post.id'))

)

class User(db.Model):

    #Table content 
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(50), nullable= False)
    created = db.Column(db.DateTime, nullable=False, default= datetime.datetime.utcnow())
    posts = db.relationship('Post', backref='author', lazy=True)

    # Relationship between a user and its followers
    # This table is self referencing (many to many relationship with User table)
    followed_by = db.relationship('User', secondary=following, 
                                primaryjoin=id == following.c.followed_id,
                                secondaryjoin=id ==following.c.follower_id,
                                backref=db.backref('following', lazy='dynamic'))


class Post(db.Model):

    # Table content 
    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String(100), nullable=False)
    image_file = db.Column(db.String(30), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False, default= datetime.datetime.utcnow())

    # Relationship with the user who create the post (one-to-many with User table)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship with the users who liked the post created by another user 
    # The author can like his own post as well
    likes = db.relationship('User', secondary=post_likes, )

