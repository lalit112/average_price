"""
Module for handling database
"""

# Import modules
import os
from os import path
import psycopg2
from dotenv import load_dotenv
from psycopg2._psycopg import OperationalError  # pylint: disable=no-name-in-module

basedir = path.abspath(path.dirname(__file__))
# Loading environment variables
load_dotenv(path.join(basedir, '.env'))


def create_connection():
    """
        Function for handling creation of database connection
        :return: connection object or none
        """""
    try:
        conn = psycopg2.connect(
            host=os.environ['DB_HOST'],
            database=os.environ['DATABASE_NAME'],
            user=os.environ['DB_USERNAME'],
            password=os.environ['DB_PASSWORD'])
    except OperationalError:
        return None
    return conn
