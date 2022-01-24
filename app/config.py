"""Flask app configuration."""
from enum import Enum


class DevStatus(Enum):
    dev=1
    prod=2


class Config:
    """Set Flask configuration from environment variables."""

    SECRET_KEY = "104838b865614f38846c2a9f37a2d86d"

    GOOGLE_API_KEY="AIzaSyDPRTPnkhY1D2qJzrv4wQUlKrPVaDqLvpg"



    # Static Assets
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Flask-SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "sqlite:///daycare.db"
    SQLALCHEMY_ECHO = True

class DevConfig(Config):
    DEBUG = True
    SQL_DEBUG = True
    STATUS = DevStatus.dev

class ProdConfig(Config):
    DEBUG = True
    SQL_DEBUG = True
    STATUS = DevStatus.prod
