from src.constantes.url_prefix import IMAGE_URL
from src.models.Database import db
from src.models.Product import Product


class Complement(Product):
    __tablename__ = 'complements'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    type_id = db.Column(db.Integer, db.ForeignKey('complement_types.id'))
    type = db.relationship('ComplementType', back_populates='complements', foreign_keys=[type_id])
    menus = db.relationship('Menu', back_populates='complements', secondary='menus_complements')
    __mapper_args__ = {
        'polymorphic_identity': 'complement',
    }

    def __init__(self, name, price, description, type_id, image=''):
        super().__init__(name, price, description, image)
        self.type_id = type_id

    def serialize(self):
        image = self.image if self.image is not None else 'burger.jpg'

        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'type': self.type.serialize(),
            'type_id': self.type_id,
            'slug': self.slug,
            'is_available': self.is_available,
            'is_featured': self.is_featured,
            'is_offer_of_the_day': self.is_offer_of_the_day,
            'is_popular': self.is_popular,
            'image': 'static/images/' + image,

        }

    def slugify(self, name):
        return name.lower().replace(' ', '-')

    def save(self):
        """
        Save the burger
        """
        db.session.add(self)
        db.session.commit()
