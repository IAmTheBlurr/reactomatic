import discord

from pymongo import MongoClient

from configurator import Configurator

client = discord.Client()
config = Configurator(r'C:\Development\Projects\PortalBot9000\experiments\portal-bot-experiment.json')

mongo_client = MongoClient(config.database_url, config.database_port)
portal_discord = mongo_client.portal_events
portal_events = portal_discord.events
prefix = config.command_prefix


async def record_new_event(payload):
    return portal_events.insert_one(payload)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    parsed = message.content.split(', ')
    command = parsed[0]
    event_type = parsed[1]
    event_name = parsed[2]

    if command == f'{prefix}create-event':
        await record_new_event({'name': event_name, 'type': event_type})
        await message.channel.send(f'Created event: {event_name}')

    if message.content.startswith(f'{prefix}show-events'):
        await message.channel.send('Here are the events coming up for the following fortnight')

client.run(config.bot_token)
