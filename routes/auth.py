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

        # Check if the username or email already exists
        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            flash('Username or email already exists', 'error')
            return redirect(url_for('auth.register'))

        # Create a new user
        new_user = User(username=username, email=email, is_owner=is_owner)
        new_user.set_password(password)

        # Commit to database with error handling
        try:
            db.session.add(new_user)
            db.session.commit()
            flash('User registered successfully!', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()  # Rollback in case of failure
            flash(f"Error creating user: {str(e)}", 'error')
            return redirect(url_for('auth.register'))

    return render_template('signup.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')

        # Check for missing credentials
        if not username or not password:
            flash('Please enter both username and password', 'danger')
            return render_template('login.html'), 400  # Bad Request

        # Ensure username comparison is case insensitive
        user = User.query.filter(db.func.lower(User.username) == db.func.lower(username)).first()


        # Validate user credentials
        if user is None or not user.check_password(password):
            flash('Invalid login credentials', 'danger')  # Changed to avoid revealing specifics
            return render_template('login.html'), 401  # Unauthorized

        # Login user
        login_user(user)
        flash(f'Welcome back, {user.username}!', 'success')

        # Redirect to the next page or home
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        else:
            return redirect(url_for('home'))
    else:
        return render_template('login.html')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    # Log out the user
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile', methods=['GET'])
@login_required
def profile():
    # Display the user's profile and boutiques
    user_boutiques = current_user.boutiques
    return render_template(
        'profile.html',
        username=current_user.username,
        email=current_user.email,
        is_owner=current_user.is_owner,
        user=current_user,
        bucket_list=current_user.bucket_list
    )

@auth_bp.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_new_password = request.form.get('confirm_new_password')

        # Validate form data
        errors = False
        if not current_password:
            flash('Please enter your current password.', 'danger')
            errors = True
        if not new_password:
            flash('Please enter a new password.', 'danger')
            errors = True
        if not confirm_new_password:
            flash('Please confirm your new password.', 'danger')
            errors = True
        if new_password != confirm_new_password:
            flash('Passwords must match.', 'danger')
            errors = True
        if new_password and len(new_password) < 8:
            flash('Password must be at least 8 characters long.', 'danger')
            errors = True
        if errors:
            return render_template('update_password.html'), 400  # Bad Request

        # Validate current password
        if not current_user.check_password(current_password):
            flash('Current password is incorrect.', 'danger')
            return render_template('update_password.html'), 401  # Unauthorized

        # Update password
        current_user.set_password(new_password)
        db.session.commit()
        flash('Your password has been updated successfully.', 'success')
        return redirect(url_for('auth.profile'))

    return render_template('update_password.html')
