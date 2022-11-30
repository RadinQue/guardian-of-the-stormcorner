from ops import Ops
from messagereciever import MessageReciever
import discord
import os
import pathlib
import sys

import logger

def get_datadir() -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """

    home = pathlib.Path().home()

    if sys.platform == "win32":
        return home / "AppData/Roaming"
    elif sys.platform.startswith('linux'): # recommended idiom for compatibility
        return home / ".local/share"
    elif sys.platform == "darwin":
        return home / "Library/Application Support"

# create program dir
my_datadir = get_datadir() / "immunity-bot"

try:
    my_datadir.mkdir(parents=True)
except FileExistsError:
    pass


# key path constants
# key_directory_path = os.path.normpath(os.getenv('APPDATA') + "/immunity-bot")
key_file_path = my_datadir / "key.txt"

print(key_file_path)

# API key to use when logging in
api_key = ''

# whether or not we have to create the key file
create_file = False

client = discord.Client(intents=discord.Intents.all())
ops = Ops()
msgreciever = MessageReciever()

@client.event
async def on_ready():
    # modifying global variables
    global login_success
    global waiting_for_server
    login_success = True
    waiting_for_server = False
    
    print('We have logged in as {0.user}'.format(client))
    logger.init()

    # if no key file was found and the API key worked, create the file
    if create_file:
        if not os.path.exists(my_datadir):
            os.makedirs(my_datadir)
            
        key_file = open(key_file_path, "w")
        key_file.write(api_key)
        key_file.close()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    ops.interpret_message(message)

    await msgreciever.do_handle_message(message, ops)

    ops.cleanup_after_message(message)

# declaring as 'y' so the while loop starts
reenter_prompt = 'y'
# when the login was successful the user intention will not matter
login_success = False
# the while loop won't do anything while waiting for the bot to respond
waiting_for_server = False

while reenter_prompt == 'y' or login_success:
    if waiting_for_server:
        continue

    if os.path.exists(key_file_path):
        key_file = open(key_file_path, "r")
        api_key = key_file.readline()
        key_file.close()
    else:
        # no API key file,
        create_file = True

        api_key = input("Provide API key: ")

    try:
        client.run(api_key)
        waiting_for_server = True
    except Exception as e:
        print(e)
        print("Can't connect to Discord servers!")
        login_success = False
        reenter_prompt = input("Try to re-enter API key? (y/n)")
