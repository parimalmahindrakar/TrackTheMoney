from marshmallow import fields, Schema

class UserSchema(Schema):
    _id = fields.String()
    username = fields.String()
    email = fields.String()
