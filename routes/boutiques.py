from flask import Blueprint, request, render_template, redirect, url_for, flash
from models.boutique import db, Boutique

boutiques_bp = Blueprint('boutiques', __name__)

@boutiques_bp.route('/boutiques', methods=['GET', 'POST'])
def create_boutique():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description', '')
        location = request.form.get('location')
        owner_id = request.form.get('owner_id')

        # Validate input
        if not name or not location or not owner_id.isdigit():
            flash('Invalid input', 'error')
            return redirect(url_for('boutiques.create_boutique'))

        new_boutique = Boutique(
            name=name,
            description=description,
            location=location,
            owner_id=int(owner_id)
        )
        db.session.add(new_boutique)
        db.session.commit()
        flash('Boutique created successfully!', 'success')
        return redirect(url_for('boutiques.list_boutiques'))

    return render_template('create_boutique.html')

@boutiques_bp.route('/boutiques/<int:id>', methods=['GET'])
def get_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    return render_template('shop.html', boutique=boutique)

@boutiques_bp.route('/boutiques/<int:id>/edit', methods=['GET', 'POST'])
def update_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    if request.method == 'POST':
        boutique.name = request.form.get('name', boutique.name)
        boutique.description = request.form.get('description', boutique.description)
        boutique.location = request.form.get('location', boutique.location)

        db.session.commit()
        flash('Boutique updated successfully!', 'success')
        return redirect(url_for('boutiques.get_boutique', id=boutique.id))

    return render_template('edit_boutique.html', boutique=boutique)

@boutiques_bp.route('/boutiques/<int:id>/delete', methods=['POST'])
def delete_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    db.session.delete(boutique)
    db.session.commit()
    flash('Boutique deleted successfully!', 'success')
    return redirect(url_for('boutiques.list_boutiques'))

@boutiques_bp.route('/boutiques/list', methods=['GET'])
def list_boutiques():
    boutiques = Boutique.query.all()
    return render_template('index.html', boutiques=boutiques)
