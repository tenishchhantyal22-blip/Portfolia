from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))
    location = db.Column(db.String(100))

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posted_by = db.Column(db.String(100))
    resource_type = db.Column(db.String(50))
    quantity = db.Column(db.Integer)
    location = db.Column(db.String(100))
    Urgency = db.Column(db.String(20))
    status = db.Column(db.String(20), default="open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'))
    volunteer_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    matched_at = db.Column(db.DateTime, default=datetime.utcnow)
