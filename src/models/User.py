from datetime import datetime
from src.models.Database import db


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(120), unique=True)
    is_verified = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(128))
    role = db.Column(db.String(100), default='ROLE_USER')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    type = db.Column(db.String(50))

    __mapper_args__ = {
        'polymorphic_identity': 'User',
        'polymorphic_on': type
    }

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email
        self.role = 'ROLE_USER'

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at
        }
