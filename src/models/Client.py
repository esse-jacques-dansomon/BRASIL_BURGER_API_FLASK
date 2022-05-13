from sqlalchemy import ForeignKey

from src.models.Database import db
from src.models.User import User


class Client(User):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, ForeignKey('users.id'), primary_key=True)
    phone = db.Column(db.String(20), nullable=False, unique=True)
    orders = db.relationship('Order', back_populates='client')
    addresses = db.relationship('Address', back_populates='client')
    __mapper_args__ = {
        'polymorphic_identity': 'client'
    }

    def __init__(self, username, password, email, phone):
        super().__init__(username, password, email)
        self.phone = phone
        self.role = 'ROLE_USER'

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'phone': self.phone,
            'role': self.role,
            'is_verified': self.is_verified,

        }

    def __repr__(self):
        return self.serialize()

    def save(self):
        db.session.add(self)
        try:
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return False
        return True

