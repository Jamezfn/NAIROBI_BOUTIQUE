from extensions import db
from .user import User

class Boutique(db.Model):
    __tablename__ = 'boutique'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationship with Item
    items = db.relationship('Item', backref='boutique', lazy=True)

    def __repr__(self):
        return f'<Boutique(id={self.id}, name={self.name})>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'owner_id': self.owner_id
        }

class Item(db.Model):
    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    boutique_id = db.Column(db.Integer, db.ForeignKey('boutique.id'), nullable=False)

    def __repr__(self):
        return f'<Item(id={self.id}, name={self.name}, price={self.price})>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'boutique_id': self.boutique_id
        }

class BucketList(db.Model):
    __tablename__ = 'bucket_list'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    
    user = db.relationship('User', backref='bucket_list')
    item = db.relationship('Item', backref='in_bucket_list')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_id': self.item_id,
            'item_name': self.item.name,
            'item_description': self.item.description
        }
