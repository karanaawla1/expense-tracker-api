from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.categories import categories_bp
    from app.routes.expenses import expenses_bp
    from app.routes.summary import summary_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(categories_bp, url_prefix="/api/categories")
    app.register_blueprint(expenses_bp, url_prefix="/api/expenses")
    app.register_blueprint(summary_bp, url_prefix="/api/summary")

    # Create all tables
    with app.app_context():
        db.create_all()

    return app
