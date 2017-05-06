from functools import wraps
import datetime

from flask import request, make_response, jsonify, g as global_user
from flask_restful import Resource, Api, reqparse
from sqlalchemy.exc import SQLAlchemyError

from .import apiv1
from ..models import User, Bucketlist, Item
from ..serializer import BucketlistSchema, BucketlistItemSchema
from .. import db

bucketlist_schema = BucketlistSchema()
items_schema = BucketlistItemSchema()
api = Api(apiv1)


# Handle authentication
def authentication_required(function):
    @wraps(function)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if not auth_token:
            response = {'message': 'Please login to access this resource.'}
            return make_response(jsonify(response))
        this_user_id = User.decode_auth_token(auth_token)
        if not isinstance(this_user_id, int):
            response = {'status': 'fail',
                        'error': this_user_id}
            return make_response(jsonify(response))
        global_user.user = this_user_id
        return function(*args, **kwargs)
    return decorated_function


class BucketlistApi(Resource):
    '''
    Bucketlist class for all bucketlists
    '''
    @authentication_required
    def get(self, bucket_id=None):
        '''
        implements the GET method of the API resource. if a bucket_id argument is given it returns the bucketlist with 
        that id else it returns all the bucketlists of the logged in user.
        '''
        if bucket_id:
            bucket = Bucketlist.query.filter_by(
                id=bucket_id, created_by=global_user.user).first()
            results = bucketlist_schema.dump(bucket)
            if results.data:
                return results
            else:
                response = {
                    'message': 'You do not have bucket with id {}. Please try again'.format(bucket_id)}
                return make_response(jsonify(response))
        else:
            if request.args.get('page'):
                page_number = int(request.args.get('page'))
            else:
                page_number = 1
            if request.args.get('limit'):
                limit = int(request.args.get('limit'))
            else:
                limit = 20
            if request.args.get('q'):
                q = str(request.args.get('q'))
                buckets = Bucketlist.query.filter(Bucketlist.name.like('%{}%'.format(q))).filter_by(
                    created_by=global_user.user).paginate(page_number, limit, False)

            else:
                buckets = Bucketlist.query.filter_by(
                    created_by=global_user.user).paginate(page_number, limit, False)
            if buckets.has_prev:
                previous_page = "{}api/v1/bucketlists?page={}&limit={}".format(
                    request.url_root, page_number - 1, limit)
            else:
                previous_page = None
            if buckets.has_next:
                next_page = "{}api/v1/bucketlists?page={}&limit={}".format(
                    request.url_root, page_number + 1, limit)
            else:
                next_page = None

            results = bucketlist_schema.dump(buckets.items, many=True)
            if results.data:
                response = jsonify({'previous page': previous_page,
                                    'next page': next_page,
                                    'results': results})
                response.status_code = 200
                return make_response(response)
            else:
                if request.args.get('q'):
                    q = request.args.get('q')
                    response = jsonify(
                        {'message': 'You do not have any bucketlists whose name contains {}.'.format(q)})
                    return make_response(response)
                else:
                    response = jsonify(
                        {'message': 'You do not have any bucketlists.'})
                    return make_response(response)

    @authentication_required
    def post(self):
        '''
        Implements the POST method of the API endpoint takes in a bucketlist name as an argument.
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', 'Please input bucketlist name.')
        new_bucketlist = parser.parse_args(strict=True)
        bucket = Bucketlist.query.filter_by(
            name=new_bucketlist['name']).first()
        bucket = bucketlist_schema.dump(bucket)
        if bucket.data:
            response = jsonify({'status': 'fail',
                                'message': 'Bucketlist with that name already exists. please try again.'
                                })
            response.status_code = 400
            return make_response(response)
        else:
            try:
                new_bucket = Bucketlist(
                    name=new_bucketlist['name'], created_by=int(global_user.user))
                db.session.add(new_bucket)
                db.session.commit()
                response = {'status': 'success',
                            'message': 'Bucketlist created.'}
                return make_response(jsonify(response))
            except(SQLAlchemyError):
                db.session.rollback()
                response = {'status': 'fail',
                            'message': str(SQLAlchemyError)}
                return make_response(jsonify(response))
            except(Exception):
                response = {'status': 'fail',
                            'message': str(Exception)}
                return make_response(jsonify(response))

    @authentication_required
    def put(self, bucket_id):
        '''
        Updates a bucketlist takes in the new bucketlist name as argument
        '''
        parser = reqparse.RequestParser()
        parser.add_argument(
            'name', type=str, help="Please input new bucketlist name.")
        updated_bucket = parser.parse_args(strict=True)
        bucket = Bucketlist.query.filter_by(
            id=bucket_id, created_by=int(global_user.user)).first()
        if bucket and updated_bucket:
            try:
                bucket.name = updated_bucket['name']
                bucket.date_modified = datetime.datetime.utcnow()
                db.session.add(bucket)
                db.session.commit()
                response = {'status': 'success',
                            'message': 'Bucketlist updated.'}
                return make_response(jsonify(response))
            except(Exception):
                response = {'status': 'fail',
                            'message': 'Please try again',
                            'error': str(Exception)}
                return make_response(jsonify(response))
            except(SQLAlchemyError):
                db.session.rollback()
                response = {'status': 'fail',
                            'message': str(SQLAlchemyError)}
                return make_response(jsonify(response))

        else:
            response = {
                'message': 'You do not have a bucket with id {0}'.format(bucket_id)}
            return make_response(jsonify(response))

    @authentication_required
    def delete(self, bucket_id):
        '''
        Deletes the bucketlist with the given id.
        '''
        bucket = Bucketlist.query.filter_by(
            id=bucket_id, created_by=int(global_user.user)).first()
        if bucket:
            try:
                db.session.delete(bucket)
                db.session.commit()
                response = {'status': 'success',
                            'message': 'Bucket {0} successfully deleted'.format(bucket_id)}
                return make_response(jsonify(response))
            except(Exception):
                response = {'status': 'failed',
                            'error': str(Exception)}
                return make_response(jsonify(response))
            except (SQLAlchemyError):
                db.session.rollback()
                response = {'status': 'failed',
                            'error': str(SQLAlchemyError)}
                return make_response(jsonify(response))
        else:
            response = {'status': 'failed',
                        'message': 'You dont have a bucketlist with id {0}'.format(bucket_id)}
            return make_response(jsonify(response))


class BucketlistItems(Resource):
    '''
    Bucketlist items class for each bucketlist. ie, adding, updating, getting and deleting 
    the items of a particular bucketlist.
    '''
    @authentication_required
    def post(self, bucket_id):
        '''
        Adds new items to a bucketlist
        '''
        parser = reqparse.RequestParser()
        parser.add_argument('name', help='Please input item name.')
        new_item = parser.parse_args()
        item_query = Item.query.filter_by(
            bucketlist_id=bucket_id, name=new_item['name']).first()
        if not item_query:
            try:
                item = Item(name=new_item['name'], bucketlist_id=bucket_id)
                db.session.add(item)
                db.session.commit()
                response = {'status': 'success',
                            'message': 'New item added to bucketlist.'}
                return make_response(jsonify(response))
            except(SQLAlchemyError):
                db.session.rollback()
                response = {'status': 'fail',
                            'message': SQLAlchemyError}
                return make_response(jsonify(response))
            except(Exception):
                response = {'status': 'fail',
                            'message': str(Exception)}
                return make_response(jsonify(response))
        else:
            response = {'status': 'fail',
                        'message': 'Item with that name exists please try again.'}
            return make_response(jsonify(response))

    @authentication_required
    def put(self, bucket_id, item_id):
        '''
        Updates a bucketlist item given the bucketlist id and the item name
        '''
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument(
            "done", type=str, help="Please input 'true' for done or 'false' for not done.")
        updated_item = parser.parse_args()
        bucket_query = Bucketlist.query.filter_by(
            id=bucket_id, created_by=int(global_user.user)).first()
        bucket_results = bucketlist_schema.dump(bucket_query)
        if bucket_results.data:
            item_query = Item.query.filter_by(
                id=item_id, bucketlist_id=bucket_id).first()
            if item_query:
                try:
                    if updated_item['name']:
                        item_query.name = updated_item['name']
                    if updated_item['done'] and updated_item['done'].lower() in ["false", "true"]:
                        if updated_item['done'].lower() == "true":
                            item_query.done = True
                        else:
                            item_query.done = False
                    item_query.date_modified = datetime.datetime.utcnow()
                    db.session.add(item_query)
                    db.session.commit()
                    bucket_query.date_modified = datetime.datetime.utcnow()
                    db.session.add(bucket_query)
                    db.session.commit()
                    response = {'status': 'success',
                                'message': 'item {} updated successfully'.format(item_id)}
                    return make_response(jsonify(response))
                except(SQLAlchemyError):
                    db.session.rollback()
                    response = {'status': 'fail',
                                'message': str(SQLAlchemyError)}
                    return make_response(jsonify(response))
                except(Exception):
                    response = {'status': 'fail',
                                'message': str(Exception)}
                    return make_response(jsonify(response))
            else:
                response = {'status': 'fail',
                            'message': 'Bucketlist {0} has no item {1}' .format(bucket_id, item_id)}
                return make_response(jsonify(response))
        else:
            response = {'status': 'fail',
                        'message': 'You do not have bucketlist with id {}'.format(bucket_id)
                        }
            return make_response(jsonify(response))

    @authentication_required
    def delete(self, bucket_id, item_id):
        '''
        Deletes a bucketlist item given the bucket id and the item name.
        '''
        bucket_query = Bucketlist.query.filter_by(id=bucket_id).first()
        if bucket_query:
            item = Item.query.filter_by(id=item_id).first()
            if item:
                try:
                    db.session.delete(item)
                    db.session.commit()
                    response = {'status': 'success',
                                'message': 'item deleted.'}
                    return make_response(jsonify(response))
                except(SQLAlchemyError):
                    response = {'status': 'fail',
                                'message': 'Please try again.'}
                    return make_response(jsonify(response))
                except(Exception):
                    response = {'status': 'fail',
                                'message': str(Exception)
                                }
                    return make_response(jsonify(response))
            else:
                response = {'status': 'fail',
                            'message': 'Item does not exist. Please try again.'}
                return make_response(jsonify(response))
        else:
            response = {'status': 'fail',
                        'message': 'You do not have bucketlist with id {}'.format(bucket_id)
                        }
            return make_response(jsonify(response))


api.add_resource(BucketlistApi, '/api/v1/bucketlists',
                 '/api/v1/bucketlists/<int:bucket_id>')
api.add_resource(BucketlistItems, '/api/v1/bucketlists/<int:bucket_id>/items',
                 '/api/v1/bucketlists/<int:bucket_id>/items/<int:item_id>')
