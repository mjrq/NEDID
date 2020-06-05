from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap

#Globally accesible libraries
db = SQLAlchemy()
bootstrap = Bootstrap()

def create_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')

    # Initialize Plugins
    db.init_app(app)
    bootstrap.init_app(app)

    with app.app_context():
        # Include our Routes
        from . import routes
        db.create_all()  # Create the table

        # Register Blueprints

        return app