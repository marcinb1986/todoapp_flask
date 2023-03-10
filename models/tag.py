# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
from flask_sqlalchemy import SQLAlchemy
from models.action import ActionModel
db = SQLAlchemy()

# class Tag(Base):


class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    action_id = db.Column(db.String, db.ForeignKey('actions.id'))
    action = db.relationship(ActionModel, uselist=False, lazy='dynamic')
