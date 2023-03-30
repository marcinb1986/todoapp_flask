from db import db


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
