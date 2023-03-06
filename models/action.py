# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class Action(Base):
class ActionModel(db.Model):

    __tablename__ = 'actions'

    # id = Column(Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(80))
    category = db.Column(db.String)
    description = db.Column(db.String)
    persons = db.relationship("PersonModel", back_populates="action")
    #one-to-many relationship
    tag = db.relationship("Tag", uselist=False)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'))  
    #one-to-one relationship