import configparser
import sys
import os
import logging

# TODO: Move config to redis

CONFIG_FILENAME = "greiderbot.cfg"

def genConfigFile():
    cfg = configparser.RawConfigParser()
    cfg.add_section("General")
    cfg.set("General","loglevel","DEBUG")
    cfg.add_section("Irc")
    cfg.set("Irc","username","<user>")
    cfg.set("Irc","oauth","<oauth>")
    cfg.set("Irc","server","irc.chat.twitch.tv")
    cfg.set("Irc","port",6667)
    cfg.set("Irc","channel","<channel>")
    cfg.set("Irc","commandprefix","!")
    cfg.set("Irc","welcomemessage","Hello!")
    cfg.add_section("Twitch")
    cfg.set("Twitch","clientid","<oauth>")
    cfg.set("Twitch","clientsecret","<oauth>")

    with open(CONFIG_FILENAME,"w") as f:
        cfg.write(f)


def readConfigFile():
    cfg = configparser.ConfigParser()
    if os.path.isfile(CONFIG_FILENAME):
        cfg.read(CONFIG_FILENAME)
        logging.info("Successfully read {}".format(CONFIG_FILENAME))
    else:
        print("Could not find any configuration, please edit {} and restart".format(CONFIG_FILENAME))
        _genConfigFile()
        sys.exit(1)
    return cfg
