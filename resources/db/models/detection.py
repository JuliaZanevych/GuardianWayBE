from resources.db.db import db


class Detection(db.Model):
    __tablename__ = "detection"

    id = db.Column(db.Integer, primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey("object.id"), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("location.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    timestamp = db.Column(db.TIMESTAMP, nullable=False)
    density = db.Column(db.REAL, nullable=False)
