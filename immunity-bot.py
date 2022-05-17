from ops import Ops
from messagereciever import MessageReciever
import discord

client = discord.Client()
ops = Ops()
msgreciever = MessageReciever()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    ops.interpret_message(message)

    await msgreciever.do_handle_message(message, ops)

    ops.cleanup_after_message(message)

try:
    client.run('')
except Exception as e:
    print(e)
    print("Can't connect to Discord servers!")
