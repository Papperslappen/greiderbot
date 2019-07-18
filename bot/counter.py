from bot.command import command
from common.storage import redis
import logging
import sys

log = logging.getLogger("bot.counter")

class Counter:
    def __init__(self,name):
        self.name = name
        if(redis.hget("counter",name)):
            redis.hset("counter",name,0)

    def set(self,value):
        redis.hset("counter",self.name,int(value))

    def incr(self):
        return int(redis.hincrby("counter",self.name,1))

    def decr(self):
        return int(redis.hincrby("counter",self.name,-1))

    def value(self):
        return int(redis.hget("counter",self.name))


@command("set",attributes=["modonly"])
def set(args):
    args = args.split()
    if len(args) != 2:
        log.warning("malformed set command")
        return ""
    name = args[0]
    value = args[1]
    try:
        Counter(name).set(int(value))
    except:
        log.warning("Exception in setting counter: {} - {}".format(name,sys.exc_info()[0]))
    return "{} set to {}".format(name, value)


# v v v v move this to misc commands

kyckling_counter = Counter("kyckling")

@command("vinst",timeout = 60, attributes=["subonly"])
def win(args):
    value = kyckling_counter.incr()

    return "Winner winner chicken dinner! Kyckling hittills ikväll: {}".format(value)

@command("kyckling",timeout=10)
def kyckling(args):
    count = int(kyckling_counter.value())
    k = "kycklingmiddag"
    if(count <= 0):
        return "Det har inte blivit någon kyckling hittills idag"
    if int(count)>1:
        k = "kycklingmiddagar"
    return "Hittils idag har det bjudits på {} {}".format(count,k)
