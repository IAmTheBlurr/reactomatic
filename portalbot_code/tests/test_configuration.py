import os

from connectors.configuration import Configuration


class TestConfigurator(object):
    def test_class_init_properties(self):
        config = Configuration(os.path.abspath(os.curdir + os.path.normpath('/files/good-config.json')))
        assert config.client_id == '01234'
        assert config.client_secret == '56789'
        assert config.command_prefix == '$'
        assert config.bot_token == 'abc'
        assert config.database_url == 'localhost'
        assert config.database_port == 27017

    def test_raised_exception_with_string_database_port(self):
        try:
            Configuration(os.path.abspath(os.curdir + os.path.normpath('/files/bad-config.json')))
        except ValueError as error:
            assert error.args[0] == 'The database port value must be an integer.  <class \'str\'> object encountered'
