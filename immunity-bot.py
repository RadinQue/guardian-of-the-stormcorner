import discord
import requests
from io import BytesIO
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

    

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('.df'):
        if message.attachments:
            response = requests.get(message.attachments[0].url)
            img = Image.open(BytesIO(response.content))
            img = img.filter(ImageEnhance.CONTRAST)
            for i in range(8):
                factor = i / 4.0
                img.enhance(factor).show("Sharpness %f" % factor)
            img.save('./temp.png')
            file = discord.File("temp.png", filename="aaa.png")
            await message.channel.send("temp.png", file=file)

client.run('NzYzNTM3MTU0NzAxMzkzOTIw.X35JYw.t3Lr-aHa6ccnPDVbh59KL1BXkwM')