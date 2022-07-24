import constants
import sqlite3
import traceback
from unit import Unit

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
        self.execute('''CREATE TABLE IF NOT EXISTS units(id INTEGER PRIMARY KEY, name TEXT NOT NULL, base_health, INT, min_attack INT, max_attack INT, min_initiative FLOAT, max_initiative FLOAT, ai_type TEXT, price FLOAT, game_version FLOAT)''')
        

    #SELECT - SQL#

    def select_where(self, select_columns, table_name, where, where_value):
        select_sql = "SELECT {} FROM {} WHERE {}=?".format(select_columns.lower(),table_name.lower(),where.lower())
        self.execute(select_sql, (where_value,))
        return self.cursor.fetchall()

    #CREATE - SQL#

    def save_unit(self, unit):
        #INSERT OR IGNORE ignores the INSERT if it already exists (if the value we select for has to be unique, like a PRIMARY KEY)
        save_unit_sql = '''INSERT OR IGNORE INTO units(name, base_health, min_attack, max_attack, min_initiative, max_initiative, ai_type, price, game_version) VALUES (?,?,?,?,?,?,?,?,?) '''
        self.execute(save_unit_sql, (unit._name, unit._base_health, unit._min_attack, unit._max_attack, unit._min_initiative, unit._max_initiative, unit._ai_type, unit.get_price(), unit.version))

    def get_unit_by_name(self, unit_name):
        fetched_unit = self.select_where("*","actors","name",unit_name)[0]
        unit = Unit(fetched_unit,)
        return unit