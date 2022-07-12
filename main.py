""" ./main.py """
import os

from reactomatic_bot import ReactomaticBot
from connectors import Configuration


if __name__ == '__main__':
    config_file = os.path.abspath(os.curdir + os.path.normpath('/config.json'))
    config = Configuration(config_file)

    reactomatic = ReactomaticBot(config)
    reactomatic.transform_and_roll_out()
