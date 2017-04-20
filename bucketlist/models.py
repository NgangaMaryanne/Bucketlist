from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from bucketlist import db, login_manager


class User(UserMixin, db.Model):
    '''
    creates users table.
    '''
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    bucketlists = db.relationship('Bucketlist', backref=db.backref(
        'bucketlists', uselist=True, cascade='delete,all'))

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


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Bucketlist(db.Model):
    __tablename__ = 'bucketlists'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    items = db.relationship('Item', backref=db.backref('items', uselist=True, cascade='delete,all'))

    def __repr__(self):
        return '<Bucketlist: {}>' .format(self.name)


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_created = db.Column(db.DateTime)
    date_modified = db.Column(db.DateTime)
    done = db.Column(db.Boolean, default=False)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlists.id'))

    def __repr__(self):
        return '<Item: {}>' .format(self.name)