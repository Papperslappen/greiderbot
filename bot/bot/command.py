import time
import logging
from enum import Enum

log = logging.getLogger("command")

_commands = {}

class ResultType(Enum):
    VALUE = 1
    TIMEOUT = 2
    EMPTY = 3

class CommandResult:
    def __init__(self):
        self.value = ""
        self.type = ResultType.EMPTY

def emptyResult():
    return CommandResult()

def successResult(value):
    c = CommandResult()
    c.value = value
    c.type = ResultType.VALUE
    return c

def timeoutResult(timeleft):
    c = CommandResult()
    c.type = ResultType.TIMEOUT
    return c

class Command:
    def __init__(self,func,name,attributes=[],helptext = ""):
        self.name = name
        self.attributes = attributes
        self.func = func
        if helptext != "":
            self.helptext = helptext
        else:
            self.helptext = helptext

    def __str__(self):
        return "Command with name: {}".format(self.name)

    def do(self,args):
        log.debug("Doing command {} with args {}".format(self,args))
        return self.func(args)

class EmptyCommand(Command):
    def __init__(self):
        self.name = "Empty Command"
        self.attributes = []

    def do(self,args):
        return emptyResult()

def getCommand(name):
    log.debug("getCommand({})".format(name))
    if name in _commands.keys():
        log.debug("Found!")
        return _commands[name]
    else:
        log.debug("Not found!")
        return EmptyCommand()

def isCommand(name):
    return name in _commands.keys()

def registerCommand(name,func,timeout = 0,attributes = []):
    log.debug("registerCommand with name {}".format(name))
    decorator = command("name",timeout,attributes)
    decorator(func)

def alias(name,targetname):
    log.debug("registering alias {} for {}",name,targetname)
    target = getCommand(targetname)
    _commands[name] = target

def command(name,timeout = 0, attributes = []):
    name = name.lower()
    def decorator(func):
        class DecoratedFunc:
            def __init__(self,func,timeout,attributes):
                self.lastUsed = time.time()-timeout
                self.timeout = timeout
                self.func = func
                self.attributes = attributes

            def __call__(self,args):
                if self.lastUsed + self.timeout > time.time():
                    return timeoutResult(self.timeout-(time.time()-self.lastUsed))
                else:
                    self.lastUsed = time.time()
                    return successResult(self.func(args))


        decorated = DecoratedFunc(func,timeout,attributes)
        _commands[name] = Command(decorated,name,attributes)
        return func # leave the original function unmodified
    return decorator

@command("ping",timeout = 5, attributes = ['modonly'])
def ping(args):
    log.debug("hello this is ping with args {}".format(args))
    if args == "":
        return "pong"
    else:
        return args
