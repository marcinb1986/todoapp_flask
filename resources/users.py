import json
import uuid
from flask import jsonify, request
from login_schemas import LoginRegisterSchema
from db import db
from models.login_register import RegisterUserModel
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token
from passlib.hash import pbkdf2_sha256

blp = Blueprint("users", __name__, description="Operation on users")


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def change_dict(data):
    renamed_dict = {}
    for k, v in data.items():
        if k == 'userName':
            renamed_dict['user_name'] = v
        else:
            renamed_dict[k] = v
    return renamed_dict


@blp.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        data = request.json
        id_user = str(uuid.uuid4())
        data['id'] = id_user
        new_user_data = change_dict(data)
        if len(new_user_data['user_name']) or len(new_user_data['password']) == 0:
            abort(400, message="Missing user or password")
        try:
            LoginRegisterSchema.parse_obj(new_user_data)
            if RegisterUserModel.query.filter(RegisterUserModel.user_name == new_user_data['user_name']).first():
                abort(409, message="A user with that username already exist")
            hashed_password = pbkdf2_sha256.hash(new_user_data['password'])
            new_user_data['password'] = hashed_password
            user_data = RegisterUserModel(**new_user_data)
            db.session.add(user_data)
            db.session.commit()
            return ({'message': 'success'})
        except ValueError as e:
            return jsonify({'error': str(e)})

    if request.method == 'GET':
        users = RegisterUserModel.query.all()
        users_dict = [user.serialize() for user in users]
        return jsonify(users_dict)


@blp.route('/register/<string:id>', methods=['DELETE'])
def delete_user(id):
    user = RegisterUserModel.query.get_or_404(id)
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@blp.route('/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        data = request.json
        new_user_data = change_dict(data)
        try:
            user = RegisterUserModel.query.filter(
                RegisterUserModel.user_name == new_user_data['user_name']
            ).first()

            if user and pbkdf2_sha256.verify(new_user_data['password'], user.password):
                access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'error': str(e)
            }), 500
