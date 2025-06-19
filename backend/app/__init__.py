import os
from flask import Flask
from .config import Config
from .extensions import db, jwt # Import jwt
from flask_cors import CORS

def create_app(config_class=Config):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_class)

    # Ensure instance folder exists
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    db_path = db_uri.split('sqlite:///')[1]
    db_dir = os.path.dirname(db_path)
    
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Initialize Flask extensions here
    db.init_app(app)
    jwt.init_app(app) # Initialize JWT

    # Register blueprints here
    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp) # Register the auth blueprint

    from .routes.admin import admin_bp 
    app.register_blueprint(admin_bp) 

    from .routes.user import user_bp 
    app.register_blueprint(user_bp) 

    return app
