#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# twisted.words.protocols.irc not ported to python 3 yet m(

#USAGE: ./christian.py #Channel

#twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl

#system imports
import sys

class EasterEggs():

    def DarkWing(self):
        #TODO: Random selection from file
        msg = "DarkWing"
        return msg

    def Balu(self):
        #TODO: Random selection from file
        msg = "Balu"
        return msg

    def Press(self):
        #TODO: Read from file
        url="http://ccc-ffm.de"
        return url

class ServiceFunctions():

    def Donnerstag(self,arg,channel,cb):
        #TODO: Read from file
        msg = "Donnerstag"
        cb.say(channel,"Wir treffen uns immer Donnerstags um 19:00 Uhr in Bockenheim in unserem Hackquarter in der Häuser Gasse 2")
        print("Donnerstag")
        return msg


class KeyFunctions():


    def ListKeys(self,arg,channel,cb):
        print("ListKeys")
        cb.say(channel,"ListKeys")

    def OpenHQ(self,arg,channel,cb):
        """This changes the channel topic"""
        foo = "bar"

    def CloseHQ(self,arg,channel,cb):
        """This changes the channel topic"""
        foo = "bar"

    def ChangeKeyholders(self,oldholder,newholder):
        """This changes the channel topic"""
        self.keyholders.remove(oldholder)
        self.keyholders.add(newholder)

class InternBot(irc.IRCClient):
    nickname = 'christian'

    """Action Objects"""
    key = KeyFunctions()
    eggs = EasterEggs()
    service = ServiceFunctions()

    """Function Dispatcher"""
    dispatch = {
            '!test':key.ListKeys,
            '!donnerstag':service.Donnerstag,
            }

    def connectionMade(self):
        irc.IRCClient.connectionMade(self)
        print ("connection Established")

    def connectionLost(self, reason):
        irc.IRCClient.connectionLost(self, reason)

    def signedOn(self):
        """Called when bot has succesfully signed on to server."""
        #TODO Get and Set Keyholders from Channel topic
        self.join(self.factory.channel)

    def joined(self, channel):
        """This will get called when the bot joins the channel."""

    def privmsg(self, user, channel, msg):
        """This will get called when the bot receives a message."""

        # Check to see if they're sending me a private message
        if channel == self.nickname:
            msg = "Wer flüstert lügt ;)"
            self.msg(user, msg)

        # Otherwise check to see if it is a message directed at me
        if msg.startswith(self.nickname + ":"):
            msg = "I am a Bot, lower your shields and surrender your ships."
            self.msg(channel, msg)

    def alterCollidedNick(self, nickname):
        return nickname+'_'

    def settopic(self, topic):
        self.topic(topic)

    def privmsg(self, user, channel, message):
        nick, _, host = user.partition('!')
        message = message.strip()

        self.dispatch[message]("test",channel,self)


class BotFactory(protocol.ClientFactory):
    """A factory for Bots.
    A new protocol instance will be created each time we connect to the server.
    """

    protocol = InternBot

    def __init__(self, channel):
        self.channel = 'gnarplong' #channel


    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        print ("connection failed: %s", reason)
        reactor.stop()

if __name__ == '__main__':
    #create intern
    factory = BotFactory(sys.argv[1])

    #TODO: Parse from config file
    hostname = 'irc.hackint.org'
    port = 9999
    reactor.connectSSL(hostname, port, factory, ssl.ClientContextFactory())

    #run
    reactor.run()
