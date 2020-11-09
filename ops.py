from messageparser import MessageParser
from imagefilterer import ImageFilterer
from urlparser import URLParser
import discord

messageparser = MessageParser()
imagefilterer = ImageFilterer()
urlparser = URLParser()

class Ops:

    last_sent_image_url = "unset"

    """ Sending messages """

    async def send_image_to_chat(self, img, channel):
        try:
            img.save('./img.png')
        except Exception as e:
            """ wand requires this """
            img.save(filename = './img.png')

        file = discord.File("img.png", filename="img.png")
        await channel.send("", file=file)

    async def send_message_to_chat(self, message, channel):
        await channel.send(message)

    """ Receiving messages """

    def interpret_message(self, message):
        if messageparser.message_contains_image(message):
            self.last_sent_image_url = messageparser.get_image_url_from_message(message)

    """ Image commands """

    async def do_enhance(self, message):
        try:
            img = urlparser.get_image_object_from_url(self.last_sent_image_url)
            img = imagefilterer.apply_emboss(8, img)
            await self.send_image_to_chat(img, message.channel)
        except Exception as e:
            print(e)
            await self.send_message_to_chat("No image found", message.channel)

    async def do_df(self, message):
        try:
            img = urlparser.get_image_object_from_url(self.last_sent_image_url)
            img = imagefilterer.apply_contrast(50, img)
            await self.send_image_to_chat(img, message.channel)
        except Exception as e:
            print(e)
            await self.send_message_to_chat("No image found", message.channel)

    async def do_magik(self, message):
        try:
            img = urlparser.get_image_object_from_url(self.last_sent_image_url)
            scale = messageparser.get_int_from_command_message(message)
            try:
               scale = int(scale)
            except ValueError:
                scale = 1
            img = imagefilterer.apply_magik(scale, img)
            await self.send_image_to_chat(img, message.channel)
        except Exception as e:
            print(e)
            await self.send_message_to_chat("No image found", message.channel)

    """ Text commands """

    async def do_mock(self, message):
        try:
            formatted = message.content.split("..mock", 1)[1]
            ret = ""
            i = False
            for char in formatted:
                if i:
                    ret += char.upper()
                else:
                    ret += char.lower()

                if char != ' ':
                    i = not i
            await self.send_message_to_chat(ret, message.channel)
        except Exception as e:
            print(e)
            await self.send_message_to_chat("Can't mock you if you're not saying anything", message.channel)