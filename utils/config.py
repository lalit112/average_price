"""Flask configuration for development and testing environments"""

# Import modules
import os
from os import environ, path
from dotenv import load_dotenv

basedir = path.abspath(path.dirname(__file__))

# loading environment variables
load_dotenv(path.join(basedir, '.env'))


class DevConfig:
    """Set Flask config variables."""

    FLASK_ENV = os.environ.get('FLASK_ENV_DEV')
    TESTING = False
    SECRET_KEY = environ.get('SECRET_KEY')


class TestConfig:
    FLASK_ENV = os.environ.get('FLASK_ENV_TEST')
    TESTING = os.environ.get('TESTING')
    SECRET_KEY = environ.get('SECRET_KEY')

