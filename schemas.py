from marshmallow import Schema, fields


class PersonsSchema(Schema):
    name = fields.Str(required=True)
    lastName = fields.Str(required=True)

class TagsSchema(Schema):
    id = fields.Int(required=True)
    name = fields.Str(required=True)

class ActionsSchema(PersonsSchema, TagsSchema):
    id= fields.Int(required=True)
    description=fields.Str(required=True)
    action = fields.Str(required=True)
    tag = fields.List(fields.Nested(TagsSchema(), required=True))
    category= fields.Str(required=True)
    persons = fields.List(fields.Nested(PersonsSchema()))

class ActionSchema(TagsSchema):
    id=fields.Int(required=True)
    description=fields.Str(required=True)
    action = fields.Str(required=True)
    tag = fields.List(fields.Nested(TagsSchema(), required = True))
    category = fields.Str(required=True)