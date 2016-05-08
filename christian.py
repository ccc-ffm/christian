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
from bots import Bot
from modules import BotLog

LOG = BotLog()

LOG.log("notice", "Christian started")

class BotFactory(protocol.ClientFactory):
    """A factory for Bots.
    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel):
        self.channel = channel
        self.protocol = Bot

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        LOG.log("crit", "connection failed: "+str(reason))

    def getChannel(self):
        return(self.channel)

if __name__ == '__main__':


    #read Serversettings from config file
    PARSER = SafeConfigParser()

    PARSER.read('./config/network.cfg')
    HOST=PARSER.get('network', 'hostname')
    PORT=PARSER.getint('network', 'port')

    #Read channels from config file
    PARSER.read('./config/channels.cfg')
    CHANNELS = PARSER.items( 'channels' )
    chan_list=[]
    for key, channel in CHANNELS:
            chan_list.append(channel)

    #Factory
    FACTORY = BotFactory(chan_list)

    #connect
    LOG.log("info", "connecting to "+HOST+" on port "+str(PORT))
    reactor.connectSSL(HOST, PORT, FACTORY, ssl.ClientContextFactory())

    #run
    LOG.log("info", "starting reactor")
    reactor.run()
