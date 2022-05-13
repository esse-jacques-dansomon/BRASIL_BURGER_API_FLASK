from src.models.Database import db


class ComplementType(db.Model):
    __tablename__ = 'complement_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    complements = db.relationship('Complement', back_populates='type')
    slug = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, name, description='', image=''):
        self.name = name
        self.image = image
        self.description = description
        self.slug = self.slugify(name)


    def slugify(self, name):
        return name.lower().replace(' ', '-')

    def serialize(self):
        image = self.image if self.image is not None else 'boissons.jpg'

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image': 'static/images/' + image,
            'slug': self.slug
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()
