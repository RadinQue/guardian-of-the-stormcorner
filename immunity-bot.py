from ops import Ops
import discord

client = discord.Client()
ops = Ops()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    ops.interpret_message(message)

    if message.content.startswith('..enhance'):
        await ops.do_enhance(message)

    if message.content.startswith('..df'):
        await ops.do_df(message)

    if message.content.startswith('..mock'):
        await ops.do_mock(message)

try:
    client.run('NzYzNTM3MTU0NzAxMzkzOTIw.X35JYw.t3Lr-aHa6ccnPDVbh59KL1BXkwM')
except Exception as e:
    print(e)
    print("Can't connect to Discord servers!")
