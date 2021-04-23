from marshmallow import Schema, fields


class ProductSchema(Schema):
    id = fields.Integer()
    name = fields.String()
    code = fields.String()
    description = fields.String()
    price = fields.Decimal()


class CartSchema(Schema):
    id = fields.Integer()
    created_at = fields.DateTime()
    state = fields.String()
    total = fields.Decimal()


class CartItemSchema(Schema):
    id = fields.Integer()
    qty = fields.Integer()
    total = fields.Decimal()

    product = fields.Nested(ProductSchema)
