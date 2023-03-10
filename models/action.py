
from flask_sqlalchemy import SQLAlchemy
# from models.tag import TagModel
# from models.person import PersonModel

db = SQLAlchemy()

# class Action(Base):


class ActionModel(db.Model):

    __tablename__ = 'actions'

    # id = Column(Integer, primary_key=True)
    id = db.Column(db.String, primary_key=True)
    action = db.Column(db.String(80))
    category = db.Column(db.String)
    description = db.Column(db.String)
    # tag = db.relationship(TagModel, uselist=False)
    # tag_id = db.Column(db.String, db.ForeignKey('tags.id'))
    # one-to-one relationship
    # persons = db.relationship(PersonModel, back_populates="action")
    # one-to-many relationship
