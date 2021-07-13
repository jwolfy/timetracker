import uuid
import sqlalchemy
import jwt
import datetime
import logging

from flask import current_app, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from app.api.models import db, User
from app.api import api
from http import HTTPStatus
from functools import wraps

logger = logging.getLogger(__name__)


def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if current_app.config.get('LOGIN_REQUIRED_DISABLED'):
            return func(*args, **kwargs)

        token = None

        if 'x-access-token' in request.headers:
            token = request.headers.get('X-Access-Token')

        if not token:
            return jsonify({'message': 'Token is missing'}), HTTPStatus.UNAUTHORIZED

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except Exception as e:
            logger.exception(e)
            return jsonify({'message': 'Token is invalid'}), HTTPStatus.UNAUTHORIZED

        return func(current_user, *args, **kwargs)

    return decorated


def admin_login_required(func):
    @wraps(func)
    def decorated(current_user=None, *args, **kwargs):
        if current_app.config.get('ADMIN_LOGIN_REQUIRED_DISABLED'):
            return func(*args, **kwargs)

        if not current_user or not current_user.is_admin:
            return jsonify({'message': 'Cannot perform that function'}), HTTPStatus.UNAUTHORIZED

        return func(*args, **kwargs)

    return decorated


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()),
                    name=data['username'],
                    password=hashed_password,
                    is_admin=False)
    try:
        db.session.add(new_user)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        logger.exception(e)
        return jsonify({'message': 'Could not create user. Try a different username'}), HTTPStatus.CONFLICT

    return jsonify({
        'message': 'New user created',
        'user': {
            'public_id': new_user.public_id,
            'name': new_user.name,
            'password': new_user.password,
            'is_admin': False,
        },
    }), HTTPStatus.CREATED


@api.route('/users', methods=['GET'])
@login_required
@admin_login_required
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['name'] = user.name
        user_data['password'] = user.password
        user_data['is_admin'] = user.is_admin
        output.append(user_data)

    return jsonify({'users': output}), HTTPStatus.OK


@api.route('/users/<public_id>', methods=['GET'])
@login_required
@admin_login_required
def get_user(public_id):
    user = User.get(public_id)

    if not user:
        return jsonify({'message': 'No user found'}), HTTPStatus.NOT_FOUND

    user_data = {}
    user_data['public_id'] = user.public_id
    user_data['name'] = user.name
    user_data['password'] = user.password
    user_data['is_admin'] = user.is_admin

    return jsonify({'user': user_data})


@api.route('/users/<public_id>', methods=['PUT'])
@login_required
@admin_login_required
def promote_user(public_id):
    user = User.get(public_id)

    if not user:
        return jsonify({'message': 'No user found'}), HTTPStatus.NOT_FOUND

    user.is_admin = True
    db.session.commit()

    return jsonify({'message': 'The user has been promoted'}), HTTPStatus.OK


@api.route('/users/<public_id>', methods=['DELETE'])
@login_required
@admin_login_required
def delete_user(public_id):
    user = User.get(public_id)

    if not user:
        return jsonify({'message': 'No user found'}), HTTPStatus.NOT_FOUND

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'The user has been deleted'}), HTTPStatus.OK


def unauthorized_response():
    return make_response(
        'Could not verify',
        HTTPStatus.UNAUTHORIZED,
        {'WWW-Authenticate': 'Basic realm="Timetracker API"'},
    )


@api.route('/login', methods=['GET'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return unauthorized_response()

    user = User.query.filter_by(name=auth.username).first()

    if not user:
        return unauthorized_response()

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {
                'public_id': user.public_id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256',
        )
        return jsonify({'token': token}), HTTPStatus.OK

    return unauthorized_response()
