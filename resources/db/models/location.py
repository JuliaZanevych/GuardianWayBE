from sqlalchemy import func, text, select, literal_column, over

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
    def nearest(cls, longitude, latitude, radius=10):
        point = func.ST_SetSRID(func.ST_MakePoint(longitude, latitude), 4326)
        nearest_location = db.session.query(cls).filter(func.ST_DWithin(cls.geo, point, radius)).first()
        return nearest_location

    @classmethod
    def nearest_neighbors(cls, points, radius=10):
        session = db.session

        points_text = ', '.join(f"ST_SetSRID(ST_MakePoint({lon}, {lat}), 4326)" for lon, lat in points)
        query_text = f"point, row_number() OVER () AS idx FROM unnest(array[{points_text}]) AS point"

        temp_table = select(
            literal_column("point"),
            literal_column("idx")
        ).select_from(select(text(query_text))).cte('temp_table')

        nearest_neighbors_query = (session.query(
            temp_table.c.idx,
            cls
        ).distinct(temp_table.c.idx).outerjoin(
            cls, func.ST_DWithin(cls.geo, temp_table.c.point, radius)
        ))

        results = []
        query_results = nearest_neighbors_query.all()
        for idx, neighbor in query_results:
            if neighbor:
                results.append(neighbor)
            else:
                results.append(None)

        session.close()
        return results
