from src.models.Database import db
from src.services.lib import make_slug


class Product(db.Model):
    """
    Product class
    """
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.String(250), nullable=True)
    is_available = db.Column(db.Boolean, nullable=False, default=True)
    is_featured = db.Column(db.Boolean, nullable=False, default=False)
    is_offer_of_the_day = db.Column(db.Boolean, nullable=False, default=False)
    is_popular = db.Column(db.Boolean, nullable=False, default=False)
    slug = db.Column(db.String(80), nullable=False)
    order_items = db.relationship('OrderItem', back_populates='product', cascade='all, delete-orphan', lazy=True)
    product_type = db.Column(db.String(50))
    __mapper_args__ = {
        'polymorphic_identity': 'Product',
        'polymorphic_on': product_type
    }

    def __init__(self, name, price, description, image='burger.jpg'):
        if Product.query.filter_by(name=name).first() is not None:
            name = name + '-copy'
        self.name = name
        self.price = price
        self.description = description
        self.slug = make_slug(name)
        self.image = image
        self.is_available = True

    def serialize(self):
        image = self.image if self.image is not None else 'burger.jpg'
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'image': 'static/images/' + image,
            'product_type': self.product_type,
            'slug': self.slug,
            'is_available': self.is_available,
            'is_featured': self.is_featured,
            'is_offer_of_the_day': self.is_offer_of_the_day,
            'is_popular': self.is_popular

        }

    def update_product(self, data):
        if data is not None or data != {}:
            if 'name' in data:
                self.name = data['name']
                self.slug = make_slug(data['name'])
            if 'price' in data:
                self.price = data['price']
            if 'description' in data:
                self.description = data['description']
            if 'image' in data:
                self.image = data['image']
            if 'is_available' in data:
                self.is_available = data['is_available']

    def update(self):
        db.session.commit()
