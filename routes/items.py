from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from models.item import db, Item, Boutique

items_bp = Blueprint('items', __name__)

@items_bp.route('/boutiques/<int:boutique_id>/items', methods=['POST'])
@login_required
def create_item(boutique_id):
    boutique = Boutique.query.get_or_404(boutique_id)

    if boutique.owner_id != current_user.id:
        return jsonify({'error': 'Unauthorized action'}), 403

    name = request.form.get('name')
    price = request.form.get('price')

    
    if not name or not price or not price.isdigit() or float(price) <= 0:
        flash('Invalid input. Please ensure all fields are correctly filled.', 'error')
        return redirect(url_for('boutiques.get_boutique', id=boutique_id))

    new_item = Item(
        name=name,
        price=float(price),
        description=request.form.get('description', ''),
        boutique_id=boutique.id
    )
    db.session.add(new_item)
    db.session.commit()
    flash('Item created successfully!', 'success')
    return redirect(url_for('boutiques.get_boutique', id=boutique_id))

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

@items_bp.route('/items/<int:id>', methods=['POST'])
@login_required
def update_item(id):
    item = Item.query.get_or_404(id)

    if item.boutique.owner_id != current_user.id:
        return jsonify({'error': 'Unauthorized action'}), 403

    item.name = request.form.get('name', item.name)
    item.price = request.form.get('price', item.price)
    item.description = request.form.get('description', item.description)

    try:
        item.price = float(item.price)
    except ValueError:
        flash('Invalid price. Must be a number.', 'error')
        return redirect(url_for('boutiques.get_boutique', id=item.boutique_id))

    if item.price <= 0:
        flash('Price must be greater than 0.', 'error')
        return redirect(url_for('boutiques.get_boutique', id=item.boutique_id))

    db.session.commit()
    flash('Item updated successfully!', 'success')
    return redirect(url_for('boutiques.get_boutique', id=item.boutique_id))

@items_bp.route('/items/<int:id>/delete', methods=['POST'])
@login_required
def delete_item(id):
    item = Item.query.get_or_404(id)

    if item.boutique.owner_id != current_user.id:
        return jsonify({'error': 'Unauthorized action'}), 403

    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('boutiques.get_boutique', id=item.boutique_id))
