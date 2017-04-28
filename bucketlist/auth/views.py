from flask import Flask, request, jsonify, make_response
from flask_restful import Resource, Api, reqparse
from sqlalchemy.exc import SQLAlchemyError
from marshmallow import ValidationError
import json

from .import auth
from ..models import User, UserSchema
from .. import db

schema = UserSchema(strict=True)
api = Api(auth)
class UserRegistration(Resource):
    def post(self):
        user_data = request.get_json()
        #check that user does not exist
        user = User.query.filter_by(email=user_data['email']).first()
        #check that username does not exist too
        if not user:
            try:
                user = User(email=user_data['email'], username=user_data['username'], first_name=user_data['first_name'],
                            last_name=user_data['last_name'],password=user_data['password'] )
                user.add(user)
                auth_token = user.encode_auth_token(user.id)
                response = {'status':'success',
                            'message':'Successfully registered',
                            'auth_token':auth_token.decode()
                            }
                return make_response(jsonify(response)), 201
            except(Exception):
                response = {'status':'failed',
                            'message':'Please try again'
                            }
                return make_response(jsonify(response)), 400
            except(SQLAlchemyError):
                db.session.rollback()
                response={'error':SQLAlchemyError,
                          'message':'Database error. try again.'
                }
                return make_response(jsonify(response)), 400
        else:
            response = {'status':'fail',
                        'message':'User exists. please log in.'
                        }
            return make_response(jsonify(response))




'''
    def get(self):
        users_query = User.query.all()
        results = schema.dump(users_query, many=True).data
        return results

    def post(self):
    
        #Add a new user.
    
        # register=request.data

        raw_dict = request.get_json(force=True)
        

        try:
            # schema.validate(raw_dict)
            # ['data']['attributes']
            request_dict = raw_dict
            print(raw_dict)
            user = User(email=request_dict['email'], username=request_dict['username'], first_name=request_dict['first_name'], 
                        last_name=request_dict['last_name'], password=request_dict['password'])
            user.add(user)
            query= User.query.get(user.id)
            results = schema.dump(query).data
            return results, 201
        except(ValidationError):
            resp = jsonify({"error":ValidationError})
            resp.status_code = 403
            return resp
        except(SQLAlchemyError):
            db.session.rollback()
            resp = jsonify({"error":str(SQLAlchemyError)})
            resp.status_code = 403
            return resp
'''
class GetUpdateDeleteUser(Resource):
    def get(self, id):
        user = User.query.get_or_404(self, id)
        result = schema.dump(user).data
        return result

    def patch(self, id):
        user = User.query.get_or_404(id)
        changed_data = request.get_json(force=True)
        try:
            for key, value in changed_data.items():
                setattr(user, key, value)
            user.update()
            return self.get(id)
        except(ValidationError):
            resp = jsonify({"error":ValidationError})
            resp.status_code = HTTP_401_BadRequest
            return resp
        except(SQLAlchemyError):
            resp = jsonify({"Error":str(SQLAlchemyError)})
            resp.status_code = HTTP_401_BadRequest
            return resp

    def delete(self, id):
        user = User.query.get_or_404(id)
        try:
            user.delete(user)
            response = make_response()
            response.status_code=204
        except(SQLAlchemyError):
            db.session.rollback()
            resp.status_code = 204
            return resp



class UserLogin(Resource):
    def post(self):
        user_details = request.get_json()
        try:
            user=User.query.filter_by(email=user_details['email']).first()
            auth_token = user.encode_auth_token(user.id)
            if user and user.verify_password(user_details['password']):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
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
                        'message':'Login failed please try again.'}
            return make_response(jsonify(response))
        #add edge cases for wrong email or wrong password.


api.add_resource(UserRegistration, '/auth/register')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(GetUpdateDeleteUser, '/admin/changeuser/<int:id>.json')