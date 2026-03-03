from marshmallow import Schema, fields


class UserLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=True)


class UserLoginResponseSchema(Schema):
    message = fields.Str()
    access_token = fields.Str()
    user_id = fields.Str()
