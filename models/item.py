from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///boutiques.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Boutique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    location = db.Column(db.String(100), nullable=False)
    owner_id = db.Column(db.Integer, nullable=False)
    items = db.relationship('Item', backref='boutique', lazy=True)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(500), nullable=True)
    boutique_id = db.Column(db.Integer, db.ForeignKey('boutique.id'), nullable=False)

    def __repr__(self):
        return f'<Item {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'boutique_id': self.boutique_id
        }

with app.app_context():
    db.create_all()

@app.route('/boutiques/<int:boutique_id>/items', methods=['POST'])
def create_item(boutique_id):
    boutique = Boutique.query.get_or_404(boutique_id)
    data = request.get_json()

    new_item = Item(
        name=data['name'],
        price=data['price'],
        description=data.get('description', ''),
        boutique_id=boutique.id
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@app.route('/boutiques/<int:boutique_id>/items', methods=['GET'])
def get_items(boutique_id):
    boutique = Boutique.query.get_or_404(boutique_id)
    items = Item.query.filter_by(boutique_id=boutique.id).all()
    return jsonify([item.to_dict() for item in items])

@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict())

@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()

    item.name = data.get('name', item.name)
    item.price = data.get('price', item.price)
    item.description = data.get('description', item.description)

    db.session.commit()
    return jsonify(item.to_dict())

@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
