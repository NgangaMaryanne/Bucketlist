from marshmallow import Schema, fields, pprint, validate


class BucketlistItemSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be empty.')
    id = fields.Integer(dump_only=True)
    name = fields.Str(validate=not_blank)
    date_created = fields.Date()
    date_modified = fields.Date()
    done = fields.Boolean(validate=not_blank)
    bucketlist_id = fields.Integer(validate=not_blank)


class BucketlistSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be empty.')
    id = fields.Integer(dump_only=True)
    name = fields.Str(validate=not_blank)
    date_created = fields.Date()
    date_modified = fields.Date()
    created_by = fields.Integer()
    items = fields.Nested(BucketlistItemSchema(), many=True, uselist=True)


class UserSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")
    id = fields.Integer(dump_only=True)
    email = fields.Email(validate=not_blank)
    username = fields.Str(validate=not_blank)
    first_name = fields.Str()
    last_name = fields.Str()
    password_hash = fields.Str(validate=not_blank)
    is_admin = fields.Boolean()
    bucketlists = fields.Nested(BucketlistSchema(), many=True)
