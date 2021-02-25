import configparser
import os


class ConfigManagement:
    def __init__(self):
        self._config_parser = configparser.ConfigParser()
        self._config = None
        self.__init()

    def __init(self):
        self._config_parser.read(f'{os.getcwd()}\\config.ini')
        self._config = self._config_parser

    def config(self, block: str):
        return self._config[block]
