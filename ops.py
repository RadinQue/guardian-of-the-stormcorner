import time
import random
from messageparser import MessageParser
from imagefilterer import ImageFilterer
from soundfilterer import SoundFilterer
from urlparser import URLParser
import discord
from discord import Message
from PIL import Image
import json
import os

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

    async def do_skrillex(self, message):
        try:
            img = urlparser.get_image_object_from_url(self.last_sent_image_url)
            color = messageparser.get_hex_from_command_message(message)
            img = imagefilterer.apply_skrillex_feet(img, color)
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

    """ Misc """

    async def do_loudwarningcheck(self, message):
        try:
            if message.author.name == 'Cherry412':
                extensionsToCheck = ['.mp3', '.wav', '.mp4']
                self.potentiallyLoudFound=False

                if any(ext in message.content for ext in extensionsToCheck):
                    self.potentiallyLoudFound=True

                for att in message.attachments:
                    if any(ext in att.filename for ext in extensionsToCheck):
                        self.potentiallyLoudFound=True
                
                if self.potentiallyLoudFound:
                    print("potentially loud media by cherry detected")
                    await self.send_message_to_chat(":warning: Potentially loud media sent by Cherry412 - check your volume levels before pressing play!! :warning: ", message.channel)
        except Exception as e:
            print(e)

    async def do_heads_or_tails(self, message):
        result = bool(random.getrandbits(1))
        await self.send_message_to_chat("Flipping coin...", message.channel)
        time.sleep(1)
        result_msg = ""
        if result:
            result_msg = "Heads!"
        else:
            result_msg = "Tails!"
        
        await self.send_message_to_chat(result_msg, message.channel)

    ## Overlay command
    ## Takes the image from the message and a keyword.
    ## Looks for a previously saved image and overlays that with the image in the message
    #  @param message The message from the user
    async def do_overlay(self, message):
        overlay_obj = OverlayCommand(self.last_sent_image_url)

        parameters = message.content.split(" ", 2)
        # work out the command
        # if the params list is only 2 that means it's ..overlay 'keyword'
        if len(parameters) == 2:
            keyword = parameters[1]
            ret_img, error_msg = await overlay_obj.do_overlay(keyword)

            if error_msg == "":
                await self.send_image_to_chat(ret_img, message.channel)
            else:
                await self.send_message_to_chat(error_msg, message.channel)

            return

        intent = parameters[1]
        keyword = parameters[2]

        if intent == "" or keyword == "":
            await self.send_message_to_chat("Invalid arguments.\n..overlay <intent> <keyword> OR ..overlay <keyword>", message.channel)

        ret_msg = ""

        if intent == "add":
            # ..overlay add 'keyword'
            ret_msg = await overlay_obj.add_overlay(keyword)
        elif intent == "remove" or intent == "delete":
            # overlay remove 'keyword'
            ret_msg = await overlay_obj.remove_overlay(keyword)

        if ret_msg != "":
            await self.send_message_to_chat(ret_msg, message.channel)

        del overlay_obj


class OverlayCommand:
    image_url = "None"

    overlays_database = None

    def __init__(self, url):
        self.overlays_database = json.load(open("res/overlay/database.json"))
        self.image_url = url

    async def add_overlay(self, keyword):
        # check if keyword isn't already added
        try:
            image = urlparser.get_image_object_from_url(self.image_url)

            if self.search_resource(self.overlays_database, keyword) != None:
                return "Keyword '" + keyword + "' is already an existing keyword.\nTo delete it, type '..overlay delete " + keyword + "'."
            
            extension = urlparser.get_extension_from_url(self.image_url)

            try:
                image.save("res/overlay/" + keyword + extension)
            except Exception as e:
                print(e)
                return "Could not save the image."
        except:
            return "Couldn't get image object."
        
        new_data = {"keyword": keyword,
                    "resource": keyword + extension}

        self.write_json(new_data)
        return "Keyword: '" + keyword + "' was added an associated with '" + keyword + extension + "'"

    async def remove_overlay(self, keyword):
        if self.search_resource(self.overlays_database, keyword) == None:
            return "Couldn't find the provided keyword.\nTo add it, type '..overlay add '" + keyword + "' and provide the image to associate it with!"

        filename = self.search_resource(self.overlays_database, keyword)
        self.remove_json_obj(keyword)
        os.remove("res/overlay/" + filename)
        return "Successfully removed '" + keyword + "'."

    async def do_overlay(self, keyword):
        if self.search_resource(self.overlays_database, keyword) == None:
            return None, "Couldn't find the provided keyword.\nTo add it, type '..overlay add '" + keyword + "' and provide the image to associate it with!"

        try:
            image = urlparser.get_image_object_from_url(self.image_url)
            
            filename = self.search_resource(self.overlays_database, keyword)
            overlay = Image.open("res/overlay/" + filename)
            filter_result = imagefilterer.overlay_images(image, overlay)
        except:
            return None, "Couldn't get image object."

        return filter_result, ""

    """ Helper Functions """

    def search_resource(self, jsondata, keyword):
        for keyval in jsondata['overlays']:
            if keyword.lower() == keyval['keyword'].lower():
                return keyval['resource']

    def write_json(self, data, filename='res/overlay/database.json'):
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data["overlays"].append(data)
            file.seek(0)
            json.dump(file_data, file, indent=4)
            # update the parsed python object
            self.overlays_database = file_data

    def remove_json_obj(self, keyword, filename='res/overlay/database.json'):
        for i in range(len(self.overlays_database["overlays"])):
            print("keyword: ", self.overlays_database["overlays"][i]["keyword"])
            if self.overlays_database["overlays"][i]["keyword"] == keyword:
                self.overlays_database["overlays"].pop(i)
                break

        open(filename, 'w').write(json.dumps(self.overlays_database, sort_keys=True, indent=4, separators=(',', ': ')))