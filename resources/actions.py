import inspect
from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models.action import ActionModel
from schemas import ActionsSchema, ActionSchema
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

            # print(f"filtered actions: {filtered_actions}")
            for filtered_action in filtered_actions:
                action = ActionModel.query.get_or_404(filtered_action['id'])
                if action:
                    action.action = filtered_action['action']
                    action.category = filtered_action['category']
                    action.description = filtered_action['description']
                    action.tag.name = filtered_action['tag']['name']

                    if filtered_action['tag']:
                        if action.tag:
                            action.tag.name = filtered_action['tag']['name']

                    for d in data:
                        if d['id'] == filtered_action['id']:
                            for person in d['persons']:
                                print(f"person:{person}")
                                action.persons.name = person['name']
                                action.persons.last_name = person['lastName']
                    print(action)
                    # print(f"filtered_action:{filtered_action}")
                    # for person in filtered_action['persons']:
                    #     # print(F"person:{person}")
                    #     person_data = next(
                    #         (d for d in data if d['id'] == person['id']), None)
                    #     # print(
                    #     #     f"d['id']={d['id']}, person['id']={person['id']}")
                    #     # print(person_data)
                    #     if person_data:
                    #         person_obj = PersonModel.query.get_or_404(
                    #             person['id'])
                    #         person_obj.name = person.data['name']
                    #         person_obj.last_name = person_data['last_name']

                    db.session.add(action)
                    db.session.commit()
                    # else:
                    #     persons = PersonModel(
                    #         id=filtered_action['persons']['id'],
                    #         name=filtered_action['persons']['name'],
                    #         last_name=filtered_action['persons']['last_name'],
                    #         action_id=filtered_action['id']
                    #     )
                    #     db.session.add(persons)

                    # print(filtered_actions)
                    # for filtered_action in filtered_actions:
                    #     act_data = next(
                    #         (d for d in data if d['id'] == filtered_action['id']), None)
                    #     update_action(filtered_action, act_data)

            return jsonify({'message': 'Actions updated successfully'}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500

        # changed_ids = []
        # for d in data:
        #     if d not in actions_dict:
        #         changed_ids.append(d['id'])

        # filtered_actions = []
        # for id in changed_ids:
        #     filtered_action = ActionModel.query.filter(
        #         ActionModel.id == id).first()
        #     if filtered_action:
        #         filtered_actions.append(filtered_action)

        # for i in range(len(data)):
        #     if data[i]['id'] in changed_ids:
        #         modified_action = filtered_actions[changed_ids.index(
        #             data[i]['id'])]
        #         modified_action.name = data[i]['name']

        # db.session.commit()

        # filtered_actions_dict = [x.serialize() for x in filtered_actions] // zmiana z ActionModel do tablicy obiektów
        # print(filtered_actions_dict)
        #     for action in ActionModel.query.filter(ActionModel.id.in_(changed_ids)):
        #         request_data_for_action = next(
        #             filter(lambda d: d['id'] == action.id, request_data), None)
        #         if request_data_for_action is not None:
        #             action.attribute_1 = request_data_for_action['attribite_1']
        #             action.attribute_2 = request_data_for_action['attribute_2']
        #             # Add code to update tag here
        #             if 'tag' in request_data_for_action:
        #                 tag = request_data_for_action['tag']
        #                 action.tag_id = tag[0]['id']
        #             db.session.add(action)
        #     db.session.commit()
        #     return jsonify({'success': True})

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
