from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import func

from resources.db import Detection, db, Location

analytics_blueprint = Blueprint('analytics', __name__)


@analytics_blueprint.route('/detections', methods=['get'])
@jwt_required()
def get_detections():
    print('HERE')
    lat = request.args.get('latitude', type=float)
    lon = request.args.get('longitude', type=float)
    if lat is not None and lon is not None:
        point = func.ST_SetSRID(func.ST_MakePoint(lon, lat), 4326)
        nearest_locations = db.session.query(Location).filter(func.ST_DWithin(Location.geo, point, 5000)).all()
        detections = Detection.query.filter(
            Detection.location_id.in_([location.id for location in nearest_locations])).all()
    else:
        detections = Detection.query.all()
    return jsonify([{
        'objectId': detection.object_id,
        'density': detection.density,
        'longitude': detection.location.longitude,
        'latitude': detection.location.latitude,
    } for detection in detections])
