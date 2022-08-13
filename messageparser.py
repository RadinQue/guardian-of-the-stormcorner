from urlparser import URLParser
urlparser = URLParser()


class MessageParser:

    """ Parsing commands """

    def get_contents_from_command_message(self, message):
        try:
            return message.content[message.content.index(' '):len(message.content)]
        except Exception as e:
            return ""

    def get_int_from_command_message(self, message):
        try:
            return message.content[message.content.index(' ')+1:message.content.index(' ')+2]
        except Exception as e:
            return ""

    def get_hex_from_command_message(self, message):
        try:
            return message.content[message.content.index(' ') + 1 : message.content.index(' ') + 8]
        except Exception as e:
            return ""

    def get_image_url_from_message(self, message):
        attachments = message.embeds + message.attachments
        for val in attachments:
            return val.url

        retmessage = self.get_contents_from_command_message(message)
        if retmessage:
            return retmessage

        return "No image found"

    """ Message contains... """

    def message_contains_valid_link(self, message):
        return urlparser.validate_url(self.get_contents_from_command_message(message))

    def message_contains_valid_link_to_image(self, message):
        command_content = self.get_contents_from_command_message(message)
        return urlparser.url_points_to_image(command_content) and urlparser.validate_url(command_content)

    def message_contains_image(self, message):
        return message.embeds or message.attachments or self.message_contains_valid_link_to_image(message)
