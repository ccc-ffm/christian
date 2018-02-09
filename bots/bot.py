"""Create Bots from modules"""
#Twisted
from twisted.words.protocols import irc

#System
import re, subprocess
from time import sleep, time
import os.path

#import commands
from commands import EasterEggFunctions, HQFunctions,\
                     KeyFunctions, ServiceFunctions,\
                     HelpFunctions, PostboxFunctions,\
                     PostboxMgmtFunctions, AssistanceFunctions

from modules import HQ, Keys, Postbox, InternTopic, Status, Friendship
from utils import BotLog

LOG = BotLog()

def get_git_revision_short_hash():
    return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).rstrip()

class Bot(irc.IRCClient):
    """The Bot"""

    status = Status()
    hq = None
    keys = None
    postbox = None
    friendship = None
    internTopic = InternTopic()
    versionName = "christian"
    versionNum = "git-" + get_git_revision_short_hash()
    sourceURL = ""
    lineRate = .2
    timestamp = 0
    hostname = None


    EasterEggFunctions = EasterEggFunctions()
    HQFunctions = HQFunctions()
    KeyFunctions = KeyFunctions()
    ServiceFunctions = ServiceFunctions()
    HelpFunctions = HelpFunctions()
    PostboxFunctions = PostboxFunctions()
    PostboxMgmtFunctions = PostboxMgmtFunctions()
    AssistanceFunctions = AssistanceFunctions()

    def __init__(self):
        self.wait_max_sec = 6000
        self.current_wait_sec = 1
        self.intern_access = []
        self.status.callback = self.updateStatus

    def updateStatus(self, status):
        LOG.debug("update status: " + status)
        self.hq.hq_set(status)
        for channel in self.factory.channel:
            if 'HQFunctions' in self.factory.channel[channel]:
                LOG.debug("set topic on channel " + channel)
                self.topicUpdated("mqtt", "#" + channel, status)

    def connectionMade(self):
        self.keys = self.factory.keys
        self.hq = self.factory.hq
        self.hq.status = self.status
        self.postbox = self.factory.postbox
        self.friendship = self.factory.friendship
        self.nickname = self.factory.nickname
        self.password = self.factory.password
        irc.IRCClient.connectionMade(self)
        self.current_wait_sec = 1
        LOG.log("notice", "connection established")
        LOG.log("info", "Connecting to MQTT broker...")
        f = self.factory
        try:
            self.status.connect(f.MQTT_host, f.MQTT_port, f.MQTT_ssl, f.MQTT_ca,
                    f.MQTT_topic, f.MQTT_user, f.MQTT_pass, f.MQTT_id,
                    f.MQTT_bunteslicht, f.MQTT_sound, f.MQTT_switch,
                    f.MQTT_ambientlight, f.MQTT_power)
        except:
            LOG.log("warning", "failed connecting to MQTT broker.")

        self.aliases = {}
        with open(self.factory.useraliases, "r") as filea:
            for line in filea:
                alias = line.split(":")
                self.aliases[alias[0]] = alias[1].strip().encode()

        self.cmdaliases = {}
        if os.path.isfile(self.factory.cmdaliases):
            with open(self.factory.cmdaliases, "r") as fileb:
                for line in fileb:
                    alias = line.split(":")
                    self.cmdaliases[alias[0]] = alias[1].strip().encode()

    def connectionLost(self, reason):
        LOG.log("crit", "connection lost: "+str(reason))
        #Wait before we
        if self.current_wait_sec < self.wait_max_sec:
            self.current_wait_sec = self.current_wait_sec * 2
            sleep(self.current_wait_sec)
        #try to reconnect
        self.status.disconnect()
        irc.IRCClient.connectionLost(self, reason)

    def irc_ERR_NICKNAMEINUSE(self, prefix, params):
        irc.IRCClient.irc_ERR_NICKNAMEINUSE(self, prefix, params)
        LOG.log("info", "Nick " + self.nickname + " is already in use. Issue GHOST command...")
        self.msg('NickServ', 'ghost {0} {1}'.format(self.nickname, self.password))
        self.setNick(self.nickname)

    def signedOn(self):
        self.identify()
        self.whois(self.nickname)

    def identify(self):
        LOG.log("notice", "Authenticating against NickServ...")
        self.msg('NickServ', 'identify {0} {1}'.format(self.nickname, self.password))
        LOG.log("notice", "Awaiting verification...")

    def irc_RPL_WHOISUSER(self, prefix, params):
        if params[-5] == self.nickname:
            self.hostname = params[-3]

    def noticed(self, user, channel, message):
        if "NickServ" in user and "identified" in message:
            LOG.log("notice", "Successfully authenticated against NickServ")
            for channel in self.factory.channel:
                self.join(channel)
        if "NickServ" in user and "is registered" in message:
            LOG.log("notice", "Received notice that nick is registered, reauthenticate...")
            self.identify()
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
        self.mode(channel, False, "b", None, arg)
        self.msg('ChanServ', 'unban {0} {1}'.format(channel, self.nickname))

    def modeChanged(self, user, channel, set, modes, args):
        if "b" in modes:
            for arg in args:
                if self.nickname in arg or (self.hostname and self.hostname in arg):
                    if(set):
                        LOG.log("notice", "We have been banned from channel " + channel + " by " + user)
                        self.unban(channel, arg)
                    else:
                        LOG.log("notice", "We have been unbanned from channel " + channel + " by " + user)
                        self.join(channel)
        if channel.lstrip("#") in self.factory.channel and 'HQFunctions' in self.factory.channel[channel.lstrip('#')]:
            if "o" in modes:
                for arg in args:
                    # if we know the status (from mqtt) set it once we joined and got op
                    if self.nickname in arg and set and self.hq.hq_status != 'unknown':
                        LOG.log("notice", "Got op, setting topic")
                        self.topicUpdated("mqtt", channel, "status")


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

    @classmethod
    def do_action(self, message, nick, channel, instance):

        command = message[0].translate(None, '!')
        action = None
        channel_actions = {}

        chan = channel.lstrip('#')
        if chan in instance.factory.channel:
            channel_actions = instance.factory.channel[chan]
            LOG.log("notice", "actions associated with channel `" + channel + "`: " + str(channel_actions))
        found = False
        for actions in channel_actions:
            actions = actions.strip()
            try:
                """Don't create new instances for each command"""
                #action = getattr(globals()[actions](),command) if globals().has_key(actions) else None
                action = getattr(getattr(instance, actions),command) if hasattr(instance, actions) and hasattr(getattr(instance, actions), command) else None
                if action:
                    LOG.log("info", "Found command `" + command + "` in `" + actions + "`")
                    kwargs = {'msg': message[1:],
                              'nck': nick,
                              'hq': instance.hq,
                              'keys': instance.keys,
                              'pb': instance.postbox,
                              'friendship': instance.friendship
                             }

                    found = True
                    action(channel, instance, **kwargs)
            except:
                pass
        if not found:
            LOG.log("info", "Command `" + command + "` not implemented in actions associated with channel `" + channel + "`")
            return

    @classmethod
    def do_special_action(self, message, nick, channel, instance):
        if 'AssistanceFunctions' in instance.factory.channel[channel.lstrip('#')]:
            pattern = re.compile('(' + '|'.join(instance.factory.url_list) + ')(\S*)')
            matches = re.findall(pattern, message)
            if matches:
                for match in matches:
                    url = instance.friendship.getPrivateUrl('https://' + match[0] + match[1])
                    instance.say(channel, url)
                return True
            else:
                return False
        else:
            return False

    def topicUpdated(self, user, channel, newTopic):
        nick, _, host = user.partition('!')
        if nick != self.nickname and nick != self.hostname and channel.lstrip("#") in self.factory.channel and 'HQFunctions' in self.factory.channel[channel.lstrip('#')]:
            self.topic(channel, self.internTopic.getTopic(self.hq, self.keys))

    def privmsg(self, user, channel, message):
        """This is called on any message seen in the given channel"""
        nick, _, host = user.partition('!')

        #do nothing if first sign is something else than a !
        if message[0] != "!":
            return self.do_special_action(message, nick, channel, self)

        #replace nick aliases by the actual nickname
        for alias, nickname in self.aliases.items():
            message = re.sub(alias, nickname, message)

        message = message.strip()
        msg = message.split(" ")

        #replace cmd aliases with the actual command
        for alias, command in self.cmdaliases.items():
            msg[0] = re.sub(alias, command, msg[0])


        self.do_action(msg, nick, channel, self)
