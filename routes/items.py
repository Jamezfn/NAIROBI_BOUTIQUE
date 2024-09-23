from flask import Blueprint, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.item import Item, Boutique

items_bp = Blueprint('items', __name__)

@items_bp.route('/boutiques/<int:boutique_id>/items', methods=['POST'])
@login_required
def create_item(boutique_id):
    boutique = Boutique.query.get_or_404(boutique_id)

    if boutique.owner_id != current_user.id:
        flash('You are not authorized to add items to this boutique.', 'danger')
        return redirect(url_for('auth.profile'))

    name = request.form.get('name')
    price = request.form.get('price')

    if not name or not price:
        flash('Name and price are required.', 'danger')
        return redirect(url_for('boutiques.get_boutique', id=boutique_id))

    try:
        price_value = float(price)
        if price_value <= 0:
            raise ValueError
    except ValueError:
        flash('Invalid price. Please enter a number greater than 0.', 'danger')
        return redirect(url_for('boutiques.get_boutique', id=boutique_id))

    new_item = Item(
        name=name,
        price=price_value,
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

@items_bp.route('/items/<int:item_id>', methods=['GET'])
@login_required
def get_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())

@items_bp.route('/items/<int:item_id>', methods=['POST'])
@login_required
def update_item(item_id):
    item = Item.query.get_or_404(item_id)

    if item.boutique.owner_id != current_user.id:
        flash('You are not authorized to update this item.', 'danger')
        return redirect(url_for('auth.profile'))

    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description')

    if name:
        item.name = name

    if description:
        item.description = description

    if price:
        try:
            price_value = float(price)
            if price_value <= 0:
                raise ValueError
            item.price = price_value
        except ValueError:
            flash('Invalid price. Please enter a number greater than 0.', 'danger')
            return redirect(url_for('boutiques.get_boutique', id=item.boutique_id))

    db.session.commit()
    flash('Item updated successfully!', 'success')
    return redirect(url_for('boutiques.get_boutique', id=item.boutique_id))

@items_bp.route('/items/<int:item_id>/delete', methods=['POST'])
@login_required
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)

    if item.boutique.owner_id != current_user.id:
        flash('You are not authorized to delete this item.', 'danger')
        return redirect(url_for('auth.profile'))

    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('boutiques.get_boutique', id=item.boutique_id))
