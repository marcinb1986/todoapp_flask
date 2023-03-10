# from marshmallow import Schema, fields
from pydantic import BaseModel, Field
from typing import List


class PersonsSchema(BaseModel):
    name: str
    lastName: str


class TagSchema(BaseModel):
    name: str


class ActionsSchema(BaseModel):
    id: int
    description: str
    action: str
    category: str
    tag: TagSchema
    persons: List[PersonsSchema]


class ActionSchema(BaseModel):
    description: str
    action: str
    category: str
    # tag: TagSchema


# class PersonsSchema(Schema):
#     name = fields.Str(required=True)
#     lastName = fields.Str(required=True)


# class TagsSchema(Schema):
#     id = fields.Int(required=True)
#     name = fields.Str(required=True)


# class ActionsSchema(Schema):
#     id = fields.Int(required=True)
#     description = fields.Str(required=True)
#     action = fields.Str(required=True)
#     tag = fields.List(fields.Nested(TagsSchema(), required=True))
#     category = fields.Str(required=True)
#     persons = fields.List(fields.Nested(PersonsSchema()))


# class ActionSchema(Schema):
#     id = fields.Int(required=True)
#     description = fields.Str(required=True)
#     action = fields.Str(required=True)
#     tag = fields.Nested(TagsSchema, many=True)
#     category = fields.Str(required=True)
