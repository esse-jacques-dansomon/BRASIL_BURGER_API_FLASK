from src.constantes.url_prefix import IMAGE_URL
from src.models.Database import db
from src.models.Product import Product

menus_complements = db.Table('menus_complements', db.metadata,
                             db.Column('menu_id', db.ForeignKey('menus.id')),
                             db.Column('complement_id', db.ForeignKey('complements.id'))
                             )


class Menu(Product):
    __tablename__ = 'menus'
    id = db.Column(db.Integer, db.ForeignKey('products.id'), primary_key=True)
    cook_time = db.Column(db.Integer, nullable=False)
    burger_id = db.Column(db.Integer, db.ForeignKey('burgers.id'))
    burger = db.relationship('Burger', backref='menus', foreign_keys=[burger_id])
    complements = db.relationship('Complement', back_populates='menus', secondary=menus_complements, lazy='dynamic')

    __mapper_args__ = {
        'polymorphic_identity': 'menu'
    }

    def __init__(self, name, price, description, cook_time, burger_id, image='menu.jpg'):
        super().__init__(name, price, description, image)
        self.cook_time = cook_time
        self.burger_id = burger_id

    def serialize(self):
        image = self.image if self.image is not None else 'burger.jpg'
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'product_type': self.product_type,
            'description': self.description,
            'burger': self.burger.serialize(),
            'complements': [complement.serialize() for complement in self.complements],
            'list_complements_id': [complement.id for complement in self.complements],
            'image': 'static/images/'+ image,
            'cook_time': self.cook_time,
            'burger_id': self.burger_id,
            'is_available': self.is_available,
            'is_featured': self.is_featured,
            'is_offer_of_the_day': self.is_offer_of_the_day,
            'is_popular': self.is_popular
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update_price(self):
        price = self.burger.price
        for complement in self.complements:
            price += complement.price
        self.price = price
        db.session.commit()
