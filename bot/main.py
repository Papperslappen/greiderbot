import time
import datetime
import logging
import signal

import common.config as config
from bot.ircbot import IrcBot
import bot.misc_commands

log = logging.getLogger("main")
logging.basicConfig(level = logging.DEBUG)

if __name__ == "__main__":

    signal.signal(signal.SIGINT, signal.default_int_handler)

    cfg = config.readConfigFile()
    # channel, nickname, server, port=6667, password
    bot = IrcBot(cfg.get("Irc","channel"),
                 cfg.get("Irc","username"),
                 cfg.get("Irc","server"),
                 int(cfg.get("Irc","port")),
                 cfg.get("Irc","oauth"),
                 cfg.get("Irc","commandprefix"),
                 cfg.get("Irc","welcomemessage"))
    try:
        bot.start()
    except KeyboardInterrupt:
        log.info("Received KeyboardInterrupt, quitting")
    finally:
        log.info("quitting")
        bot.die()
