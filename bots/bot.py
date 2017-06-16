"""Create Bots from modules"""
#Twisted
from twisted.words.protocols import irc

#System
import re, subprocess
from time import sleep, time

#Bot modules
from bots.internbot import Intern
from bots.publicbot import Public
from bots.infrabot import Infra
from bots.vorstandbot import Vorstand

from modules import HQ, Keys, Postbox, InternTopic, Status
from utils import BotLog

LOG = BotLog()

def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).rstrip()

class Bot(irc.IRCClient):
    """The Bot"""

    status = Status()
    hq = HQ(status)
    keys = Keys()
    internTopic = InternTopic()
    postbox = Postbox()
    versionName = "christian"
    versionNum = "git-" + get_git_revision_short_hash()
    sourceURL = ""
    timestamp = 0

    def __init__(self):
        self.wait_max_sec = 6000
        self.current_wait_sec = 1
        self.intern_access = []
        self.status.callback = self.updateStatus

    def updateStatus(self, status):
        LOG.debug("update status: " + status)
        self.hq.hq_set(status)
        self.topicUpdated("mqtt", "#ccc-ffm-intern", status)

    def connectionMade(self):
        self.nickname = self.factory.nickname
        self.password = self.factory.password
        irc.IRCClient.connectionMade(self)
        self.current_wait_sec = 1
        LOG.log("notice", "connection established")
        LOG.log("info", "Connecting to mqtt broker...")
        self.status.connect(self.factory.mqtthost, self.factory.mqttport, self.factory.mqttusessl, 
                self.factory.mqttcafile, self.factory.mqtttopic, self.factory.mqttuser, self.factory.mqttpassword)

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
        if "ChanServ" in user and "Unbanned" in message:
            LOG.log("notice", "Unbanned successfully, rejoining...")
            for channel in self.factory.channel:
                self.join(channel)

    def lineReceived(self, line):
        LOG.debug(line)
        self.timestamp = time()
        irc.IRCClient.lineReceived(self, line)

    def _sendHeartbeat(self):
        irc.IRCClient._sendHeartbeat(self)
        seconds = int(time() - self.timestamp)
        if self.timestamp and seconds > self.heartbeatInterval:
            LOG.log("info", "No data received for " + str(seconds) + " seconds, aborting connection...") 
            self.transport.abortConnection()

    def irc_ERR_BANNEDFROMCHAN(self, prefix, params):
        nick = params[-3]
        channel = params[-2]
        LOG.log("notice", "We are banned from channel " + channel)
        self.unban(channel, self.nickname + "!*@*")

    def kickedFrom(self, channel, kicker, message):
        LOG.log("info", "We have been kicked from " + channel + " by " + kicker + "(" + message + ")")
        self.join(channel)

    def unban(self, channel, arg):
        LOG.log("info", "Trying to unban...")
        user, mask = arg.split('!')
        self.mode(channel, False, "b", None, user, mask) 
        self.msg('ChanServ', 'unban {0} {1}'.format(channel, self.nickname))

    def modeChanged(self, user, channel, set, modes, args):
        if "b" in modes:
            for arg in args:
                if self.nickname in arg:
                    if(set):
                        LOG.log("notice", "We have been banned from channel " + channel + " by " + user)
                        self.unban(channel, arg)
                    else:
                        LOG.log("notice", "We have been unbanned from channel " + channel + " by " + user)
                        self.join(channel)


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
        LOG.log("info", "joined channel: "+channel)
        # set topic on join
        """Intern channel specific"""
        if channel == '#ccc-ffm-intern' and self.hq.hq_status != 'unknown':
            self.topicUpdated("mqtt", "#ccc-ffm-intern", "status")

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

    def topicUpdated(self, user, channel, newTopic):
        nick, _, host = user.partition('!')
        if channel == '#ccc-ffm-intern' and nick != self.nickname and nick != self.hostname:
            self.topic(channel, self.internTopic.getTopic(self.hq, self.keys))

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
