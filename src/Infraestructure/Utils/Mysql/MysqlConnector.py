import mysql.connector
import mysql.connector.locales.eng.client_error
from src.Infraestructure.Utils.Files.ConfiManagement.ConfigManagement import ConfigManagement


class MysqlConnector:
    def __init__(self):
        self._config = ConfigManagement().config('Mysql')

    def connect(self) -> mysql.connector.connect():
        return mysql.connector.connect(
            host=self._config['hostname'],
            user=self._config['user'],
            passwd=self._config['password'],
            database=self._config['database']
        )
