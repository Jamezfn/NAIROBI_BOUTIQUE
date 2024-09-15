from flask import Blueprint, request, jsonify
from flask_login import login_required
from models.item import db, Item, Boutique

items_bp = Blueprint('items', __name__)

@items_bp.route('/boutiques/<int:boutique_id>/items', methods=['POST'])
@login_required
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

@items_bp.route('/boutiques/<int:boutique_id>/items', methods=['GET'])
@login_required
def get_items(boutique_id):
    boutique = Boutique.query.get_or_404(boutique_id)
    items = Item.query.filter_by(boutique_id=boutique.id).all()
    return jsonify([item.to_dict() for item in items])

@items_bp.route('/items/<int:id>', methods=['GET'])
@login_required
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify(item.to_dict())

@items_bp.route('/items/<int:id>', methods=['PUT'])
@login_required
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()

    item.name = data.get('name', item.name)
    item.price = data.get('price', item.price)
    item.description = data.get('description', item.description)

    db.session.commit()
    return jsonify(item.to_dict())

@items_bp.route('/items/<int:id>', methods=['DELETE'])
@login_required
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted'}), 200
