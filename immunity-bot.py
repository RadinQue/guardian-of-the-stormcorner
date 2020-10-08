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
    if message.content.startswith('..enhance'):
        if message.attachments:
            response = requests.get(message.attachments[0].url)
            img = Image.open(BytesIO(response.content))
            
            for i in range(8):
                img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
                
            img.save('./temp.png')
            file = discord.File("temp.png", filename="aaa.png")
            await message.channel.send("enhancing..", file=file)

client.run('NzYzNTM3MTU0NzAxMzkzOTIw.X35JYw.t3Lr-aHa6ccnPDVbh59KL1BXkwM')