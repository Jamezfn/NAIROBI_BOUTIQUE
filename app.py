import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from routes.auth import auth_bp
from routes.boutiques import boutiques_bp
from routes.bucketlist import bucketlist_bp
from routes.items import items_bp
from models.user import db, User
from config import config  # Import your config dictionary


# Initialize extensions
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_name=None):
    app = Flask(__name__)

    # Load the configuration based on the environment
    if config_name is None:
        config_name = 'default'  # Use 'default' if no configuration name is provided
    
    app.config.from_object(config[config_name])  # Load the configuration

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

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
    # Get the configuration from the environment variable or default to 'development'
    config_name = os.getenv('FLASK_ENV', 'default')
    app = create_app(config_name)
    
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)
