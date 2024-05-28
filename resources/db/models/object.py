from resources.db.db import db


class Object(db.Model):
    __tablename__ = "object"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)

    detection = db.relationship("Detection", backref="object")
