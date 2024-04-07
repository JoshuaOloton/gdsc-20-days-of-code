from api import db

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date_published = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False)
    in_stock = db.Column(db.Boolean, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'date_published': self.date_published,
            'price': self.price,
            'in_stock': self.in_stock
        }

    def __repr__(self) -> str:
        return f'<Book {self.id} -> {self.name}>'
