from marshmallow import Schema, fields

class BankSchema(Schema):
    id = fields.String()
    name = fields.String()
    total_initial_amount = fields.Float()
    total_remaining_amount = fields.Float()
