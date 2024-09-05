from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from .user import User, db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    is_owner = data.get('is_owner', False)

    
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({'error': 'Username or email already exists'}), 400

    
    new_user = User(username=username, email=email, is_owner=is_owner)
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User registered successfully!'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user is None or not user.check_password(password):
        return jsonify({'error': 'Invalid username or password'}), 401

    login_user(user)
    return jsonify({'message': f'Welcome back, {user.username}!'}), 200

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    return jsonify({
        'username': current_user.username,
        'email': current_user.email,
        'is_owner': current_user.is_owner
    })

@auth_bp.route('/update_password', methods=['PUT'])
@login_required
def update_password():
    data = request.get_json()
    new_password = data.get('new_password')

    if not new_password:
        return jsonify({'error': 'New password is required'}), 400

    current_user.set_password(new_password)
    db.session.commit()

    return jsonify({'message': 'Password updated successfully!'}), 200

