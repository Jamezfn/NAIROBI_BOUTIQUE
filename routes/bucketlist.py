from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from extensions import db
from models.user import User
from models.item import Item, BucketList

bucketlist_bp = Blueprint('bucketlist', __name__)

@bucketlist_bp.route('/add', methods=['POST'])
@login_required
def add_to_bucketlist():
    item_id = request.form.get('item_id')

    if not item_id:
        flash('Item ID is required', 'danger')
        return redirect(url_for('auth.profile'))

    # Convert item_id to integer and handle potential ValueError
    try:
        item_id = int(item_id)
    except ValueError:
        flash('Invalid Item ID', 'danger')
        return redirect(url_for('auth.profile'))

    item = Item.query.get(item_id)
    if not item:
        flash('Item not found', 'danger')
        return redirect(url_for('auth.profile'))

    existing_entry = BucketList.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    if existing_entry:
        flash('Item already in your bucket list', 'warning')
        return redirect(url_for('auth.profile'))

    new_entry = BucketList(user_id=current_user.id, item_id=item_id)
    db.session.add(new_entry)
    db.session.commit()

    flash('Item added to your bucket list!', 'success')
    return redirect(url_for('bucketlist.view_bucketlist'))

@bucketlist_bp.route('/list', methods=['GET'])
@login_required
def view_bucketlist():
    # Optimize query to retrieve all items in one call
    items = db.session.query(Item).join(BucketList, Item.id == BucketList.item_id)\
        .filter(BucketList.user_id == current_user.id).all()
    
    return render_template('bucket-list.html', items=items)

@bucketlist_bp.route('/remove/<int:item_id>', methods=['POST'])
@login_required
def remove_from_bucketlist(item_id):
    entry = BucketList.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    
    if not entry:
        flash('Item not found in your bucket list', 'danger')
        return redirect(url_for('bucketlist.view_bucketlist'))

    db.session.delete(entry)
    db.session.commit()

    flash('Item removed from your bucket list', 'success')
    return redirect(url_for('bucketlist.view_bucketlist')) 

