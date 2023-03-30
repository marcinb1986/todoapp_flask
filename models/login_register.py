from db import db


class RegisterUserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String, primary_key=True)
    user_name = db.Column(db.String)
    password = db.Column(db.String)

    def serialize(self):
        return {
            'id': self.id,
            'userName': self.user_name,
            'password': self.password
        }
