import os
import datetime

import jwt
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bucketlist import db


class User(UserMixin, db.Model):
    '''
    creates users table.
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    bucketlists = db.relationship(
        'Bucketlist', cascade="save-update, merge, delete")

    def __init__(self, email, username, first_name, last_name, password, is_admin=False):
        self.email = email
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin
        self.bucketlists = []

    @property
    def password(self):
        return "You cannot read the password."

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User:{}>'.format(self.username)

    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def update(self, resource):
        db.session.add(resource)
        return db.session.commit()

    def delete(self, resource):
        db.session.delete(resource)
        db.session.commit()

    # method to encode token
    def encode_auth_token(self, user_id):
        try:
            payload = {
                'exp': datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(payload, os.getenv('SECRET_KEY'), algorithm='HS256')
        except(Exception):
            return Exception

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, os.getenv('SECRET_KEY'))
            return payload['sub']
        except(jwt.ExpiredSignatureError):
            return "Signature expired. Please log in again."
        except(jwt.InvalidTokenError):
            return "Invalid token. Please log in again."


class Bucketlist(db.Model):
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', cascade="save-update, merge, delete")

    def __repr__(self):
        return '<Bucketlist: {}>' .format(self.name)

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by
        self.date_created = datetime.datetime.utcnow()
        self.date_modified = datetime.datetime.utcnow()


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __repr__(self):
        return '<Item: {}>' .format(self.name)

    def __init__(self, name, bucketlist_id):
        self.name = name
        self.date_created = datetime.datetime.utcnow()
        self.date_modified = datetime.datetime.utcnow()
        self.done = False
        self.bucketlist_id = bucketlist_id
