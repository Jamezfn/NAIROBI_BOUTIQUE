from flask import Blueprint, request, jsonify
from models.boutique import db, Boutique

boutiques_bp = Blueprint('boutiques', __name__)

@boutiques_bp.route('/boutiques', methods=['POST'])
def create_boutique():
    data = request.get_json()

    # Validate input
    if not data.get('name') or not data.get('location') or not isinstance(data.get('owner_id'), int):
        return jsonify({'error': 'Invalid input'}), 400

    new_boutique = Boutique(
        name=data['name'],
        description=data.get('description', ''),
        location=data['location'],
        owner_id=data['owner_id']
    )
    db.session.add(new_boutique)
    db.session.commit()
    return jsonify(new_boutique.to_dict()), 201

@boutiques_bp.route('/boutiques', methods=['GET'])
def get_boutiques():
    boutiques = Boutique.query.all()
    return jsonify([boutique.to_dict() for boutique in boutiques])

@boutiques_bp.route('/boutiques/<int:id>', methods=['GET'])
def get_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    return jsonify(boutique.to_dict())

@boutiques_bp.route('/boutiques/<int:id>', methods=['PUT'])
def update_boutique(id):
    data = request.get_json()
    boutique = Boutique.query.get_or_404(id)

    boutique.name = data.get('name', boutique.name)
    boutique.description = data.get('description', boutique.description)
    boutique.location = data.get('location', boutique.location)

    db.session.commit()
    return jsonify(boutique.to_dict())

@boutiques_bp.route('/boutiques/<int:id>', methods=['DELETE'])
def delete_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    db.session.delete(boutique)
    db.session.commit()
    return jsonify({'message': 'Boutique deleted'}), 200

@boutiques_bp.route('/list', methods=['GET'])
def list_boutiques():
    boutiques = Boutique.query.all()
    return jsonify([boutique.to_dict() for boutique in boutiques])
