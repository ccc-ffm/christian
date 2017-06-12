"""Create Bots from modules"""
#Twisted
from twisted.words.protocols import irc

#System
import re, getpass
from time import sleep

#Bot modules
from bots.internbot import Intern
from bots.publicbot import Public
from bots.infrabot import Infra
from bots.vorstandbot import Vorstand

from modules import HQ, Keys, Postbox
from utils import BotLog

LOG = BotLog()

class Bot(irc.IRCClient):
    """The Bot"""

    hq = HQ()
    keys = Keys()
    postbox = Postbox()

    def __init__(self):
        self.wait_max_sec = 6000
        self.current_wait_sec = 1
        self.intern_access = []

    def connectionMade(self):
        self.nickname = self.factory.nickname
        self.password = self.factory.password
        irc.IRCClient.connectionMade(self)
        self.current_wait_sec = 1
        LOG.log("notice", "conncetion established")

    def connectionLost(self, reason):
        LOG.log("crit", "connection lost: "+str(reason))
        #Wait before we
        if self.current_wait_sec < self.wait_max_sec:
            self.current_wait_sec = self.current_wait_sec * 2
            sleep(self.current_wait_sec)
        #try to reconnect
        irc.IRCClient.connectionLost(self, reason)

    def irc_ERR_NICKNAMEINUSE(self, prefix, params):
        irc.IRCClient.irc_ERR_NICKNAMEINUSE(self, prefix, params)
        LOG.log("info", "Nick " + self.nickname + " is already in use. Issue GHOST command...")
        self.msg('NickServ', 'ghost {0} {1}'.format(self.nickname, self.password))
        self.setNick(self.nickname)

    def signedOn(self):
        LOG.log("notice", "Authenticating against NickServ...")
        self.msg('NickServ', 'identify {0} {1}'.format(self.nickname, self.password))
        LOG.log("notice", "Awaiting verification...")

    def noticed(self, user, channel, message):
        if "NickServ" in user and "identified" in message:
            LOG.log("notice", "Successfully authenticated against NickServ")
            for channel in self.factory.channel:
                self.join(channel)
        if "NickServ" in user and "is registered" in message:
            LOG.log("notice", "Received notice that nick is registered, reauthenticate...")
            self.signedOn()

    def lineReceived(self, line):
        LOG.debug(line)
        irc.IRCClient.lineReceived(self, line)

    def userKicked(self, kickee, channel, kicker, message):
        msg = ("Hallo, der Channel {0} kann nur betreten \
        werden, wenn man auf der Access-Liste \
        steht und eingeloggt ist. Falls du auf \
        der Access-Liste stehst, logge dich \
        bitte ein und versuche es erneut.".format(channel))

        self.msg(kickee, msg)
        LOG.debug(kicker+' kicked '+kickee+' \
        from channel '+channel+' with reason: '+message)

    def userJoined(self,user,channel):
        """Check if there are any messages for the user"""
        if self.postbox.hasmessage(user) is True:
            self.postbox.replaymessage(user,self)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""
        # set topic on join
        LOG.log("info", "joined channel: "+channel)
        """Intern channel specific"""
        if channel == '#testabot2':
            #self.msg('ChanServ', 'access #ccc-ffm-infra list')
            self.msg('ChanServ','hallo')
            if self.haq.isopen == "open":
                self.topic(channel, "HQ is open since " + self.haq.statussince)
            elif self.haq.isopen == "private":
                self.topic(channel, \
                    "HQ is open for members only since " + self.haq.statussince)
            elif self.haq.isopen == "closed":
                self.topic(channel, "HQ is closed")
            else:
                #if proper status is unknown ask for it
                self.say(channel, 'I don\'t know the current status'
                'of the HQ. Please double-check the status and set'
                'it to the proper value!')


    @classmethod
    def publicaction(self, message, nick, channel, instance):

        publicactions = Public()
        command = message[0].translate(None, '!')
        action = None

        try:
            action = getattr(publicactions,command)
        except:
            raise NotImplementedError("Class `{}` does not implement `{}`".
                    format(publicactions.__class__.__name__, command))

        kwargs = {'msg': message[1:],
                  'nck': nick
                 }

        action(channel, instance, **kwargs)

    @classmethod
    def internaction(self, message, nick, channel, instance):

        internactions = Intern()
        command = message[0].translate(None, '!')
        action = None

        try:
            action=getattr(internactions,command)
        except:
            raise NotImplementedError("Class `{}` does not implement `{}`".
                    format(internactions.__class__.__name__, command))

        kwargs = {'msg': message[1:],
                  'nck': nick,
                  'hq': self.hq,
                  'keys': self.keys,
                  'pb': self.postbox
                 }
        action(channel, instance, **kwargs)


    @classmethod
    def infraaction(self, message, nick, channel, instance):

        infraactions = Infra()
        command = message[0].translate(None, '!')
        action = None

        try:
            action = getattr(infraactions, command)
        except:
            raise NotImplementedError("Class `{}` does not implement `{}`".
                    format(infraactions.__class__.__name__, command))

        kwargs = {'msg': message[1:],
                  'nck': nick,
                  'pb': self.postbox
                 }

        action(channel, instance, **kwargs)

    @classmethod
    def vorstandaction(self, message, nick, channel, instance):

        vorstandactions = Vorstand()
        command = message[0].translate(None, '!')
        action = None

        try:
            action = getattr(vorstandactions,command)
        except:
            raise NotImplementedError("Class `{}` does not implement `{}`".
                    format(vorstandactions.__class__.__name__,command))

        kwargs={}
        action(channel, instance, **kwargs)

    def privmsg(self, user, channel, message):
        """This is called on any message seen in the given channel"""
        nick, _, host = user.partition('!')

        #do nothing if first sign is something else than a !
        if message[0] != "!":
            return False

        #replace nick aliases by the actual nickname
        aliases = {}
        with open("./config/aliases", "r") as filea:
            for line in filea:
                alias = line.split(":")
                aliases[alias[0]] = alias[1].strip().encode()
        for alias, nickname in aliases.items():
            message = re.sub(alias, nickname, message)
        msg = message.split(" ")

        #Pass the message to its method based on the channel
        if channel == '#ccc-ffm-intern':
            self.internaction(msg, nick, channel, self)

        elif channel == '#ccc-ffm':
            self.publicaction(msg, nick, channel, self)

        elif channel == '#ccc-ffm-infra':
            self.infraaction(msg, nick, channel,self)

        elif channel == '#ccc-ffm-vorstand':
            self.vorstandaction(msg, nick, channel, self)
