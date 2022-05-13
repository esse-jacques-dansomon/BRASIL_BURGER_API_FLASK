from src.models.Database import db


def get_all_by_client(client_id):
    return Address.query.filter_by(client_id=client_id).all()


class Address(db.Model):
    __tablename__ = 'addresses'
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(80), nullable=False)
    city = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(80), nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    client = db.relationship('Client', back_populates='addresses')

    def __init__(self, street, city, state, client_id):
        self.street = street
        self.city = city
        self.state = state
        self.client_id = client_id

    def serialize(self):
        return {
            'id': self.id,
            'street': self.street,
            'city': self.city,
            'state': self.state
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, data):
        if 'street' in data:
            self.street = data['street']
        if 'city' in data:
            self.city = data['city']
        if 'state' in data:
            self.state = data['state']
        db.session.commit()
