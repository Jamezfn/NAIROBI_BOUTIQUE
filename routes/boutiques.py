from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models.user import db, User

boutiques_bp = Blueprint('boutiques', __name__)

class Boutique(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(500))
    location = db.Column(db.String(150))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    owner = db.relationship('User', backref='boutiques')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'owner_id': self.owner_id,
            'owner': self.owner.username
        }


@boutiques_bp.route('/create', methods=['POST'])
@login_required
def create_boutique():
    if not current_user.is_owner:
        return jsonify({'error': 'Only boutique owners can create boutiques'}), 403
    
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    location = data.get('location')

    
    if not name:
        return jsonify({'error': 'Boutique name is required'}), 400

    new_boutique = Boutique(name=name, description=description, location=location, owner_id=current_user.id)
    
    db.session.add(new_boutique)
    db.session.commit()

    return jsonify(new_boutique.to_dict()), 201

@boutiques_bp.route('/list', methods=['GET'])
def list_boutiques():
    boutiques = Boutique.query.all()
    return jsonify([boutique.to_dict() for boutique in boutiques])

@boutiques_bp.route('/<int:boutique_id>', methods=['GET'])
def get_boutique(boutique_id):
    boutique = Boutique.query.get_or_404(boutique_id)
    return jsonify(boutique.to_dict())

@boutiques_bp.route('/<int:boutique_id>', methods=['PUT'])
@login_required
def update_boutique(boutique_id):
    boutique = Boutique.query.get_or_404(boutique_id)

    if boutique.owner_id != current_user.id:
        return jsonify({'error': 'You are not the owner of this boutique'}), 403

    data = request.get_json()
    boutique.name = data.get('name', boutique.name)
    boutique.description = data.get('description', boutique.description)
    boutique.location = data.get('location', boutique.location)
    
    db.session.commit()
    return jsonify(boutique.to_dict())

@boutiques_bp.route('/<int:boutique_id>', methods=['DELETE'])
@login_required
def delete_boutique(boutique_id):
    boutique = Boutique.query.get_or_404(boutique_id)

    if boutique.owner_id != current_user.id:
        return jsonify({'error': 'You are not the owner of this boutique'}), 403

    db.session.delete(boutique)
    db.session.commit()
    return jsonify({'message': 'Boutique deleted successfully'}), 200
