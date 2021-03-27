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

    if message.content.startswith('..en'):
        await ops.do_enhance(message)

    if message.content.startswith('..df'):
        await ops.do_df(message)

    if message.content.startswith('..mag'):
        await ops.do_magik(message)

    if message.content.startswith('..haah'):
        await ops.do_haah(message)

    if message.content.startswith('..waaw'):
        await ops.do_waaw(message)

    if message.content.startswith('..mock'):
        await ops.do_mock(message)

    if message.content.startswith('..tecc'):
        await ops.do_tecc_tip(message)

    if message.content.startswith('..yoi'):
        await ops.do_yoi(message)

    if message.content.startswith('..loud'):
        await ops.do_loud(message)

    ops.cleanup_after_message(message)

try:
    client.run('NzYzNTM3MTU0NzAxMzkzOTIw.X35JYw.t3Lr-aHa6ccnPDVbh59KL1BXkwM')
except Exception as e:
    print(e)
    print("Can't connect to Discord servers!")
