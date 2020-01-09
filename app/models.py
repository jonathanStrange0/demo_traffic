from app import db


class IntegrationPlatform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(128), index=True, unique=True)
    variants = db.relationship("Url", backref="url", cascade="save-update, delete, delete-orphan")


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128), index=True, unique=True)