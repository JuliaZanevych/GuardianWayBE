from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required
from flask_socketio import SocketIO

from app.auth import auth_blueprint, blacklist
from app.data_processing import init_data_processing_hub

from resources.db import db


def create_app():
    app = Flask(__name__)

    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
    app.config['SQLALCHEMY_DATABASE_URI'] = '*******'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    db.init_app(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in blacklist

    socket_io = SocketIO(app)
    init_data_processing_hub(socket_io)

    app.register_blueprint(auth_blueprint)

    return app, socket_io


if __name__ == "__main__":
    app, socketio = create_app()


    @app.route('/test', methods=['get'])
    @jwt_required()
    def test():
        return '123'


    socketio.run(app, debug=True, host='0.0.0.0')
