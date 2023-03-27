import inspect
from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.action import ActionModel
from schemas import ActionsSchema, ActionSchema, UpdatedActionSchema
from sqlalchemy.exc import SQLAlchemyError
import uuid
from db import db
from models.person import PersonModel
from models.tag import TagModel
import json

blp = Blueprint('actions', __name__, description="Operation on actions")


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


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

    if request.method == 'PUT':
        data = request.json
        # print(f"data:{data}")
        actions_schema = ActionsSchema()
        try:
            actions_data = actions_schema.parse_obj(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        try:
            actions = ActionModel.query.all()
            actions_dict = [action.serialize() for action in actions]
            changed_ids = []
            for d in data:
                if d not in actions_dict:
                    changed_ids.append(d['id'])

            filtered_actions = []
            for id in changed_ids:
                filtered_action = ActionModel.query.filter(
                    ActionModel.id == id).first()
                if filtered_action:
                    filtered_actions.append(filtered_action.serialize())

            print(f"filtered actions: {filtered_actions}")
            for filtered_action in filtered_actions:
                action = ActionModel.query.get_or_404(filtered_action['id'])
                # id = filtered_action['id']
                if action:
                    for d in data:
                        if d['id'] == filtered_action['id']:
                            action.action = d['action']
                            action.category = d['category']
                            action.description = d['description']
                            action.tag.name = d['tag']['name']

                            for person in action.persons:
                                for single_person in d['persons']:
                                    if person.id == single_person['id']:
                                        if person.serialize() != single_person:
                                            person.name = single_person['name']
                                            person.last_name = single_person['lastName']
            db.session.add(action)
            db.session.commit()

            return jsonify({'message': 'Actions updated successfully'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@blp.route('/action/<string:id>', methods=['GET', 'PUT', 'DELETE'])
def get_action(id):
    if request.method == 'GET':
        action = ActionModel.query.get_or_404(id)
        return jsonify(action.serialize()), 200

    if request.method == 'PUT':
        data = request.json

        key_to_lookup = 'id'
        for person in data['persons']:
            if key_to_lookup not in person:
                person['id'] = str(uuid.uuid4())

        try:
            UpdatedActionSchema.parse_obj(data)
        except ValueError as e:
            return jsonify({'error': str(e)}), 400

        action = ActionModel.query.get_or_404(id)

        action.action = data['action']
        action.description = data['description']
        action.category = data['category']
        action.tag.name = data['tag']['name'] if 'name' in data['tag'] else None

        payload_ids = set([person['id'] for person in data['persons']])
        person_action_ids = set([person.serialize()['id']
                                for person in action.persons])

        for person in action.persons:
            person_id = person.serialize()['id']
            if person_id in payload_ids:
                for d in data['persons']:
                    if person_id == d['id']:
                        person.name = d['name']
                        person.last_ame = d['lastName']
            else:
                action.persons.remove(person)

        for d in data['persons']:
            if d['id'] not in person_action_ids:
                person = {
                    'id': d['id'],
                    'name': d['name'],
                    'last_name': d['lastName']
                }
                new_person = PersonModel(**person)
                action.persons.append(new_person)

        db.session.add(action)
        db.session.commit()
        return jsonify({'message': 'success'})

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
