from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
# from db import actionsDb
from models.action import ActionModel
from schemas import ActionsSchema, ActionSchema
from sqlalchemy.exc import SQLAlchemyError

from flask_sqlalchemy import SQLAlchemy
from pydantic import ValidationError
import uuid
from db import db
from models.person import PersonModel
from models.tag import TagModel
# from models.action import ActionModel


# db = SQLAlchemy()

blp = Blueprint('actions', __name__, description="Operation on actions")


@blp.route('/actions', methods=['GET'])
def get_actions():
    actions = ActionModel.query.all()
    result = []
    for action in actions:
        action_data = {}
        action_data['id'] = action.id
        action_data['action'] = action.action
        action_data['category'] = action.category
        action_data['description'] = action.description
        action_data['tag'] = action.tag.name if action.tag else None
        result.append(action_data)
    return jsonify(result)


@blp.route('/allActions', methods=['POST', 'GET', 'PUT'])
def add_action():

    if request.method == 'GET':
        actions = ActionModel.query.all()
        actions_dict = [action.serialize() for action in actions]
        for action_dict in actions_dict:
            action_dict.pop('_sa_instance_state', None)
            tag = TagModel.query.filter_by(action_id=action_dict['id']).first()
            person = PersonModel.query.filter_by(
                action_id=action_dict['id']).all()
            action_dict['tag'] = tag.serialize() if tag else None
            action_dict['persons'] = [p.serialize()
                                      for p in person] if person else None
        # for action in actions:
        #     action_dict = action.__dict__
        #     action_dict.pop('_sa_instance_state', None)
        #     # print(action_dict)

        #     tag = action_dict.pop('tag')
        #     if tag:
        #         tag_dict = tag.serialize()
        #         action_dict['tag'] = tag_dict

        #     persons = action_dict.pop('persons')
        #     if persons:
        #         persons_dict = [person.serialize() for person in persons]
        #         action_dict['persons'] = persons_dict

        #     actions_dict.append(actions_dict)

        return jsonify(actions_dict)

    if request.method == 'POST':
        id_action = str(uuid.uuid4())
        id_tag = str(uuid.uuid4())
        id_persons = str(uuid.uuid4())
        try:
            add_action_request = ActionSchema(**request.json)
            action_data = add_action_request.dict()
            action_data['id'] = id_action
            name = ''
            last_name = ''
            person_data = {'name': name,
                           'last_name': last_name, 'id': id_persons}
            new_person = PersonModel(**person_data)
            action_data['persons'] = [new_person]

            tag_data = action_data.pop('tag')
            tag_data['id'] = id_tag
            new_tag = TagModel(**tag_data)

            new_action = ActionModel(**action_data)
            new_action.tag = new_tag
            new_action.persons = [new_person]

            db.session.add(new_action)
            db.session.commit()
            return jsonify({'success': True})
        except SQLAlchemyError as e:
            abort(
                500,
                message=str(e)
            )
        return request.json

        # @blp.route('/allActions')
        # class Actions(MethodView):
        #     # @cross_origin()
        #     # @blp.response(201, ActionsSchema(many=True))
        #     # def get(self):
        #     #     return jsonify(list(actionsDb.values()))

        #     # @blp.arguments(ActionSchema)
        #     # @blp.response(201, ActionSchema(many=True))
        #     # def post(self, request_data):
        #     #     action_id = request_data['id']
        #     #     actionsDb[action_id] = request_data
        #     #     return jsonify(list(actionsDb.values()))

        #     @blp.arguments(ActionSchema)
        #     @blp.response(201, ActionSchema(many=True))
        #     def post(self, request_data):
        #         print(1)
        #         print(request_data)
        #         # action = ActionModel(
        #         #     id=request_data['id'],
        #         #     action=request_data['action'],
        #         #     category=request_data['category'],
        #         #     description=request_data['description'],
        #         #     persons=[PersonModel(name='', last_name='', id=0)],
        #         #     tag=[TagModel(name=t['name'], id=request_data['id'])
        #         #          for t in request_data['tag']]
        #         # )

        #         # try:
        #         #     db.session.add(action)
        #         #     db.session.commit()
        #         # except SQLAlchemyError:
        #         #     abort(500,message='An error occured while adding action')

        #         return request_data
        #         # return action

        #     # @blp.arguments(ActionsSchema(many=True))
        #     # def put(self, request_data):
        #     #     print(request_data)
        #     #     request_dict = {d['id']: d for d in request_data}
        #     #     try:
        #     #         for key, value in actionsDb.items():
        #     #             if key in request_dict:
        #     #                 for k, v in value.items():
        #     #                     if v != request_dict[key][k]:
        #     #                         actionsDb[key][k] = request_dict[key][k]
        #     #         return jsonify(actionsDb)
        #     #     except KeyError:
        #     #         abort(404, message='Update not done')

        # # @blp.route('/action/<string:actionId>')
        # # class SingleActionUpdate(MethodView):

        # #     @blp.response(201, ActionsSchema)
        # #     def get(self, actionId):
        # #         action_id = int(actionId)
        # #         if action_id not in actionsDb:
        # #             abort(400, message='Bad request, not such action id')
        # #         try:
        # #             action = actionsDb[action_id]
        # #             return jsonify(action)
        # #         except KeyError:
        # #             abort(404, message='Action not found')

        # #     @blp.arguments(ActionsSchema)
        # #     @blp.response(201, ActionsSchema(many=True))
        # #     def put(self, request_data, actionId):
        # #         request_data = request.get_json(silent=True)
        # #         action_id = int(actionId)

        # #         try:
        # #             if action_id in actionsDb:
        # #                 actionsDb[action_id] = request_data
        # #             return actionsDb
        # #         except KeyError:
        # #             abort(404, message='Update not done')

        # #     @blp.response(201, ActionsSchema(many=True))
        # #     def delete(self, actionId):
        # #         action_id = int(actionId)
        # #         try:
        # #             actionsDb.pop(action_id)
        # #             return actionsDb
        # #         except KeyError:
        # #             abort(404, message='Delete not done')
