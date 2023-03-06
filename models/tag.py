# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

# Base = declarative_base()
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# class Tag(Base):
class TagModel(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String)
    action_id = db.Column(db.Integer, db.ForeignKey('actions.id'))
    action = db.relationship("Action", uselist=False, lazy='dynamic')