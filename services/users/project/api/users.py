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
            print(f"adding ... {user}")
            response_object['message'] = f'{email} was added!'
            response_object['status'] = 'success'
            return jsonify(response_object), 201
        else:
            response_object['message'] = 'Sorry. That email already exists.'
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        return jsonify(response_object), 400
