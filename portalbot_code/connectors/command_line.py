""" ./connectors/command_line.py """
import re


class CommandLine(object):
    def __init__(self, command_string: str):
        self.__searcher = re.compile('--[a-zA-Z].* ')
        self.__parse(command_string)

    def __parse(self, command: str) -> None:
        found_commands = re.search(self.__searcher, command)

        if found_commands:
            print('Blah')
