import os
import unittest
from os import path
from unittest import mock

import psycopg2

from db import database_connection
from utils.config import TestConfig
from dotenv import load_dotenv
from application.app import create_app
from psycopg2._psycopg import OperationalError

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class TestConnection(unittest.TestCase):
    connection = None

    def setUp(self) -> None:
        self.config = {"host": os.environ['DB_HOST'],
                  "database": os.environ['DATABASE_NAME'],
                  "user": os.environ['DB_USERNAME'],
                  "password": os.environ['DB_PASSWORD']}
        app = create_app(TestConfig)
        self.app = app.test_client()
        self.assertEqual(app.debug, False)
        self.connection = psycopg2.connect(**self.config)

    def tearDown(self) -> None:
        if self.connection is not None:
            self.connection.close()

    def test_connection(self):
        self.assertTrue(self.connection, not None)

    @mock.patch.object(database_connection, 'create_connection')
    def test_connection_error(self, mock_conn):
        mock_conn.side_effect = OperationalError
        self.assertRaises(OperationalError, mock_conn)


if __name__ == "__main__":
    unittest.main()
