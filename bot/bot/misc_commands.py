import bot.command as cmd
import wikipedia
import logging
import sys

log = logging.getLogger("misc_commands")

wikipedia.set_lang("sv")

@cmd.command("fakta",timeout=30)
def fakta(args):
    """Visa ett kul fakta om något"""
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
