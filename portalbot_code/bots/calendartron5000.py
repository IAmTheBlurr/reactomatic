""" ./entities/calendartron5000.py """
from discord import Client as DiscordClient
from discord import Message, User

from connectors import Configuration, Database
from entities import Attendee, Event


class CalendarTron5000(DiscordClient):
    def __init__(self, config: Configuration):
        super().__init__()
        self.__config = config
        self.events = Database(self.__config, 'events')
        self.attendees = Database(self.__config, 'attendees')
        self.hosts = Database(self.__config, 'hosts')

    @property
    def __available_commands(self) -> dict:
        prefix = self.__config.command_prefix
        return {
            f'{prefix}attend-event': self.__attend_event,
            f'{prefix}cancel-event': self.__cancel_event,
            f'{prefix}create-event': self.__create_event,
            f'{prefix}events-attending': self.__events_attending,
            f'{prefix}events-hosting': self.__events_hosting,
            f'{prefix}show-event': self.__show_event,
            f'{prefix}show-events': self.__show_events,
            f'{prefix}update-event': self.__update_event,
            f'{prefix}unattend-event': self.__unattend_event,
        }

    async def __attend_event(self, message: Message, args):
        attendee = Attendee(str(message.author), self.__config, user=message.author)
        await attendee.attend(args[0])

    async def __create_event(self, message: Message, args):
        payload = {
            'title': args[0],
            'type': args[1],
        }
        new_event = Event(self.__config, payload=payload)
        await new_event.create()
        await message.channel.send(f'Created event: {new_event.title}')

    async def __cancel_event(self, _, args):
        event = Event(self.__config, args[0], database=self.events)

        for attendee_name in event.attendees:
            await Attendee(attendee_name, self.__config).notify_of_cancellation(event.title)

        await event.cancel()

    async def __events_attending(self, message: Message, _):
        attendee = Attendee(str(message.author), config=self.__config, user=message.author)
        await attendee.show_attending()

    async def __events_hosting(self, message: Message, args):
        return

    async def __show_event(self, message: Message, args):
        async with self.events:
            event = await self.events.find_one({'id': args[0]})
            direct_message = f'Here is the info for Event {event["id"]}\n\r'
            direct_message += f'Title: {event["title"]}\n'
            direct_message += f'Type: {event["type"]}\n'

            await message.author.create_dm()
            await message.author.dm_channel.send(direct_message)

    async def __show_events(self, message: Message, _):
        async with self.events:
            events = await self.events.find({})
            events_message = f'Here are the events coming up for the following fortnight \n\r'

            for event in events:
                events_message += f'ID: {event["id"]}\n'
                events_message += f'Title: {event["title"]}\n'
                events_message += f'Type: {event["type"]}\n'
                events_message += f'\n'

            await message.author.create_dm()
            await message.author.dm_channel.send(events_message)

    async def __unattend_event(self, message: Message, args):
        attendee = Attendee(str(message.author), self.__config, user=message.author)
        await attendee.unattend(args[0])

    async def __update_event(self, message: Message, *args):
        return

    async def on_message(self, message: Message):
        # Ignore messages which don't start with the command prefix
        if not message.content.startswith(self.__config.command_prefix):
            return

        command_args = message.content.split(' ')
        command = command_args.pop(0)

        # Ignore commands which aren't registered in our available command list
        if command not in self.__available_commands.keys():
            return

        await self.__available_commands[command](message, command_args)

    @staticmethod
    async def on_ready():
        print(f'I am CalendarTron.  I fight for the users.  Never fear, I is here.')

    def transform_and_roll_out(self):
        self.run(self.__config.bot_token)
