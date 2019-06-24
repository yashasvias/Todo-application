from flask import make_response, request, json, jsonify
from flask_login import current_user, login_user, logout_user, login_required
from . import todo_api_blueprint
from flask_api import status
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from db import db



@login_required
@todo_api_blueprint.route('/api/todoitems', methods=['GET'])
def get_todoitem():
    if current_user.is_authenticated:

        data = []
        for row in db.session.query(db.Todoitem).filter(db.Todoitem.id != None):
            data.append(row.to_json())
            response = jsonify(data)



        return response
    return make_response(jsonify({'message': 'You are not logged in'}))

@login_required
@todo_api_blueprint.route('/api/todoitem/<id>', methods=['PUT'])
def update_todoitem(id):
    if current_user.is_authenticated:

        item = db.session.query(db.Todoitem).filter(db.Todoitem.id == 'id')
        username = request.form['username']
        title = request.form['title']


        if item is not None:
            try:

                item.title = "title"

                db.session.add(item)
                db.session.commit()

                response = jsonify({'message': 'updated'})
            except SQLAlchemyError as e:
                print(e)
                response = jsonify({"message": "error in updateing the data"})
                return response, status.HTTP_500_INTERNAL_SERVER_ERROR

        else:
            response = jsonify({'message': 'Cannot find item'}), 404

        return response
    return make_response(jsonify({'message': 'You are not logged in'}))

@login_required
@todo_api_blueprint.route('/api/todoitem/create', methods=['POST'])
def post_register():
    if current_user.is_authenticated:


        t = request.form['title']
        c = request.form['comment']
        user = current_user.get_username()
        print(user)

        todo_item = db.Todoitem(username=user,title=t,comment=c)


        db.session.add(todo_item)
        db.session.commit()

        response = jsonify(
            {'message': 'item added', 'result': todo_item.to_json()})

        return response
    return make_response(jsonify({'message': 'You are not logged in'}))