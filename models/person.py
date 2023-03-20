# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
from db import db
# from flask_sqlalchemy import SQLAlchemy
# from models.action import ActionModel
# Base = declarative_base()

# db = SQLAlchemy()

# class Person(Base):


class PersonModel(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    last_name = db.Column(db.String)
    action_id = db.Column(db.String, db.ForeignKey('actions.id'))
    action = db.relationship(
        "ActionModel", back_populates='persons')

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'lastName': self.last_name,
        }
