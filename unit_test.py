
import unittest
from db_config import connect_db
import mysql.connector

class TestDatabase(unittest.TestCase):
    def test_connection_successful(self):
        """Test if database connection is established successfully."""
        conn = connect_db()
        self.assertIsNotNone(conn, "Failed to establish a connection to the database.")
        if conn:
            conn.close()

    def test_connection_object_type(self):
        """Test if the connection object returned is of correct type."""
        conn = connect_db()
        self.assertIsInstance(
            conn,
            mysql.connector.connection_cext.CMySQLConnection,
            "Connection object is not of type CMySQLConnection."
        )
        if conn:
            conn.close()


if __name__ == '__main__':
    unittest.main()
