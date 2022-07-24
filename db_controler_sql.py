import constants
import sqlite3
import traceback

class DatabaseControllerSQL():
    def __init__(self):
        self._database_uri = constants.SQL_URI
        self._sql_cursor = None

    #EXECUTION - SQL#

    def _create_connection(self):
        try:
            connection = sqlite3.connect(self._database_uri, check_same_thread=False)
            
            self._sql_cursor = connection.cursor()

            return connection
        except sqlite3.Error:
            traceback.print_exc()

    def execute(self, command, parameters):
        self._sql_cursor.execute(command, parameters)

    def commit(self):
        self._sql_connection.commit()

    def create_db_if_not_exists(self):
        # Create table if it doesn't exist
        self.execute('''CREATE TABLE IF NOT EXISTS units(id INTEGER PRIMARY KEY, name TEXT NOT NULL, base_health, INT, min_attack INT, max_attack INT, min_initiative FLOAT, max_initiative FLOAT, price FLOAT)''')
        

    #CREATE - SQL#

    def create_actor(self, name, base_health, min_attack, max_attack, min_initiative, max_initiative, price):
        #INSERT OR IGNORE ignores the INSERT if it already exists (if the value we select for has to be unique, like a PRIMARY KEY)
        create_actor_sql = '''INSERT OR IGNORE INTO units(name, base_health, min_attack, max_attack, min_initiative, max_initiative, price) VALUES (?,?,?,?,?,?,?) '''
        self.execute(create_actor_sql, (name, base_health, min_attack, max_attack, min_initiative, max_initiative, price,))

    #RETRIEVE - SQL#

    def get_actor