"""Create Bots from modules"""
#Twisted
from twisted.words.protocols import irc

#System
import re, getpass
from time import sleep
#Bot modules
from modules import HQ, EasterEggs, ServiceFunctions, Keyfunctions

class Bot(irc.IRCClient):
    """Bot Baseclass"""

    def __init__(self):
        self.wait_max_sec = 6000
        self.current_wait_sec = 120

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        print "Connection Established"

    def connectionLost(self, reason):
        #Wait before we
        if self.current_wait_sec < self.wait_max_sec:
            self.current_wait_sec = self.current_wait_sec * 2
        sleep(self.current_wait_sec)
        #try to reconnect
        irc.IRCClient.connectionLost(self, reason)

    def alterCollidedNick(self, nickname):
        return nickname+'_'


class PublicBot(Bot):
    """This Bot will join the public channel"""

    nickname = 'hans'

    """Action Objects"""
    service = ServiceFunctions()

    def joined(self, channel):
        self.say(channel, "Hello my friends! I'm back!")

    def privmsg(self, user, channel, message):
        nick, _, host = user.partition('!')
        msg = message.split(" ")

        if msg[0] == "!help":
            self.service.help(nick, channel, self)
        if msg[0] == "!donnerstag":
            self.service.donnerstag(channel, self)

class InternBot(Bot):
    """This Bot will jpin the intern channel"""

    nickname = 'hans'

    """Action Objects"""
    key = Keyfunctions()
    eggs = EasterEggs()
    service = ServiceFunctions()
    haq = HQ()

    def signedOn(self):
        pswd = getpass.getpass('Authpassword: ')
        self.msg('nickserv','identfy'+pswd)
        sleep(1)
        #TODO: check nickserv answer
        #if nickserv answer authenticated join
        #else connection Lost
        self.join(self.factory.channel)


    def userKicked(self, kickee, channel, kicker, message):
        print "kickee: " + kickee
        print "channel : " + channel
        print "kicker : " + kicker
        print "message : " + message
        msg = "Hallo, der Channel " + channel + " kann nur \
                betreten werden, wenn man auf der Access-Liste \
                steht und eingeloggt ist. Falls du auf der \
                Access-Liste stehst, logge dich bitte ein und \
                versuche es erneut."
        self.msg(kickee, msg)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        # set topic on join
        self.say(channel, "Hello my friends! I'm back!")
        if self.haq.isopen == "open":
            self.topic(channel, "HQ is open since " + self.haq.statussince)
        elif self.haq.isopen == "private":
            self.topic(channel, \
                    "HQ is open for members only since " + self.haq.statussince)
        elif self.haq.isopen == "closed":
            self.topic(channel, "HQ is closed")
        else:
            # if proper status is unknown ask for it
            self.say(channel, "I don't know the current status of the HQ. \
                    Please double-check the status and set it to the \
                    proper value!")


    @classmethod
    def getusers(cls, message, nick):
        """Check user list from command"""
        msg = message.split()
        if len(msg) == 1:
            users = [nick]
        else:
            users = msg[1:]
        return users

    def privmsg(self, user, channel, message):
        """This is called on any message seen in the given channel"""
        nick, _, host = user.partition('!')
        #do nothing if first sign is something else than a !
        if message[0] != "!":
            return False

        ## replace nick aliases by the actual nickname
        aliases = {}
        with open("./config/aliases", "r") as filea:
            for line in filea:
                alias = line.split(":")
                aliases[alias[0]] = alias[1].strip().encode()
        for alias, nickname in aliases.items():
            message = re.sub(alias, nickname, message)
        msg = message.split(" ")

        if msg[0] == "!help":
            self.service.help(nick, channel, self)

        #if channel[1:] != self.factory.getChannel():
            #return False
        if msg[0] == "!keys":
            if len(msg) == 3:
                self.key.changekeyholders(channel, self, msg[1], msg[2])
            else:
                self.key.listkeys(nick, self)
        elif msg[0] == "!donnerstag":
            self.service.donnerstag(channel, self)
        elif msg[0] == "!darkwing":
            self.eggs.darkwing(channel, self)
        elif msg[0] == "!balu":
            self.eggs.balu(channel, self)
        elif msg[0] == "!raspel":
            self.eggs.raspel(channel, self)
        elif msg[0] == "!open":
            self.haq.openhq(channel, self)
        elif msg[0] == "!private":
            self.haq.privatehq(channel, self)
        elif msg[0] == "!close":
            self.haq.closehq(channel, self)
        elif msg[0] == "!join":
            self.haq.join(channel, self, self.getusers(message, nick))
            if self.haq.isopen == "closed":
                self.haq.openhq(channel, self)
            if self.key.iskeyholder(nick):
                #If the person owns a key, increase count of physical keys in HQ
                self.haq.keysinhq += 1
        elif msg[0] == "!leave" or msg[0] == "!part":
            self.haq.leave(channel, self, self.getusers(message, nick))
            # Check if person with last key is leaving the hq
            if self.haq.keysinhq == 1 and self.key.iskeyholder(nick):
                self.msg(nick, "You've got the last key!" \
                 " Remember to lock the door!")
                self.say(channel, \
                        nick + " has the last key, don't let him escape!")
        elif msg[0] == "!whois":
            self.haq.whois(channel, self)
