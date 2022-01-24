"""Initialize app."""
from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

import os


db = SQLAlchemy()
login_manager = LoginManager()


def template_render(item, template_name):
    return render_template(os.path.join(item, template_name))


def create_app():
    """Construct the core app object."""
    app = Flask(__name__, instance_relative_config=False)

    # Application Configuration
    app.config.update(TESTING=True,
                      DEBUG=True,
                      SECRET_KEY="104838b865614f38846c2a9f37a2d86d", #secret key
                      SQLALCHEMY_DATABASE_URI="sqlite:///daycare.db", # db name
                      SQLALCHEMY_ECHO=False,
                      SQLALCHEMY_TRACK_MODIFICATIONS=False
                      )

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        from app import home_routes, login_routes, profile_routes, main_routes, manager_routes

        app.register_blueprint(home_routes.home_bp)

        # Register Blueprints
        app.register_blueprint(login_routes.login_bp)
        app.register_blueprint(profile_routes.profile_bp)
        app.register_blueprint(main_routes.main_bp)
        app.register_blueprint(manager_routes.manager_bp)

        # Create Database Models)
        db.create_all()

        return app
