from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required
from flask_socketio import SocketIO
from flask_cors import CORS

from app import data_processing_blueprint
from app.auth import auth_blueprint, blacklist
from app.data_processing import init_data_processing_hub
from app.analytics import analytics_blueprint

from resources.db import db


def create_app():
    app = Flask(__name__)
    CORS(app, cors_allowed_origins='*' )

    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
    app.config['SQLALCHEMY_DATABASE_URI'] = ''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    app.config['JWT_TOKEN_LOCATION'] = ["headers"]

    db.init_app(app)
    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload["jti"]
        return jti in blacklist

    socket_io = SocketIO(app, cors_allowed_origins='*', async_mode='threading')

    init_data_processing_hub(socket_io)

    app.register_blueprint(auth_blueprint)
    app.register_blueprint(analytics_blueprint, url_prefix='/analytics')
    app.register_blueprint(data_processing_blueprint, url_prefix='/data_processing')

    return app, socket_io


if __name__ == "__main__":
    app, socketio = create_app()
    socketio.run(app, debug=True, host='0.0.0.0', ssl_context=('cert.pem', 'key.pem'))
