# from sqlalchemy import Column, Integer, String, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base

from flask_sqlalchemy import SQLAlchemy

# Base = declarative_base()

db = SQLAlchemy()

# class Person(Base):
class PersonModel(db.Model):
    __tablename__ = 'persons'

    # id = Column(Integer, primary_key = True)
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    last_name = db.Column(db.String)
    action_id = db.Column(db.Integer,db.ForeignKey('actions.id'))
    action = db.relationship("ActionModel", back_populates='persons', lazy='dynamic')


