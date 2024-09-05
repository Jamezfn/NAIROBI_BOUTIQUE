from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from .auth import auth_bp
from .boutiques import boutiques_bp
from .bucketlist import bucketlist_bp
from .user import db, User

app = Flask(__name__)

app.config['SECRET_KEY'] = '12345678'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(boutiques_bp, url_prefix='/boutiques')
app.register_blueprint(bucketlist_bp, url_prefix='/bucketlist')


@app.route('/')
def home():
    return "Welcome to Nairobi Boutique Hub!"

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)