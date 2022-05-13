from datetime import datetime

from sqlalchemy.orm import dynamic

from src.models.Database import db


class Payment(db.Model):
    __tablename__ = 'payments'
    id = db.Column(db.Integer, primary_key=True)
    paid_at = db.Column(db.DateTime, nullable=True)
    type = db.Column(db.String(255), nullable=True, default='cash')
    is_paid = db.Column(db.Boolean, default=False)
    order = db.relationship('Order', back_populates='payment')

    def __init__(self, type='',  is_paid=False):
        self.type = type
        self.is_paid = is_paid

    def serialize(self):
        return {
            'id': self.id,
            'paid_at': self.paid_at,
            'is_paid': self.is_paid,
            'type': self.type,
        }

    def save(self):
        self.paid_at = datetime.now()
        db.session.add(self)
        return db.session.commit()