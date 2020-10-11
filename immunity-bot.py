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

    async def send_message_to_chat(self, message, channel):
        await channel.send(message)

    def apply_contrast(self, contrast_amount, img):
        return ImageEnhance.Contrast(img).enhance(contrast_amount)

    def saturate(self, saturation_amount, img):
        return ImageEnhance.Color(img).enhance(saturation_amount)

    def apply_emboss(self, emboss_amount, img):
        i = 0
        while i < emboss_amount:
            img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
            i += 1

        return img

    def mock(self, message):
        formatted = message.split("..mock", 1)[1]
        ret = ""
        i = False
        for char in formatted:
            if i:
                ret += char.upper()
            else:
                ret += char.lower()

            if char != ' ':
                i = not i

        return ret


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

    if message.content.startswith('..mock'):
        await ops.send_message_to_chat(ops.mock(message.content), message.channel)
        ...


client.run('NzYzNTM3MTU0NzAxMzkzOTIw.X35JYw.t3Lr-aHa6ccnPDVbh59KL1BXkwM')
