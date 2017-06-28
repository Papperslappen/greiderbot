from bot.command import command
from common.storage import redis
import logging

log = logging.getLogger("counter")

@command("set",attributes=["modonly"])
def set(args):
    args = args.split()
    if len(args) != 2:
        log.INFO("malformed set command")
