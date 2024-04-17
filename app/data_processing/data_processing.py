from flask_socketio import send, disconnect, emit
from flask_jwt_extended import jwt_required
from geoalchemy2 import WKTElement

from datetime import datetime

import json

from resources.db import Object, Location, db, Detection


def init_data_processing_hub(socketio):
    @socketio.on('connect')
    @jwt_required()
    def verify_token():
        print('Client connected')

    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected')

    @socketio.on('detection')
    def handle_pothole(data):
        _object = Object.query.filter_by(id=str(data['object_id'])).first()
        if not _object:
            emit('error', f'Unknown Object with id {data["object_id"]}')
            return

        nearest_location = Location.nearest(data['location']['longitude'], data['location']['latitude'])
        if not nearest_location:
            nearest_location = Location(
                latitude=data['location']['latitude'],
                longitude=data['location']['longitude'],
                geo=WKTElement(f"POINT({data['location']['longitude']} {data['location']['latitude']})", srid=4326
                               ))
            db.session.add(nearest_location)
            db.session.commit()
            print('New point created!')

        existing_detection = Detection.query.filter_by(object_id=data['object_id'],
                                                       location_id=nearest_location.id).first()

        if not existing_detection:
            new_detection = Detection(
                object_id=data['object_id'],
                location_id=nearest_location.id,
                timestamp=datetime.fromisoformat(data['timestamp']),
                density=data['density']
            )
            db.session.add(new_detection)
            db.session.commit()
        else:
            existing_detection.timestamp = datetime.fromisoformat(data['timestamp'])
            existing_detection.density = data['density']
            db.session.commit()
