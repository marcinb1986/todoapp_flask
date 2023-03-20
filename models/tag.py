# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
# from flask_sqlalchemy import SQLAlchemy
# from models.action import ActionModel
from db import db

# class Tag(Base):


class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(80))
    action_id = db.Column(db.String, db.ForeignKey('actions.id'), unique=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'action_id': self.action_id
        }
