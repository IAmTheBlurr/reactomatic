""" ./connectors/configuration.py """
import json
import os


class Configuration(object):
    def __init__(self, file_path: str):
        self.__database_port = 0
        self.__file_path = ''

        self.bot_token = ''
        self.client_id = ''
        self.client_secret = ''
        self.command_prefix = ''
        self.database_name = ''
        self.database_url = ''
        self.modules = []

        self.read_file(file_path)

    @property
    def database_port(self):
        return self.__database_port

    @database_port.setter
    def database_port(self, value: int):
        if not isinstance(value, int):
            raise ValueError(f'The database port value must be an integer.  {type(value)} object encountered')

        self.__database_port = value

    @property
    def file_path(self):
        return self.__file_path

    @file_path.setter
    def file_path(self, value: str):
        if not os.path.isfile(value):
            raise IOError('Value provided as a path to the file does not appear to point to a file.  Please provide a full path to a .json file.')

        self.__file_path = value

    def read_file(self, file_path: str) -> None:
        self.file_path = file_path

        with open(self.file_path) as config:
            data = config.read()

        content = json.loads(data)

        self.client_id = content['discord']['client_id'] if 'client_id' in content['discord'] else ''
        self.client_secret = content['discord']['client_secret'] if 'client_secret' in content['discord']else ''
        self.command_prefix = content['discord']['command_prefix'] if 'command_prefix' in content['discord'] else ''
        self.bot_token = content['discord']['bot_token'] if 'bot_token' in content['discord'] else ''
        self.database_name = content['database']['name'] if 'port' in content['database'] else ''
        self.database_port = content['database']['port'] if 'port' in content['database'] else 0
        self.database_url = content['database']['address'] if 'address' in content['database'] else ''
