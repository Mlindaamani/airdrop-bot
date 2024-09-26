
import mysql.connector
import os
from dotenv import load_dotenv


load_dotenv('.env')


def get_connection():
    return mysql.connector.connect(host=os.getenv('DATABASE_HOST'),
                                   user=os.getenv('DATABASE_USER'),
                                   password=os.getenv("DATABASE_PASSWORD"),
                                   database=os.getenv('DATABASE_NAME'))


class Database:
    """This class handles all the database operations"""
    def __init__(self, host=os.getenv('DATABASE_HOST'), user='root', password='', database='ebotdb'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def db_connection(self):
        """Establishes a connection to the database and returns a connection object"""
        try:
            self.connection = mysql.connector.connect(
                host=self.host, user=self.user, password=self.password, database=self.database)
            return self.connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def get_cursor(self):
        """Return a cursor object"""
        return self.db_connection().cursor(dictionary=True, buffered=True)

    def get_users(self):
        """Get all the users"""
        try:
            cursor = self.get_cursor()
            cursor.execute("SELECT * FROM users")
            cursor.close()
            return cursor.fetchall()
        except mysql.connector.Error as error:
            print(f'Error: {error}')

    def get_user_by_id(self, id):
        """Returns a user with a given ID"""
        try:
            cursor = self.get_cursor()
            cursor.execute(
                "SELECT * FROM users WHERE id = %(user_id)s", {'user_id': id})
            user = cursor.fetchone()
            return user if user else "User not found!"
        except mysql.connector.Error as err:
            print(f'Error: {err}')

# You can test this module here in the main function
def main():
    database = Database()
    print(database.get_user_by_id(1))
    print(get_connection())


if __name__ == '__main__':
    main()
