# immunity-bot

immunity bot aka. the guardian of the stormcorner is a python based discord bot we wrote so we can use the "magik" meme command whenever notsobot's offline. we added some of our own extra features along the way

as the bot was written for use only in our private server, it is **not** designed for use in multiple servers at once. **only run this on one server per api key**. we may change this later.

We bundled an ffmpeg.exe with the repo, up to you if you want to trust a random exe from github haha, feel free to use your own one though.

# Bot local run guide

This project currently runs on Python 3.8

**1: install the required dependencies with py -3 -m pip install:**

    py -3 -m pip install pillow
  
    py -3 -m pip install requests

    py -3 -m pip install pyo
    
    py -3 -m pip install wand
  
    py -3 -m pip install -U discord.py

    py -3 -m pip install wxpython
    
    py -3 -m pip install numpy==1.19.3

wxypython is optional: we don't use this but it stops pyo from complaining each launch

**2.a: install imagemagick (windows)**
	
https://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-on-windows

**2.b: install imagemagick (linux): enter to terminal**
	
	sudo apt install imagemagick
 
**3: go to immunity-bot.py line 27 and paste your api key into client.run('key here')**
 
**4: cd to the folder with immunity-bot.py in**

**5: enter to terminal**

    py -3 immunity-bot.py

# Some of the resources we used

discord.py documentation
https://github.com/Rapptz/discord.py

Minimal bot template
https://discordpy.readthedocs.io/en/latest/quickstart.html#a-minimal-bot

Pillow (Python Imaging Library) - check sidebar
https://pillow.readthedocs.io/en/stable/reference/ImageEnhance.html

Imagemagick's wand
https://docs.wand-py.org/en/0.6.3/

fun.py reference (yes we ripped it off)
https://github.com/NotSoSuper/NotSoBot/blob/master/mods/Fun.py

pyo documentation
http://ajaxsoundstudio.com/pyodoc/api/

Discord bot general guide
https://www.writebots.com/how-to-make-a-discord-bot/

Token guide
https://www.writebots.com/discord-bot-token/

Discord bot hosting basics
https://www.writebots.com/discord-bot-hosting/
