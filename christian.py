#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# twisted.words.protocols.irc not ported to python 3 yet m(

#USAGE: ./christian.py Channel


#twisted imports
from twisted.internet import reactor, protocol, ssl

#system imports
import sys
from ConfigParser import SafeConfigParser

#Import the bots we want to create
from bots import InternBot, Bot, PublicBot
from modules import BotLog

LOG = BotLog()

LOG.log("notice", "Christian started")
class BotFactory(protocol.ClientFactory):
    """A factory for Bots.
    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel):
        #TODO: Set proper channels
        """Create different bots based on channel"""
        self.protocol = Bot
        if channel == 'botdemo':
            self.protocol = InternBot
            LOG.log("info", "instance: InternBot")
            self.channel = channel #channel we're going to join
            LOG.log("info", "channel: "+channel)
        elif channel == 'test':
            self.protocol = PublicBot
            LOG.log("info", "instance: InternBot")
            self.channel = 'testgnarplong'
            LOG.log("info", "channel: "+channel)
        else:
            LOG.log("crit", "no such channel: "+channel)
            exit(1)

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        LOG.log("crit", "connection failed: "+str(reason))
        #reactor.stop()

    def getChannel(self):
        return(self.channel)

if __name__ == '__main__':

    #create intern
    FACTORY = BotFactory(sys.argv[1])

    #read Serversettings from config file
    PARSER = SafeConfigParser()
    PARSER.read('./config/network.cfg')

    HOST=PARSER.get('network', 'hostname')
    PORT=PARSER.getint('network', 'port')

    #connect
    LOG.log("info", "connecting to "+HOST+" on port "+str(PORT))
    reactor.connectSSL(HOST, PORT, FACTORY, ssl.ClientContextFactory())

    #run
    LOG.log("info", "starting reactor")
    reactor.run()
