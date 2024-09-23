from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.item import Item, Boutique

boutiques_bp = Blueprint('boutiques', __name__)

@boutiques_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_boutique():                   
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        location = request.form.get('location')

        # Validate input
        if not name or not location:
            flash('Invalid input', 'error')
            return redirect(url_for('boutiques.create_boutique'))

        new_boutique = Boutique(
            name=name,
            description=description,
            location=location,
            owner_id=current_user.id  # Automatically get the logged-in user's ID
        )
        db.session.add(new_boutique)
        db.session.commit()
        flash('Boutique created successfully!', 'success')
        return redirect(url_for('auth.profile'))  # Redirect to profile after creating boutique

    return render_template('create_boutique.html')

@boutiques_bp.route('/<int:id>', methods=['GET'])
@login_required
def get_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    if boutique.owner_id != current_user.id:
        flash('You are not authorized to view this boutique', 'danger')
        return redirect(url_for('auth.profile'))

    return render_template('shop.html', boutique=boutique)

@boutiques_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def update_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    if boutique.owner_id != current_user.id:
        flash('You are not authorized to edit this boutique', 'danger')
        return redirect(url_for('auth.profile'))

    if request.method == 'POST':
        boutique.name = request.form.get('name', boutique.name)
        boutique.description = request.form.get('description', boutique.description)
        boutique.location = request.form.get('location', boutique.location)

        db.session.commit()
        flash('Boutique updated successfully!', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('edit_boutique.html', boutique=boutique)

@boutiques_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    if boutique.owner_id != current_user.id:
        flash('You are not authorized to delete this boutique', 'danger')
        return redirect(url_for('auth.profile'))

    db.session.delete(boutique)
    db.session.commit()
    flash('Boutique deleted successfully!', 'success')
    return redirect(url_for('auth.profile'))

@boutiques_bp.route('/list', methods=['GET'], endpoint='list')
def list_boutiques():
    boutiques = Boutique.query.all()
    return render_template('index.html', boutiques=boutiques)


# Add route to handle adding items to a boutique
@boutiques_bp.route('/<int:id>/items/add', methods=['POST'])
@login_required
def add_item(id):
    boutique = Boutique.query.get_or_404(id)
    if boutique.owner_id != current_user.id:
        flash('You are not authorized to add items to this boutique', 'danger')
        return redirect(url_for('auth.profile'))

    name = request.form.get('name')
    price = request.form.get('price')
    description = request.form.get('description', '')

    # Validate item inputs
    if not name or not price.isdigit():
        flash('Invalid item details', 'error')
        return redirect(url_for('auth.profile'))

    new_item = Item(
        name=name,
        price=float(price),
        description=description,
        boutique_id=boutique.id
    )
    db.session.add(new_item)
    db.session.commit()
    flash('Item added successfully!', 'success')
    return redirect(url_for('auth.profile'))
