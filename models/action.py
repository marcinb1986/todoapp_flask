from models.tag import TagModel
# from models.person import PersonModel
from db import db
# from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.dialects.postgresql as postgresql
# db = SQLAlchemy()
# class Action(Base):


class ActionModel(db.Model):

    __tablename__ = 'actions'

    id = db.Column(db.String, primary_key=True)
    action = db.Column(db.String(80))
    category = db.Column(db.String(80))
    description = db.Column(db.String(100))
    # one-to-one relationship
    tag = db.relationship(TagModel, backref='action',
                          uselist=False, lazy=True)
    # one-to-many relationship
    persons = db.relationship('PersonModel', back_populates="action")

    def serialize(self):
        return {
            'id': self.id,
            'action': self.action,
            'category': self.category,
            'description': self.description,
            'tag': self.tag.serialize() if self.tag else None,
            'persons': [person.serialize() for person in self.persons]
        }
