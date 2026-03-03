from marshmallow import Schema, fields, validate


class ProductSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=3))
    description = fields.Str(required=True)
    price = fields.Float(required=True)
    old_price = fields.Float(required=False, allow_none=True)
    sizes = fields.List(fields.Str(validate=validate.OneOf(['S', 'M', 'L', 'XL', 'XXL'])), required=True)
    colors = fields.List(fields.Str(), required=True)
    stock = fields.Int(required=True)
    category = fields.Str(required=True)
    tags = fields.List(fields.Str(), required=True)
