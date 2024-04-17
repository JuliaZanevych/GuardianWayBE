from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
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
                password=generate_password_hash(data['password'])
            )
            db.session.add(user)
            db.session.commit()
            return jsonify({'message': 'User registered successfully!'}), 200
        except Exception as e:
            print(e)
            return jsonify({'message': 'An error occurred during registration.'}), 500
    else:
        return jsonify({'message': 'User already exists!'}), 400


@auth_blueprint.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        access_token = create_access_token(identity=user.email, expires_delta=timedelta(minutes=10))
        refresh_token = create_refresh_token(identity=user.email, expires_delta=timedelta(hours=36))
        return jsonify(access_token=access_token, refresh_token=refresh_token), 200
    else:
        return jsonify({'message': 'Invalid email or password'}), 401


@auth_blueprint.route('/logout', methods=['POST'])
@jwt_required(refresh=True)
def logout():
    jti = get_jwt()["jti"]
    blacklist.add(jti)
    return jsonify({"msg": "Successfully logged out"}), 200


@auth_blueprint.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity, expires_delta=timedelta(seconds=36))
    # jti = get_jwt()["jti"]
    # blacklist.add(jti)
    return jsonify(access_token=access_token)
