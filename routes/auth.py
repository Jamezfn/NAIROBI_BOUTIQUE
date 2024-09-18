from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User, db

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        is_owner = data.get('is_owner', False) == 'on'

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already exists', 'error')
            return redirect(url_for('auth.register'))

        new_user = User(username=username, email=email, is_owner=is_owner)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('User registered successfully!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash('Invalid username or password', 'error')
            return redirect(url_for('auth.login'))

        login_user(user)
        flash(f'Welcome back, {user.username}!', 'success')
        return redirect(url_for('home'))

    return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    user_boutiques = current_user.boutiques
    return render_template(
        'profile.html',
        username=current_user.username,
        email=current_user.email,
        is_owner=current_user.is_owner,
        user=current_user,
        bucket_list=current_user.bucket_list
    )

@auth_bp.route('/update_password', methods=['PUT'])
@login_required
def update_password():
    new_password = request.form.get('new_password')

    if not new_password:
        flash('New password is required', 'error')
        return redirect(url_for('auth.profile'))

    current_user.set_password(new_password)
    db.session.commit()

    flash('Password updated successfully!', 'success')
    return redirect(url_for('auth.profile'))
