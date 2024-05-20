from functools import wraps
from flask import session
from flask_socketio import send, disconnect, emit
from flask_jwt_extended import jwt_required, verify_jwt_in_request, get_jwt_identity, get_unverified_jwt_headers
from geoalchemy2 import WKTElement
from flask import jsonify, Blueprint, request
from jwt import ExpiredSignatureError
from flask_jwt_extended.exceptions import NoAuthorizationError

from datetime import datetime

import json

from resources.db import Object, Location, db, Detection

data_processing_blueprint = Blueprint('data_processing', __name__)


def init_data_processing_hub(socketio):
    @socketio.on('connect')
    @jwt_required()
    def verify_token():
        session['user_id'] = get_jwt_identity()
        print('Client connected!')

    @socketio.on_error()
    def error_handler(error):
        print(error)
        if isinstance(error, NoAuthorizationError) or isinstance(error, ExpiredSignatureError):
            disconnect()
        pass

    @socketio.on('disconnect')
    def test_disconnect():
        print('Client disconnected')

    @socketio.on('test')
    def test_disconnect123(data):
        print('Client test', data)

    @socketio.on('detection')
    def handle_pothole(data):
        _object = Object.query.filter_by(id=data['object_id']).first()
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
                user_id=session['user_id'],
                timestamp=datetime.fromisoformat(data['timestamp']),
                density=data['density']
            )
            db.session.add(new_detection)
            db.session.commit()
            print('New detection add!')
        else:
            existing_detection.timestamp = datetime.fromisoformat(data['timestamp'])
            existing_detection.density = data['density']
            db.session.commit()
            print('Detection updated!')

    @socketio.on('detection_batch')
    def handle_detection_batch(data):
        print(data)
        for detection in data['detections']:
            _object = Object.query.filter_by(id=detection['object_id']).first()
            if not _object:
                print('No Object!')
                emit('error', f'Unknown Object with id {detection["object_id"]}')
                continue

            nearest_location = Location.nearest(detection['location']['longitude'], detection['location']['latitude'])
            if not nearest_location:
                nearest_location = Location(
                    latitude=detection['location']['latitude'],
                    longitude=detection['location']['longitude'],
                    geo=WKTElement(f"POINT({detection['location']['longitude']} {detection['location']['latitude']})",
                                   srid=4326))
                db.session.add(nearest_location)
                db.session.commit()
                print('New point created!')

            existing_detection = Detection.query.filter_by(
                object_id=detection['object_id'],
                location_id=nearest_location.id).first()

            if not existing_detection:
                new_detection = Detection(
                    object_id=detection['object_id'],
                    location_id=nearest_location.id,
                    user_id=session['user_id'],
                    timestamp=datetime.fromisoformat(detection['timestamp']),
                    density=detection['density']
                )
                db.session.add(new_detection)
                print('New detection add!')
            else:
                existing_detection.timestamp = datetime.fromisoformat(detection['timestamp'])
                existing_detection.density = detection['density']
                print('Detection updated!')

        print('Batch_saved!')
        emit('batch_saved', data['batchId'])
        db.session.commit()


@data_processing_blueprint.route('/process_data_batch', methods=['POST'])
@jwt_required()
def handle_detection_batch():
    data = request.get_json()
    print(data)

    for index, detection in enumerate(data['detections']):
        _object = Object.query.filter_by(id=detection['object_id']).first()
        if not _object:
            print('No Object!')
            return f'Unknown Object with id {detection["object_id"]}', 404

        nearest_location = Location.nearest(detection['location']['longitude'],
                                            detection['location']['latitude'], radius=5)
        if not nearest_location:
            nearest_location = Location(
                latitude=detection['location']['latitude'],
                longitude=detection['location']['longitude'],
                geo=WKTElement(f"POINT({detection['location']['longitude']} {detection['location']['latitude']})",
                               srid=4326))
            db.session.add(nearest_location)
            db.session.commit()
            print('New point created!')

        existing_detection = Detection.query.filter_by(
            object_id=detection['object_id'],
            location_id=nearest_location.id).first()

        if not existing_detection:
            new_detection = Detection(
                object_id=detection['object_id'],
                location_id=nearest_location.id,
                user_id=get_jwt_identity(),
                timestamp=datetime.fromisoformat(detection['timestamp']),
                density=detection['density']
            )
            db.session.add(new_detection)
            print('New detection add!')
        else:
            existing_detection.timestamp = datetime.fromisoformat(detection['timestamp'])
            existing_detection.density = detection['density']
            print('Detection updated!')

    print('Batch_saved!')
    db.session.commit()
    return jsonify({"batchId": data['batchId']}), 200
