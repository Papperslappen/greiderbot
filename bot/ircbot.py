import sys
import irc.client
import irc.bot
import logging
import bot.command as cmd
log = logging.getLogger('ircbot')
import bot.counter

def utf8len(s):
    return len(s.encode('utf-8'))

def utf8truncate(s,length): #This is bad but maybe good enough
    r = s[0:length]
    while utf8len(r)>length:
        r = r[0:-1]
    return r

def process_tags(t):
    tags = {}
    for row in t:
        k = row["key"]
        v = row["value"]
        tags[k] = v
    badges = tags["badges"].split(',')
    tags["badges"] = badges
    return tags


class IrcBot(irc.bot.SingleServerIRCBot):
    def __init__(self, channelname, nickname, server, port=6667, password = "", prefix="!",welcome = ""):
        irc.bot.SingleServerIRCBot.__init__(
            self,
            [irc.bot.ServerSpec(server,port,password)],
            nickname,
            nickname
        )
        if channelname[0] != '#':
            channelname = '#'+channelname
        self.channelname = channelname
        self.prefix = prefix
        self.welcome = welcome

    def on_nicknameinuse(self, c, e):
        c.nick(c.get_nickname() + "_")

    def on_welcome(self, c, e):
        c.cap("REQ", "twitch.tv/tags")
        c.cap("REQ", "twitch.tv/membership")
        c.cap("REQ", "twitch.tv/commands")

        log.info("Joining channel {}".format(self.channelname))
        c.join(self.channelname)
        if (self.welcome != "") :
            self.postToChannel(self.welcome)

    def on_privmsg(self, c, e):
        pass

    def on_pubmsg(self, c, e):
        message = e.arguments[0]
        tags = process_tags(e.tags)
        log.debug("Tags: {}".format(tags))
        if message.strip().startswith(self.prefix):
            log.debug("Command incoming from user: {}".format(e.source.nick))
            cline = message.strip().split(" ")
            command_name = cline[0]
            command_name = command_name[len(self.prefix):].lower()
            args = " ".join(cline[1:]) # args = "" if cline is the empty list
            log.debug("Finding command {} with args {}".format(command_name,args))
            command = cmd.getCommand(command_name)
            command_result = command.do(args)
            log.debug("CommandResult of type: {} with value: {}".format(command_result.type,command_result.value))
            if command_result.type == cmd.ResultType.TIMEOUT:
                log.info("Command {} timed out".format(command_name))
            elif command_result.type == cmd.ResultType.EMPTY:
                log.info("Command {} does not exist".format(command_name))
            else:
                if len(command_result.value) >= 1 :
                    log.info("Sending response: {} to channel {}".format(command_result.value,self.channelname))
                    self.postToChannel(command_result.value)

    def on_notice(self,c,e):
        pass

    def do_command(self,e,cmd):
        pass

    def whisperToUser(self,user,message):
        self.postToChannel("/w {} {}".format(user,message))

    def postToChannel(self,message):
        maxlength = 450 #this awaits a good unicode aware truncator
        #Remove carriage return and new line
        message = message.replace("\r"," ")
        message = message.replace("\n"," ")

        if utf8len(message) > maxlength:
            log.info("Trying to send a too long message. Length {}".format(len(message)))
            message = utf8truncate(message,maxlength)

        try:
            self.connection.privmsg(self.channelname,message)
        except irc.client.InvalidCharacters as e:
            log.error("Invalid characters in postToChannel. Error: {}".format(e))
        except:
            log.error("Error in postToChannel: {}".format(sys.exc_info()[0]))
            raise
