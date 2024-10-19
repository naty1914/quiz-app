from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from app.database import db
import os
from dotenv import load_dotenv

load_dotenv()
from app.models import User
login_manager = LoginManager()
migrate = Migrate()  

def create_app():
    """It creates and configures the Flask app."""
    app = Flask(__name__)
    
    app.config['SECRET_KEY'] =os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'True') == 'True'
   
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    login_manager.login_view = 'app.login'  
    from .app import app as app_blueprint
    app.register_blueprint(app_blueprint)
    
    return app

@login_manager.user_loader
def load_user(user_id):
    """It loads a user from the database."""
    return User.query.get(int(user_id))