"""
This module is the entry point for application
"""

# Import modules
from flask import Flask
from utils.config import DevConfig
from get_price.average_price import avg_price


def create_app(config=DevConfig):
    """
    Factory function for creating flask app
    :return: app instance
    """
    app = Flask(__name__)
    app.config.from_object(config)
    app.register_blueprint(avg_price, url_prefix='/rates')
    return app
