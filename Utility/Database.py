import mysql.connector


class Database:

    def __init__(self):
        self.connection = None
        pass

    def connect(self, db_params: dict):
        try:
            connection = mysql.connector.connect(
                host=db_params.get("host"),
                database=db_params.get("database"),
                user=db_params.get("user"),
                password=db_params.get("password")
            )
            self.connection = connection
        except Exception as e:
            print(f"Failed to connect to MySQL server due to Error: {e}")
            raise e

    def test_connection(self):
        return self.connection.is_connected()

    @staticmethod
    def create_table(connection: mysql.connector.MySQLConnection, table_name: str, table_schema: str):
        if connection.is_connected():
            cursor = connection.cursor()
            # Create table
            cursor.execute(f"CREATE TABLE {table_name} ({table_schema})")
            print(f"Table {table_name} created successfully")
            cursor.close()
        else:
            print("No connection to MySQL server")
