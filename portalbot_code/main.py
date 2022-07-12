""" ./main.py """
import os

from bots import CalendarTron5000
from connectors import Configuration


if __name__ == '__main__':
    config_file = os.path.abspath(os.curdir + os.path.normpath('/config.json'))
    config = Configuration(config_file)

    calendartron = CalendarTron5000(config)
    calendartron.transform_and_roll_out()
