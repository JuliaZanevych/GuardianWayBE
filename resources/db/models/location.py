from sqlalchemy import func

from resources.db.db import db
from geoalchemy2 import Geography


class Location(db.Model):
    __tablename__ = "location"

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.REAL, nullable=False)
    longitude = db.Column(db.REAL, nullable=False)
    geo = db.Column(Geography(geometry_type='POINT', srid=4326))

    detection = db.relationship("Detection", backref="location")

    @classmethod
    def nearest(cls, longitude, latitude):
        point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
        nearest_location = db.session.query(cls).filter(func.ST_DWithin(cls.geo, point, 10)).first()
        return nearest_location
