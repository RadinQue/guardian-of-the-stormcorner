import time
from messageparser import MessageParser
from imagefilterer import ImageFilterer
from soundfilterer import SoundFilterer
from urlparser import URLParser
import discord
from discord import Message

messageparser = MessageParser()
imagefilterer = ImageFilterer()
soundfilterer = SoundFilterer()
urlparser = URLParser()

PRUNE_MESSAGE_HARD_LIMIT = 50

class Ops:

    last_sent_image_url = "unset"

    """ Sending messages """

    async def send_image_to_chat(self, img, channel):
        try:
            img.save('./img.png')
        except Exception as e:
            """ wand requires this """
            img.save(filename='./img.png')

        file = discord.File("img.png", filename="img.png")
        await channel.send("", file=file)

    async def send_file_to_chat(self, file_location, channel):
        file = discord.File(file_location)
        await channel.send("", file=file)

    async def send_audio_to_chat(self, channel):
        file = discord.File("sound.mp3", filename="sound.mp3")
        await channel.send("", file=file)

    async def send_message_to_chat(self, message, channel):
        await channel.send(message)

    async def send_message_to_chat_return(self, message, channel):
        return await channel.send(message)

    """ Receiving messages """

    def interpret_message(self, message):
        if messageparser.message_contains_image(message):
            self.last_sent_image_url = messageparser.get_image_url_from_message(
                message)

    def cleanup_after_message(self, message):
        soundfilterer.clean_all_temp_files()
        imagefilterer.clean_all_temp_files()

    """ Image commands """

    async def do_enhance(self, message):
        try:
            img = urlparser.get_image_object_from_url(self.last_sent_image_url)
            img = imagefilterer.apply_emboss(8, img)
            await self.send_image_to_chat(img, message.channel)
        except Exception as e:
            print(e)
            await self.send_message_to_chat("No image found / Processing error", message.channel)

    async def do_df(self, message):
        try:
            img = urlparser.get_image_object_from_url(self.last_sent_image_url)
            img = imagefilterer.apply_contrast(50, img)
            await self.send_image_to_chat(img, message.channel)
        except Exception as e:
            print(e)
            await self.send_message_to_chat("No image found / Processing error", message.channel)

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
            await self.send_message_to_chat("No image found / Processing error", message.channel)

    async def do_haah(self, message):
        try:
            img = urlparser.get_image_object_from_url(self.last_sent_image_url)
            img = imagefilterer.apply_haah(img)
            await self.send_image_to_chat(img, message.channel)
        except Exception as e:
            print(e)
            await self.send_message_to_chat("No image found / Processing error", message.channel)

    async def do_waaw(self, message):
        try:
            img = urlparser.get_image_object_from_url(self.last_sent_image_url)
            img = imagefilterer.apply_waaw(img)
            await self.send_image_to_chat(img, message.channel)
        except Exception as e:
            print(e)
            await self.send_message_to_chat("No image found / Processing error", message.channel)

    """ Audio commands """

    async def do_yoi(self, message):
        try:
            urlparser.save_audio_from_url(message.attachments[0].url)
            await soundfilterer.add_yoi()
            await self.send_audio_to_chat(message.channel)
        except Exception as e:
            print(e)
            await self.send_message_to_chat("No sound found / Processing error", message.channel)

    async def do_loud(self, message):
        try:
            urlparser.save_audio_from_url(message.attachments[0].url)
            await soundfilterer.max_distortion()
            await self.send_audio_to_chat(message.channel)
        except Exception as e:
            print(e)
            await self.send_message_to_chat("No sound found / Processing error", message.channel)

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

    """ Moderation commands """

    async def do_prune(self, message: Message):
        """ ..prune <amount> <sudo-command> """
        channel = message.channel

        parameters = message.content.split(" ", 2)
        amount = 0
        if len(parameters) >= 2:
            if parameters[1] == "MAX":
                amount = PRUNE_MESSAGE_HARD_LIMIT
            else:
                amount = int(parameters[1])

        force_overflow = False
        if len(parameters) >= 3:
            force_overflow = parameters[2] == "IKNOWWHATIAMDOING"

        if amount == 0:
            await self.send_message_to_chat("Prune explicitly requires the user to specify the amount of messages to be removed.", channel)
            await self.send_message_to_chat("If you want to bypass this limit, please provide the command a second argument: IKNOWWHATIAMDOING", channel)
            return

        message_count = 0
        if force_overflow:
            messages_to_delete = amount
        else:
            messages_to_delete = min(amount, PRUNE_MESSAGE_HARD_LIMIT)

        await message.delete()

        async for message in channel.history(limit=messages_to_delete):
            # unless the user explicitly wants to delete more messages,
            if not force_overflow:
                # double checking for both limits
                # we don't want to delete more than expected
                if message_count >= PRUNE_MESSAGE_HARD_LIMIT:
                    break

                if message_count >= amount:
                    break

            await message.delete()
            message_count = message_count + 1
            
        confirmation_message = "Deleted " + str(message_count) + " messages!"
        if not force_overflow and amount > PRUNE_MESSAGE_HARD_LIMIT:
            confirmation_message += " (Your specified amount hit the hard limit which is " + str(PRUNE_MESSAGE_HARD_LIMIT) + ")"
        
        self_destruct_message = await self.send_message_to_chat_return(confirmation_message, channel)
        time.sleep(5)
        await self_destruct_message.delete()

    """ One-off memes """

    async def do_tecc_tip(self, message):
        try:
            await self.send_message_to_chat("tip", message.channel)
            await self.send_file_to_chat("res/tecc-tip.png", message.channel)
        except Exception as e:
            print(e)
            await self.send_message_to_chat("Sorry chief, no tecc tip for you today", message.channel)
