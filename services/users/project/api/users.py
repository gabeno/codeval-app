from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project.api.models import User
from project import db

users_blueprint = Blueprint("users", __name__)

@users_blueprint.route("/users/ping", methods=['GET'])
def ping_pong():
    return jsonify({
        'status': 'success',
        'message': 'pong!'
    })

@users_blueprint.route("/users", methods=['POST'])
def add_users():
    post_data = request.get_json()
    # XXX schema validation

    response_object = dict(
        message='Invalid payload.',
        status='fail'
    )

    if not post_data:
        return jsonify(response_object), 400

    username = post_data.get("username")
    email = post_data.get("email")

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            db.session.add(User(username=username, email=email))
            db.session.commit()
            response_object['message'] = f'{email} was added!'
            response_object['status'] = 'success'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That email already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400

@users_blueprint.route("/users/<user_id>", methods=['GET'])
def get_user(user_id):
    response_object = {
        'status': 'fail',
        'data': None,
        'message': 'User does not exist'
    }

    try:
        user = User.query.filter(User.id==user_id).first()
        if not user:
            return jsonify(response_object), 404
        else:
            data = dict(
                username=user.username,
                email=user.email,
                active=user.active,
                id=user.id
            )
            response_object['data'] = data
            response_object['status'] = 'success'
            response_object['message'] = 'User {user} found!'
            return jsonify(response_object), 200
    except exc.DataError as e:
        response_object['message'] = 'Only integer id supported'
        return jsonify(response_object), 400
