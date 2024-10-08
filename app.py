import os
from flask import Flask, render_template, redirect, url_for, request
from extensions import db, login_manager
from flask_migrate import Migrate
from dotenv import load_dotenv  # Import to load environment variables from .env
from routes.auth import auth_bp
from routes.boutiques import boutiques_bp
from routes.bucketlist import bucketlist_bp
from routes.items import items_bp
from config import config  # Import your config dictionary

# Load environment variables from .env file
# This should be done before accessing any environment variables
load_dotenv()  # Added to load the .env file

# Initialize extensions
migrate = Migrate()

def create_app(config_name=None):
    app = Flask(__name__)

    # Load the configuration based on the environment
    if config_name is None:
        config_name = 'default'  # Use 'default' if no configuration name is provided

    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'warning'

    with app.app_context():
        from models.user import User
        from models.item import Item, Boutique, BucketList

    @login_manager.unauthorized_handler
    def unauthorized():
        # Redirect to the login page with `next` parameter
        return redirect(url_for('auth.login', next=request.url), code=303)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(boutiques_bp, url_prefix='/boutiques')
    app.register_blueprint(bucketlist_bp, url_prefix='/bucketlist')
    app.register_blueprint(items_bp, url_prefix='/items')

    # Home route
    @app.route('/')
    def home():
        return render_template('index.html')

    return app

if __name__ == '__main__':
    # Get the configuration from the environment variable or default to 'default'
    config_name = os.getenv('FLASK_ENV', 'default')

    # Create the Flask app with the appropriate configuration
    app = create_app(config_name)

    # Optionally create the database tables (for testing or simple use cases)
    # If you're using migrations, you don't need this; use flask db migrate/upgrade instead
    with app.app_context():
        if app.config['TESTING']:
            db.create_all()  # Only for testing if necessary

    # Run the app with debug mode depending on the environment
    app.run(debug=app.config['DEBUG'])

