# from marshmallow import Schema, fields
from pydantic import BaseModel
from typing import List, Optional


class PersonsSchema(BaseModel):
    id: str
    name: Optional[str]
    lastName: Optional[str]


class TagSchema(BaseModel):
    name: Optional[str]
    id: Optional[str]


class UpdatedActionSchema(BaseModel):
    id: str
    description: str
    action: str
    category: str
    tag: TagSchema
    persons: Optional[List[PersonsSchema]] = None


class ActionsSchema(BaseModel):
    __root__: List[UpdatedActionSchema] = []


class ActionSchema(BaseModel):
    description: str
    action: str
    category: str
    tag: TagSchema
