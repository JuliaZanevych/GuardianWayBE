from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt, \
    set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from werkzeug.security import generate_password_hash

from datetime import timedelta

from resources.db import User, db

auth_blueprint = Blueprint('auth', __name__)

blacklist = set()


@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        try:
            user = User(
                email=data['email'],
                password=generate_password_hash(data['password']),
                username=data['username']
            )
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully!'}), 200
        except Exception as e:
            return jsonify({'message': 'An error occurred during registration.'}), 500
    else:
        return 'User already exists!', 400


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=2))
        refresh_token = create_refresh_token(identity=user.id, expires_delta=timedelta(hours=36))
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return 'Invalid email or password', 401


@auth_blueprint.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    resp = jsonify({'logout': True})
    unset_jwt_cookies(resp)
    return resp, 200


@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, expires_delta=timedelta(hours=2))
    resp = jsonify({'access_token': access_token})
    return resp, 200
