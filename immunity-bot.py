from io import BytesIO

import discord
import requests
from PIL import Image, ImageEnhance, ImageFilter

client = discord.Client()


class Ops:
    """Bot Image Operations"""

    def get_image_attachment_from_message(self, message):
        return Image.open(BytesIO(requests.get(message.attachments[0].url).content))


    async def send_image_to_chat(self, img, channel):
        img.save('./img.png')
        file = discord.File("img.png", filename="img.png")
        await channel.send("", file=file)

    def apply_contrast(self, contrast_amount, img):
        return ImageEnhance.Contrast(img).enhance(contrast_amount)

    def saturate(self, saturation_amount, img):
        return ImageEnhance.Color(img).enhance(saturation_amount)

    def apply_emboss(self, emboss_amount, img):
        for i in range(emboss_amount):
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
        return img


ops = Ops()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.attachments:
        img = ops.get_image_attachment_from_message(message)

        if message.content.startswith('..enhance'):
            img = ops.apply_emboss(8, img)
            await ops.send_image_to_chat(img, message.channel)

        if message.content.startswith('..df'):
            img = ops.apply_contrast(50, img)
            await ops.send_image_to_chat(img, message.channel)

client.run('NzYzNTM3MTU0NzAxMzkzOTIw.X35JYw.t3Lr-aHa6ccnPDVbh59KL1BXkwM')
