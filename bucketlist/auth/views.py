from flask import Flask, request, jsonify, make_response, g
from flask_restful import Resource, Api, reqparse
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import json
import os
import re

from .import auth
from ..models import User
from ..serializer import UserSchema
from .. import db

schema = UserSchema(strict=True)
api = Api(auth)

class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='email is required')
        parser.add_argument('username', required=True, help='Username is required')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('password')
        user_data = parser.parse_args(strict=True)
        if user_data:
            #check that email is entered correctly.
            if not re.match(r"[^@]+@[^@]+\.[^@]+", user_data['email']):
                response = {'message':'invalid email. Please try again'}
                return make_response(jsonify(response))
            #password has to be more than 8 characters.    
            if len(user_data['password'])<8:
                response = {'message':'Password too short. Please try again'}
                return make_response(jsonify(response))
                #check that username is unique
            user_usrname = user = User.query.filter_by(username=user_data['username']).first()
            if user_usrname:
                response = {'message':'Username already exists. Please try again'}
                return make_response(jsonify(response))
            user = User.query.filter_by(email=user_data['email']).first()
            #check that username does not exist too
            if not user:
                try:
                    user = User(
                        email=user_data['email'],
                        username=user_data['username'],
                        first_name=user_data['first_name'],
                        last_name=user_data['last_name'],
                        password=user_data['password'] 
                    )
                    db.session.add(user)
                    db.session.commit()
                    response = {
                        'status':'success',
                        'message':'Successfully registered'
                    }
                    return make_response(jsonify(response))
                except(Exception):
                    response = {
                        'status':'failed',
                        'message':Exception
                    }
                    return make_response(jsonify(response))
                except(SQLAlchemyError):
                    db.session.rollback()
                    response={
                        'error':SQLAlchemyError,
                        'message':'Database error. try again.'
                    }
                    return make_response(jsonify(response))
            else:
                response = {
                    'status':'fail',
                    'message':'User exists. please log in.'
                }
                return make_response(jsonify(response))
        else:
            response = {
                'status':'fail',
                'message':'Please input details.'
            }
            return make_response(jsonify(response))

    def get(self):
        response = {'message':'User registration is a post method.'}
        return make_response(jsonify(response))
    def put(self):
        response = {'message':'User registration is a post method.'}
        return make_response(jsonify(response))
    def delete(self):
        response = {'message':'User registration is a post method.'}
        return make_response(jsonify(response))

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", "Please enter your Email to login")
        parser.add_argument("password", "Please enter your password")
        user_details = parser.parse_args(strict=True)
        if user_details:
            try:
                user=User.query.filter_by(email=user_details['email']).first()
                # auth_token = user.encode_auth_token(user.id)
                if user and user.verify_password(user_details['password']):
                    auth_token = user.encode_auth_token(user.id)
                    if auth_token:
                        #set global
                        response = {'status':'success',
                                    'message':'Successfully logged in.',
                                    'auth_token':auth_token.decode()}
                        return make_response(jsonify(response))
                else:
                    response={'status':'fail',
                              'message':'User does not exist.'}
                    return make_response(jsonify(response))
            except(Exception):
                response = {'status':'fail',
                            'message':'Login failed please try again.',
                            'error':str(Exception)}
                return make_response(jsonify(response))
        else:
            response = {'status':'fail',
                        'message':'Please input details.'}
        #add edge cases for wrong email or wrong password.

class UserStatus(Resource):
    def get(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                user = User.query.filter_by(id=resp).first()
                response = {'status':'success',
                            'data':{'id':user.id,
                                     'email':user.email,
                                     'is_admin':user.is_admin
                                }
                            }
                return make_response(jsonify(response))
            response = {'status':'fail',
                        'message':resp
                        }
        else:
            response={'status':'fail',
                        'message':'provide valid token'
                    }
            return make_response(jsonify(response))

class UserLogout(Resource):
    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    db.session.add(blacklist_token)
                    db.session.commit()
                    response = {'status':'success',
                                'message':'Successfully logged out.'
                        }
                    return make_response(jsonify(response))
                except(Exception):
                    response = {'status':'Fail',
                                'message':Exception
                                }
                    return make_response(jsonify(response))
            response = {'status':'fail',
                        'message':resp
                        }
            return make_response(jsonify(response))
        else:
            response = {'status':'Success',
                        'message':'Provide a valid auth token'
                        }
            return make_response(jsonify(response))

api.add_resource(UserRegistration, '/auth/register')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserStatus, '/auth/status')
api.add_resource(UserLogout,'/auth/logout')