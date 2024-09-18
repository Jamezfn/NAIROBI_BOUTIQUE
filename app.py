from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from routes.auth import auth_bp
from routes.boutiques import boutiques_bp
from routes.bucketlist import bucketlist_bp
from routes.items import items_bp
from models.user import db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = '12345678'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345678@localhost:5432/my_database_name'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(boutiques_bp, url_prefix='/boutiques')
app.register_blueprint(bucketlist_bp, url_prefix='/bucketlist')
app.register_blueprint(items_bp, url_prefix='/items')

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
