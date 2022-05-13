from datetime import datetime

from src.models.Database import db


class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float)
    status = db.Column(db.String(20), default='en cours')
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    client = db.relationship('Client', back_populates='orders', foreign_keys=[client_id])
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'), nullable=True)
    payment = db.relationship('Payment', back_populates='order', foreign_keys=[payment_id])
    order_items = db.relationship('OrderItem', back_populates='order', cascade="all, delete-orphan")
    more_information = db.Column(db.Text, nullable=True)
    #reference = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=datetime.utcnow)

    def __init__(self, customer_id, total, more_information):
        self.client_id = customer_id
        self.total = total,
        self.more_information = more_information
        self.status = 'En cours'
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

    def serialize(self):
        return {
            'id': self.id,
            'customer_id': self.client_id,
            'total': self.total,
            'status': self.status,
            'more_information': self.more_information,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'order_items': [order_item.serialize() for order_item in self.order_items],
            'client': self.client.serialize() if self.client else None,
            'payment': self.payment.serialize() if self.payment else None
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
