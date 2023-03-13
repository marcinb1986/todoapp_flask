from models.tag import TagModel
# from models.person import PersonModel
from db import db
# from flask_sqlalchemy import SQLAlchemy
import sqlalchemy.dialects.postgresql as postgresql
# db = SQLAlchemy()
# class Action(Base):


class ActionModel(db.Model):

    __tablename__ = 'actions'

    # id = Column(Integer, primary_key=True)
    id = db.Column(db.String, primary_key=True)
    # id = db.Column(postgresql.UUID(as_uuid=True),
    #                primary_key=True, default=uuid.uuid4, unique=True)
    action = db.Column(db.String(80))
    category = db.Column(db.String(80))
    description = db.Column(db.String(100))
    tag = db.relationship(TagModel, backref='action',
                          uselist=False, lazy=True)
    # tag_id = db.Column(db.String, db.ForeignKey('tags.id'))
    # one-to-one relationship
    persons = db.relationship('PersonModel', back_populates="action")
    # one-to-many relationship
