import re
from flask import request, jsonify, make_response
from flask_restful import Resource, Api, reqparse
from sqlalchemy.exc import SQLAlchemyError

from .import auth
from ..models import User, BlacklistToken
from ..serializer import UserSchema
from .. import db

schema = UserSchema(strict=True)
api = Api(auth)
# custom error messages
exception_error_response = {
    'status': 'failed',
    'message': Exception
}
sqlalchemy_error_response = {
    'error': SQLAlchemyError,
    'message': 'Database error. try again.'
}
wrong_method_error = {'message': 'User registration is a post method.'}


class UserRegistration(Resource):
    '''
    API endpoint for user registration.
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=Email,
                            required=True, help='email is required')
        parser.add_argument('username', required=True,
                            help='Username is required')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('password')
        user_data = parser.parse_args(strict=True)
        if user_data:
            # check that email is entered correctly.
            if not re.match(r"[^@]+@[^@]+\.[^@]+", user_data['email']):
                response = {'message': 'invalid email. Please try again'}
                return make_response(jsonify(response))
            # password has to be more than 8 characters.
            if len(user_data['password']) < 8:
                response = {'message': 'Password too short. Please try again'}
                return make_response(jsonify(response))
                # check that username is unique
            user_usrname = user = User.query.filter_by(
                username=user_data['username']).first()
            if user_usrname:
                response = {
                    'message': 'Username already exists. Please try again'}
                return make_response(jsonify(response))
            user = User.query.filter_by(email=user_data['email']).first()
            # check that username does not exist too
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
                        'status': 'success',
                        'message': 'Successfully registered'
                    }

                    response = jsonify(response)
                    response.status_code = 201
                    return make_response(response)
                except(Exception):
                    response = jsonify(exception_error_response)
                    response.status_code = 400
                    return make_response(response)
                except(SQLAlchemyError):
                    db.session.rollback()
                    response = jsonify(sqlalchemy_error_response)
                    response.status_code = 400
                    return make_response(response)
            else:
                response = {
                    'status': 'fail',
                    'message': 'User exists. please log in.'
                }
                response = jsonify(response)
                response.status_code = 400
                return make_response(response)
        else:
            response = {
                'status': 'fail',
                'message': 'Please input details.'
            }
            return make_response(jsonify(response))

    def get(self):
        return make_response(jsonify(wrong_method_error))

    def put(self):
        return make_response(jsonify(wrong_method_error))

    def delete(self):
        return make_response(jsonify(wrong_method_error))


class UserLogin(Resource):
    '''
    API endpoint for user login
    '''

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("email", "Please enter your Email to login")
        parser.add_argument("password", "Please enter your password")
        user_details = parser.parse_args(strict=True)
        if user_details:
            try:
                user = User.query.filter_by(
                    email=user_details['email']).first()
                if user and user.verify_password(user_details['password']):
                    auth_token = user.encode_auth_token(user.id)
                    if auth_token:
                        response = {'status': 'success',
                                    'message': 'Successfully logged in.',
                                    'auth_token': auth_token.decode()}
                        response = jsonify(response)
                        response.status_code = 200
                        return make_response(response)
                else:
                    response = {'status': 'fail',
                                'message': 'User does not exist.'}
                    response = jsonify(response)
                    response.status_code = 400
                    return make_response(response)
            except(Exception):
                response = jsonify(exception_error_response)
                response.status_code = 400
                return make_response(response)
        else:
            response = {'status': 'fail',
                        'message': 'Please input details.'}
            response = jsonify(response)
            response.status_code = 400
            return make_response(response)


class UserLogout(Resource):
    '''
    Logout endpoint. Just incase user needs to logout before their token can expire.
    '''

    def post(self):
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header
        else:
            auth_token = ''
        if auth_token:
            resp = User.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                blacklist_token = BlacklistToken(token=auth_token)
                try:
                    db.session.add(blacklist_token)
                    db.session.commit()
                    response = {'status': 'success',
                                'message': 'Successfully logged out.'
                                }
                    response = jsonify(response)
                    response.status_code = 200
                    return make_response(response)
                except(Exception):
                    response = jsonify(exception_error_response)
                    response.status_code = 400
                    return make_response(response)
            else:
                response = jsonify({'status': 'fail',
                                    'message': "user {} does not exist".format(resp)
                                    })
                response.status_code = 400
            return make_response(response)
        else:
            response = jsonify({'status': 'Success',
                                'message': 'Provide a valid auth token'
                                })
            response.status_code = 400
            return make_response(response)


api.add_resource(UserRegistration, '/auth/register')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserLogout, '/auth/logout')
