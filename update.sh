#!/bin/sh

cd immunity-bot
ps -ef | grep "python3.8 ./immunity-bot.py" | grep -v grep | awk '{print $2}' | xargs kill
git pull
python3.8 ./immunity-bot.py &