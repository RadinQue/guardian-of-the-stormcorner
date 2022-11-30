from datetime import datetime
import os
from enum import Enum

class LogCategory(Enum):
    BotLog = 1
    OpsLog = 2

class LogLevel(Enum):
    Log = 1
    Warning = 2
    Error = 3
    Fatal = 4

log_path = "logs"

log_filename = ""

def init():
    global log_filename

    timestamp = datetime.now().strftime("%Y.%m.%d-%H.%M.%S")
    log_filename = log_path + "/guardian_log_" + timestamp + ".log"

    try:
        logfile = open(log_filename, "x")
        logfile.write("Log file open, " + datetime.now().strftime("%Y/%m/%d %H:%M:%S") + "\n")
        logfile.close()
    except FileExistsError:
        logfile = open(log_filename, "a")
        logfile.write(datetime.now().strftime("%Y/%m/%d %H:%M:%S") + ": Attempted to create log file again.")
        logfile.close()

def log(message, category=LogCategory.OpsLog, level=LogLevel.Log):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        file = open(log_filename, "a")
        log_entry = timestamp + " - [" + category.name + ", " + level.name + "]: " + message + "\n"
        file.write(log_entry)
        file.close()
    except FileNotFoundError:
        init()
        log("Attemted to write to log file when it wasn't yet created", category=LogCategory.BotLog, level=LogLevel.Warning)
        log(message=message, category=category, level=level)

def log_array(lines = [], category=LogCategory.OpsLog, level=LogLevel.Log):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        file = open(log_filename, "a")
        log_entry = timestamp + " - [" + category.name + ", " + level.name + "]: "
        for line in lines:
            log_entry += line + "\n"

        file.write(log_entry)
        file.close()
    except FileNotFoundError:
        init()
        log("Attemted to write to log file when it wasn't yet created", category=LogCategory.BotLog, level=LogLevel.Warning)
        log(message=message, category=category, level=level)
     
