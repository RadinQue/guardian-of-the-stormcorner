# Bot local run guide on Windows

This project currently runs on Python 3.8

1: install the required dependencies with py -3 -m pip install:

    py -3 -m pip install pillow
  
    py -3 -m pip install requests

    py -3 -m pip install pyo
    
    py -3 -m pip install wand
  
    py -3 -m pip install -U discord.py

    py -3 -m pip install wxpython (optional: we don't use this but it stops pyo from complaining each launch)
    
    py -3 -m pip install numpy==1.19.3 (yes, that specific version)

2: install imagemagick (windows)
	
https://docs.wand-py.org/en/latest/guide/install.html#install-imagemagick-on-windows
 
3: go to immunity-bot.py line 27 and paste your api key into client.run('key here')
 
4: cd to the folder with immunity-bot.py in

5: enter to terminal

    py -3 immunity-bot.py

# Discord.py

discord.py documentation
https://github.com/Rapptz/discord.py

Minimal bot template
https://discordpy.readthedocs.io/en/latest/quickstart.html#a-minimal-bot

# Image manipulation

Pillow (Python Imaging Library) - check sidebar
https://pillow.readthedocs.io/en/stable/reference/ImageEnhance.html

Imagemagick's wand
https://docs.wand-py.org/en/0.6.3/

fun.py reference (yes we ripped it off)
https://github.com/NotSoSuper/NotSoBot/blob/master/mods/Fun.py

# Audio manipulation

pyo documentation
http://ajaxsoundstudio.com/pyodoc/api/

# More guides

Discord bot general guide
https://www.writebots.com/how-to-make-a-discord-bot/

Token guide
https://www.writebots.com/discord-bot-token/

Discord bot hosting basics
https://www.writebots.com/discord-bot-hosting/
