import unittest
import json

from Utility.Database import Database


class MyTestCase(unittest.TestCase):

    #@unittest.skip("Not needed")
    def test_getConnection(self):
        configs = json.load(open('C:/Users/MV_2/Documents/GitHub/lMS-monte-carlo/.venv/config.json', 'r'))
        try:
            connection = Database.get_connection(configs.get('db_params'))
            self.assertTrue(connection.is_connected())
        except Exception as e:
            self.fail(f"Failed to connect to MySQL server: {e}")


if __name__ == '__main__':
    unittest.main()
