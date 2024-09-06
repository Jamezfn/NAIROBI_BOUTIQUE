from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.user import db, User
from models.item import Item

bucketlist_bp = Blueprint('bucketlist', __name__)

class BucketList(db.Model):
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


@bucketlist_bp.route('/add', methods=['POST'])
@login_required
def add_to_bucketlist():
    data = request.get_json()
    item_id = data.get('item_id')
    
    
    if not item_id:
        return jsonify({'error': 'Item ID is required'}), 400
    
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    
    existing_entry = BucketList.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    if existing_entry:
        return jsonify({'error': 'Item already in your bucket list'}), 400
    
    new_entry = BucketList(user_id=current_user.id, item_id=item_id)
    db.session.add(new_entry)
    db.session.commit()

    return jsonify(new_entry.to_dict()), 201

@bucketlist_bp.route('/list', methods=['GET'])
@login_required
def view_bucketlist():
    bucket_list = BucketList.query.filter_by(user_id=current_user.id).all()
    return jsonify([entry.to_dict() for entry in bucket_list])

@bucketlist_bp.route('/remove/<int:item_id>', methods=['DELETE'])
@login_required
def remove_from_bucketlist(item_id):
    entry = BucketList.query.filter_by(user_id=current_user.id, item_id=item_id).first()
    
    if not entry:
        return jsonify({'error': 'Item not found in your bucket list'}), 404
    
    db.session.delete(entry)
    db.session.commit()
    
    return jsonify({'message': 'Item removed from bucket list'}), 200
