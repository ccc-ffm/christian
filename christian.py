#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# twisted.words.protocols.irc not ported to python 3 yet m(

#USAGE: ./christian.py #Channel

#twisted imports
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol, ssl

#system imports
import sys,re,thread,time
from datetime import datetime
from ConfigParser import SafeConfigParser

#Import the bots we want to create
from bots import InternBot,Bot,PublicBot
from modules import BotLog

log = BotLog()

log.log("notice", "Christian started")
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
            log.log("info", "instance: InternBot")
            self.channel = channel #channel we're going to join
            log.log("info", "channel: "+channel)
        elif channel == 'test':
            self.protocol = PublicBot
            log.log("info", "instance: InternBot")
            self.channel = 'testgnarplong'
            log.log("info", "channel: "+channel)
        else:
            log.log("crit", "no such channel: "+channel)
            exit(1)

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        log.log("crit", "connection failed: "+str(reason))
        reactor.stop()

    def getChannel(self):
        return(self.channel)

if __name__ == '__main__':

    #create intern
    factory = BotFactory(sys.argv[1])

    #read Serversettings from config file
    parser = SafeConfigParser()
    parser.read('./config/network.cfg')

    host=parser.get('network', 'hostname')
    p=parser.getint('network', 'port')

    #connect
    log.log("info", "connecting to "+host+" on port "+str(p))
    reactor.connectSSL(host, p, factory, ssl.ClientContextFactory())

    #run
    log.log("info", "starting reactor")
    reactor.run()
