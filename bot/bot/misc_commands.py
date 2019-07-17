import bot.command as cmd
import wikipedia
import logging
import sys

log = logging.getLogger("misc_commands")

@cmd.command("fakta",timeout=10,attributes=["subonly"])
def svFact(args):
    """Visa ett kul fakta om något"""
    wikipedia.set_lang("sv")
    return fact(args)

@cmd.command("fact",timeout=10,attributes=["subonly"])
def enFact(args):
    """Visa ett kul fakta om något fast på engelska"""
    wikipedia.set_lang("en")
    return fact(args)

cmd.alias("killgissa","fakta")

@cmd.command("äsch",timeout=10,attributes=[])
def asch(args):
    return "äsch"


def fact(args):
    if args == "":
        page = wikipedia.random()
    else:
        page = args
    fact = ""
    try:
        fact = wikipedia.summary(page,sentences = 2)
    except wikipedia.DisambiguationError as e:
        alternatepage = e.options[0]
        log.info("DisambiguationError, try article  {}".format(alternatepage))
        fact = wikipedia.summary(alternatepage,sentences = 2) #lets hope that DisambiguationError always gives a list of valid pages
    except:
        log.warn("Other wikipedia error: {}".format(sys.exc_info()[0]))
    finally:
        return fact


@cmd.command("discord",timeout=10)
def discord(args):
    """Länka till discord"""
    return "https://discord.gg/zhEnSX9"
