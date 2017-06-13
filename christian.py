#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# twisted.words.protocols.irc not ported to python 3 yet m(

#USAGE: ./christian.py Channel


#twisted imports
from twisted.internet import reactor, protocol, ssl, endpoints
from twisted.names import client

#system imports
import sys
from ConfigParser import SafeConfigParser

#Import the bots we want to create
from bots import Bot
from utils import BotLog, Signalhandler, Filehandler
from time import sleep

import socket

LOG = BotLog()

LOG.log("notice", "Christian started")

addresses = []
addresses6 = []
addrs = []
factory = None
port = ""
host = ""
usessl = True
cafile = ""

def gotAddress(result):
    global addresses, addrs
    for record in result[0]:
        addresses.append(record.payload.dottedQuad())
        #print (record.payload.dottedQuad())
    addrs.extend(addresses6)
    addrs.extend(addresses)
    addrs.reverse()
    connect_next()

def gotAddress6(result):
    global addresses6
    for record in result[0]:
        addresses6.append(socket.inet_ntop(socket.AF_INET6, record.payload.address))
        #print socket.inet_ntop(socket.AF_INET6, record.payload.address)
    address = client.lookupAddress(host)
    address.addCallback(gotAddress)

def connect_next():
    global addresses, addresses6, addrs
    if len(addrs) is 0:
        """If we tried all available addresses wait a while and do another lookup"""
        sleep(5)
        addresses = []
        addresses6 = []
        address_lookup()
    else:
        addr = addrs.pop()
        LOG.log("info", "connecting to " + host + "[" + addr + "] on port "+str(port) + (" using SSL" if usessl else ""))
        if usessl:
            """Actually verify server certificate"""
            certData = Filehandler().getcontent(cafile)
            authority = ssl.Certificate.loadPEM(certData)
            options = ssl.optionsForClientTLS(u'{0}'.format(host), authority)
            endpoint = endpoints.SSL4ClientEndpoint(reactor, addr, port, options)
            endpoint.connect(factory)
            #reactor.connectSSL(addr, port, factory, ssl.ClientContextFactory())
        else:
            reactor.connectTCP(addr, port, factory)

def address_lookup():
    address6 = client.lookupIPV6Address(host)
    address6.addCallback(gotAddress6)

class BotFactory(protocol.ClientFactory):
    """A factory for Bots.
    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel, nickname, password):
        self.channel = channel
        self.protocol = Bot
        self.nickname = nickname
        self.password = password

    def clientConnectionLost(self, connector, reason):
        """If we get disconnected, reconnect to server."""
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        """If connection fails, try again (server might be down temporarily)."""
        LOG.log("crit", "connection failed: "+str(reason))
        connect_next()

    def getChannel(self):
        return(self.channel)

if __name__ == '__main__':
    #global factory, host, port, usessl, cafile

    #read Serversettings from config file
    parser = SafeConfigParser()

    parser.read('./config/network.cfg')
    host=parser.get('network', 'hostname')

    address_lookup()

    port=parser.getint('network', 'port')
    usessl=parser.getboolean('network', 'ssl')
    cafile = parser.get('network', 'cafile') if usessl else ""
    nickname=parser.get('network', 'nickname')
    password=parser.get('network', 'password')

    #Read channels from config file
    parser.read('./config/channels.cfg')
    channels = parser.items( 'channels' )
    chan_list=[]

    for key, channel in channels:
            chan_list.append(channel)

    #Factory
    factory = BotFactory(chan_list, nickname, password)

    sig = Signalhandler(factory)
    reactor.addSystemEventTrigger('before', 'shutdown', sig.savestates)

    reactor.run() 
