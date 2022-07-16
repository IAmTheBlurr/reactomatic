""" ./reactomatic_bot.py """
from typing import Dict, List

from discord import Client as DiscordClient
from discord import Message, User

from pymongo import MongoClient

from connectors import Configuration


class ReactomaticBot(DiscordClient):
    def __init__(self, config: Configuration):
        super().__init__()
        self.__config = config
        self.client = MongoClient(config.database_uri)
        self.db = self.client['admin']

    @property
    def __leaderboard_commands(self) -> Dict:
        return {}

    @property
    def __request_commands(self) -> Dict:
        return {
            'album': self.__request_album,
            'band': self.__request_band,
            'song': self.__request_song
        }

    def __request_album(self, message: Message, args: List) -> None:
        return

    def __request_band(self, message: Message, args: List) -> None:
        return

    def __request_song(self, message: Message, args: List) -> None:
        return

    async def __show_bands(self, message: Message, _) -> None:
        bands = str([band['name'] for band in list(self.db['bands'].find({}))])
        await message.channel.send(str(bands))

    async def on_message(self, message: Message):
        # Ignore messages which don't start with the command prefix
        if not message.content.startswith(self.__config.command_prefix):
            return

        command_args = message.content.split(' ')
        command = command_args.pop(0)

        if command == '/request':
            # Ignore request command types which are not recognized
            if command_args[0] not in self.__request_commands.keys():
                return

            await self.__request_commands[command_args[0]](message, command_args)

        else:
            # Ignore commands which aren't registered in our available command list
            if command not in self.__leaderboard_commands.keys():
                return

            await self.__leaderboard_commands[command](message, command_args)

    @staticmethod
    async def on_ready():
        print(f'I am Raactomatic 9000.  I fight for the users.  Greetings program.')

    def transform_and_roll_out(self):
        self.run(self.__config.bot_token)
