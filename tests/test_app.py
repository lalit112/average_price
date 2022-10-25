import unittest
from unittest import mock
from db import database_connection
from application.app import create_app
from utils.config import TestConfig


class TestConnection(unittest.TestCase):
    connection = None

    def setUp(self) -> None:
        self. app = create_app(TestConfig)
        self.assertEqual(self.app.debug, False)

    def tearDown(self) -> None:
        pass

    @mock.patch.object(database_connection, 'create_connection')
    def test_get_average_price(self, mock_create_conn):
        with self.app.test_client() as client:
            sent = {'origin': "ABCDE", "destination":"XYZCD", "date_to":"2020-01-12", "date_from":"2020-01-15"}
            result = client.get(
                '/rates/?date_from=2020-01-12&date_to=2020-01-12&origin=ABCDE&destination=XYZCD',
            )
            result.return_value = [{"day":"2020-01-12", "average_price": "1289"}, {"day":"2020-01-13",
                                    "average_price": "4532"}, {"day":"2020-01-14", "average_price": "4321"}]
            mock_conn = mock.MagicMock()
            mock_create_conn.return_value = mock_conn
            mock_cursor = mock.MagicMock()
            mock_conn.cursor.return_value = mock_cursor
            mock_cursor.execute.asset_called_once_with("""SELECT day,ROUND (AVG(price)::numeric, 2) as average_price 
            from prices where orig_code= ABCDE and dest_code= XYZCD and day between 2020-01-12 and 2020-01-15 
            group by day,orig_code, dest_code HAVING COUNT(price) >=3""")
            mock_cursor.fetchall.return_value = (('2020-01-12', "1289"), ('2020-01-13', "4532"), ("2020-01-14", "4321"))
            self.assertEqual(result.return_value, [{"day":"2020-01-12", "average_price": "1289"}, {"day":"2020-01-13",
                                    "average_price": "4532"}, {"day":"2020-01-14", "average_price": "4321"}])


if __name__ == "__main__":
    unittest.main()
