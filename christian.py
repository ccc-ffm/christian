#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# twisted.words.protocols.irc not ported to python 3 yet m(

#USAGE: ./christian.py #Channel

#twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl

#system imports
import sys,os,random



class EasterEggs():

    def DarkWing(self,channel,cb):
        #TODO: Random selection from file
        #Random Selection from Jonathan Kupferman:
        #http://www.regexprn.com/2008/11/read-random-line-in-large-file-in.html
        #Open the file:

        filename="./mylines/darkwing.txt"
        file = open(filename,'r')

        #Get the total file size
        file_size = os.stat(filename)[6]

        #seek to a place in the file which is a random distance away
        #Mod by file size so that it wraps around to the beginning
        file.seek((file.tell()+random.randint(0,file_size-1))%file_size)

        #dont use the first readline since it may fall in the middle of a line
        file.readline()

        #this will return the next (complete) line from the file
        line = file.readline()

        #here is your random line in the file
        cb.say(channel,line)

    def Balu(self):
        #TODO: Random selection from file
        msg = "Balu"
        return msg

    def Press(self):
        #TODO: Read from file
        url="http://ccc-ffm.de"
        return url

class ServiceFunctions():

    def Donnerstag(self,channel,cb):
        #TODO: Read from file
        cb.say(channel,"Wir treffen uns immer Donnerstags um 19:00 Uhr in Bockenheim in unserem Hackquarter in der Häuser Gasse 2")


class KeyFunctions():

    def __init__(self):
        self.keyholders = ["max", "gnom", "test"]

    def ListKeys(self,channel,cb):
        """List current holders of hq keys"""
        #TODO make keyholders persistant

        print("ListKeys")
        keyMessage = "All the keys are belong to: "
        keyMessage += ", ".join(self.keyholders)
        cb.say(channel,keyMessage)

    def OpenHQ(self,arg,channel,cb):
        """This changes the channel topic"""
        foo = "bar"

    def CloseHQ(self,arg,channel,cb):
        """This changes the channel topic"""
        foo = "bar"

    def ChangeKeyholders(self,channel,cb,oldholder,newholder):
        """This changes the channel topic"""
        self.keyholders.remove(oldholder)
        self.keyholders.add(newholder)

class InternBot(irc.IRCClient):
    nickname = 'fred'

    """Action Objects"""
    key = KeyFunctions()
    eggs = EasterEggs()
    service = ServiceFunctions()

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

    def alterCollidedNick(self, nickname):
        return nickname+'_'

    def settopic(self, topic):
        self.topic(topic)

    def privmsg(self, user, channel, message):
        """This is called on any message seen in the given channel"""
        nick, _, host = user.partition('!')
        msg = message.split(" ")

        #Iterate over msg
        if msg[0] == "!keys":
            self.key.ListKeys(channel,self)
        elif msg[0] == "!donnerstag":
            self.service.Donnerstag(channel,self)
        elif msg[0] == "!darkwing":
            self.eggs.DarkWing(channel,self)


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
    #create new keys
    keys = KeyFunctions()

    #TODO: Parse from config file
    hostname = 'irc.hackint.org'
    port = 9999
    reactor.connectSSL(hostname, port, factory, ssl.ClientContextFactory())

    #run
    reactor.run()
