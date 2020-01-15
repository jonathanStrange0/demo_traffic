from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class IntegrationPlatform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    platform = db.Column(db.String(128), index=True, unique=True)
    urls = db.relationship("Url", backref="url", cascade="save-update, delete, delete-orphan")


class Url(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(128), index=True, unique=True)
    num_headless = db.Column(db.Integer)
    num_windows = db.Column(db.Integer)
    platform_id = db.Column(db.Integer, db.ForeignKey('integration_platform.id'))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(64), index=True, unique=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))
