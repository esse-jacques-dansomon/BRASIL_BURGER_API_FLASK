from src.models.Database import db


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer)
    price = db.Column(db.Float)
    total = db.Column(db.Float)
    order = db.relationship('Order', back_populates='order_items', foreign_keys=[order_id])
    product = db.relationship('Product', back_populates='order_items', foreign_keys=[product_id])

    def __init__(self, order_id, product_id, quantity, price):
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.price = price
        self.total = price*quantity

    def serialize(self):
        return {
            'id': self.id,
            'quantity': self.quantity,
            'price': self.price,
            'total': self.total,
            'product_id': self.product_id,
            'product': self.product.serialize()

        }
