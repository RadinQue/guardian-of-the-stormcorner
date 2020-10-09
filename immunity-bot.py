import discord
import requests
from io import BytesIO
from PIL import Image
from PIL import ImageFilter
from PIL import ImageEnhance
client = discord.Client()

def get_image_attachment_from_message(message):
    return Image.open(BytesIO(requests.get(message.attachments[0].url).content))

async def send_image_to_chat(img,channel):
    img.save('./img.png')
    file = discord.File("img.png", filename="img.png")
    await channel.send("", file=file)

def apply_contrast(contrast_amount,img):
    return ImageEnhance.Contrast(img).enhance(contrast_amount)

def saturate(saturation_amount,img):
    return ImageEnhance.Color(img).enhance(saturation_amount)

def apply_emboss(emboss_amount,img):
    for i in range(emboss_amount):
        img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.attachments:
        img = get_image_attachment_from_message(message);

        if message.content.startswith('..enhance'):
            img = apply_emboss(8,img);
            await send_image_to_chat(img,message.channel);

        if message.content.startswith('..df'):
            img = apply_contrast(50,img)
            await send_image_to_chat(img,message.channel);

client.run('NzYzNTM3MTU0NzAxMzkzOTIw.X35JYw.t3Lr-aHa6ccnPDVbh59KL1BXkwM')