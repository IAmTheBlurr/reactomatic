""" ./entities/attendee.py """
from discord import User

from connectors import Configuration, Database


class Attendee(object):
    def __init__(self, username: str, config: Configuration, user: User = None):
        self.__config = config
        self.__user = user
        self.username = username
        self.attending = []
        self.events = None
        self.attendees = None

        if config:
            self.events = Database(self.__config, 'events')
            self.attendees = Database(self.__config, 'attendees')

        if self.username and not self.__user:
            self.__populate_from_database()

    def __creation_payload(self) -> dict:
        return {
            'username': self.username,
            'attending': []
        }

    async def __populate_from_database(self):
        async with self.attendees:
            attendee_data = await self.attendees.find_one({'username': self.username})

            if not attendee_data:
                raise ValueError('Document for attendee by the name "{}" was not found in the attendee database'.format(self.username))

            self.username = attendee_data['username']
            self.attending = attendee_data['attending']

    async def attend(self, event_id: str):
        async with self.attendees:
            if not await self.attendees.find_one({'username': self.username}):
                payload = self.__creation_payload()
                payload['attending'].append(event_id)
                await self.attendees.insert(payload)
            else:
                await self.attendees.update({'username': self.username}, {'$addToSet': {'attending': event_id}})

            async with self.events:
                await self.events.update({'id': event_id}, {'$addToSet': {'attendees': self.username}})

            await self.notify('You are now set to attend the event: {}'.format(event_id))

    async def notify(self, message: str):
        await self.__user.create_dm()
        await self.__user.dm_channel.send(message)

    async def notify_of_cancellation(self, event_title: str):
        if not self.__user:
            raise ValueError('User object not defined, cannot notify "{}" of event titled "{}" being canceled'.format(self.username, event_title))

        await self.__user.create_dm()
        await self.__user.dm_channel.send('The event titled "{}" has been canceled by the host.  :\'('.format(event_title))

    async def show_attending(self):
        await self.__populate_from_database()
        await self.notify('You are set to attend the following events: {}'.format(self.attending))

    async def unattend(self, event_id: str):
        async with self.events:
            await self.events.update({'id': event_id}, {'$pull': {'attendees': str(self.username)}})

        await self.__user.create_dm()
        await self.__user.dm_channel.send('You have been removed from the attendance list for: {}'.format((event_id)))
