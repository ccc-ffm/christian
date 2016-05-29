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
from utils import BotLog, Signalhandler

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
    parser = SafeConfigParser()

    parser.read('./config/network.cfg')
    host=parser.get('network', 'hostname')
    port=parser.getint('network', 'port')

    #Read channels from config file
    parser.read('./config/channels.cfg')
    channels = parser.items( 'channels' )
    chan_list=[]

    for key, channel in channels:
            chan_list.append(channel)

    #Factory
    factory = BotFactory(chan_list)

    #connect
    LOG.log("info", "connecting to "+host+" on port "+str(port))
    reactor.connectSSL(host, port, factory, ssl.ClientContextFactory())

    sig = Signalhandler(factory)
    reactor.addSystemEventTrigger('before', 'shutdown', sig.savestates)

    #run
    LOG.log("info", "starting reactor")
    reactor.run()
