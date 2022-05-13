from src.constantes.url_prefix import IMAGE_URL
from src.models.Database import db
from src.models.Product import Product


class Burger(Product):
    """
    Class that represents a burger
    """
    __tablename__ = 'burgers'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    cook_time = db.Column(db.Integer, nullable=False)
    __mapper_args__ = {
        'polymorphic_identity': 'burger'
    }

    def __init__(self, name, price, description, cook_time, image='burger.jpg'):
        super().__init__(name, price, description)
        self.cook_time = cook_time
        self.image = image

    def serialize(self):
        """
        Serialize the burger
        """
        image = self.image if self.image is not None else 'burger.jpg'
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'image': 'static/images/'+image,
            'cook_time': self.cook_time,
            'product_type': self.product_type,
            'slug': self.slug,
            'is_available': self.is_available,
            'is_featured': self.is_featured,
            'is_offer_of_the_day': self.is_offer_of_the_day,
            'is_popular': self.is_popular

        }

    def save(self):
        """
        Save the burger
        """
        db.session.add(self)
        db.session.commit()
