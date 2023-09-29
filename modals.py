from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    deposit = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.DateTime, default=datetime.now)


class Transaction(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", backref=db.backref("user", uselist=False))
    type = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    Date = db.Column(db.DateTime, default=datetime.now)


