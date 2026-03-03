from marshmallow import Schema, fields


class RegistrationSchema(Schema):
    username = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    contact_number = fields.Str(required=True)
    street = fields.Str(required=True)
    pin_code = fields.Str(required=True)
    country = fields.Str(required=True)
