import jwt
import datetime
from flask_login import UserMixin
from marshmallow_jsonapi import Schema, fields
from marshmallow import validate
from werkzeug.security import generate_password_hash, check_password_hash

from bucketlist import db, login_manager


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
    bucketlists = db.relationship('Bucketlist', backref=db.backref(
        'bucketlists', uselist=True, cascade='delete,all'))

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

    #method to encode token
    def encode_auth_token(self, user_id):
        try:
            payload = {
            'exp':datetime.datetime.utcnow()+datetime.timedelta(days=0, seconds=5),
            'iat':datetime.datetime.utcnow(),
            'sub':user_id
            }
            return jwt.encode(payload, app.config.get('SECRET_KEY'), algorithm='HS256')
        except(Exception):
            return Exception

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklisted_token(auth_token)
            if is_blacklisted_token:
                return 'Token is blacklisted. Please log in again.'
            else:
                return payload['sub']
        except(jwt.ExpiredSignatureError):
            return "Signature expired. Please log in again."
        except(jwt.InvalidTokenError):
            return "Invalid token. Please log in again."


class UserSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")
    id = fields.Integer(dump_only=True)
    email = fields.String(validate=not_blank)
    username = fields.String(validate=not_blank)
    first_name = fields.String()
    last_name = fields.String()
    password_hash = fields.String(validate=not_blank)
    is_admin = fields.Boolean()
    bucketlists = fields.Relationship()

    def get_top_level_links(self, data, many):
        if many:
            self_link = "/users/"
        else:
            self_link = "/users/{}".format(data['id'])
        return {'self': self_link}
    class Meta:
        type_= 'users'

#model for blacklist tokens 
class BlacklistToken(db.Model):
    __tablename__ = 'blacklist_tokens'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.utcnow()

    @staticmethod
    def check_blacklisted_token(auth_token):
        response = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if response:
            return True
        else:
            return False

    def __repr__(self):
        return '<id: token: {0}'.format(self.token)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Bucketlist(db.Model):
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    date_modified = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', backref=db.backref('items', uselist=True, cascade='delete,all'))

    def __repr__(self):
        return '<Bucketlist: {}>' .format(self.name)


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