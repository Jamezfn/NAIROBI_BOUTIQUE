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

    def __repr__(self):
        return f'<Boutique {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'owner_id': self.owner_id
        }


with app.app_context():
    db.create_all()


@app.route('/boutiques', methods=['POST'])
def create_boutique():
    data = request.get_json()
    new_boutique = Boutique(
        name=data['name'],
        description=data.get('description', ''),
        location=data['location'],
        owner_id=data['owner_id']
    )
    db.session.add(new_boutique)
    db.session.commit()
    return jsonify(new_boutique.to_dict()), 201


@app.route('/boutiques', methods=['GET'])
def get_boutiques():
    boutiques = Boutique.query.all()
    return jsonify([boutique.to_dict() for boutique in boutiques])


@app.route('/boutiques/<int:id>', methods=['GET'])
def get_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    return jsonify(boutique.to_dict())


@app.route('/boutiques/<int:id>', methods=['PUT'])
def update_boutique(id):
    data = request.get_json()
    boutique = Boutique.query.get_or_404(id)

    boutique.name = data.get('name', boutique.name)
    boutique.description = data.get('description', boutique.description)
    boutique.location = data.get('location', boutique.location)

    db.session.commit()
    return jsonify(boutique.to_dict())


@app.route('/boutiques/<int:id>', methods=['DELETE'])
def delete_boutique(id):
    boutique = Boutique.query.get_or_404(id)
    db.session.delete(boutique)
    db.session.commit()
    return jsonify({'message': 'Boutique deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
