from io import BytesIO

import discord
import requests
from PIL import Image, ImageEnhance, ImageFilter

client = discord.Client()


class Ops:

    """ Sending messages """

    async def send_image_to_chat(self, img, channel):
        img.save('./img.png')
        file = discord.File("img.png", filename="img.png")
        await channel.send("", file=file)

    async def send_message_to_chat(self, message, channel):
        await channel.send(message)

    """ Image management"""

    last_sent_image_url = "unset"

    def message_contains_image(self, message):
        return ops.message_contains_embed(message) or ops.message_contains_attachment(message)

    def message_contains_embed(self, message):
        return message.embeds;

    def message_contains_attachment(self, message):
        return message.attachments;

    def get_image_url_from_message(self, message):
        return message.embeds[0].url or message.attachments[0].url

    def get_image_from_url(self, image_url):
        return Image.open(BytesIO(requests.get(image_url).content))

    async def save_image_found_in_message(self, message):
        """ We may want to get this working on a per-channel basis """
        if ops.message_contains_image(message):
            ops.last_sent_image_url = ops.get_image_url_from_message(message)
        elif ops.last_sent_image_url == "unset":
            ops.last_sent_image_url = message.author.avatar_url

    """ Image filtering """

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

    """ Text commands """

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
    
    await ops.save_image_found_in_message(message)

    if message.content.startswith('..enhance'):
        img = ops.get_image_from_url(ops.last_sent_image_url)
        img = ops.apply_emboss(8, img)
        await ops.send_image_to_chat(img, message.channel)

    if message.content.startswith('..df'):
        img = ops.get_image_from_url(ops.last_sent_image_url)
        img = ops.apply_contrast(50, img)
        await ops.send_image_to_chat(img, message.channel)

    if message.content.startswith('..mock'):
        await ops.send_message_to_chat(ops.mock(message.content), message.channel)
        ...

client.run('NzYzNTM3MTU0NzAxMzkzOTIw.X35JYw.t3Lr-aHa6ccnPDVbh59KL1BXkwM')
