#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# twisted.words.protocols.irc not ported to python 3 yet m(

#USAGE: ./christian.py Channel


#twisted imports
from twisted.internet import reactor, protocol, ssl, endpoints, task
from twisted.application.internet import ClientService
from twisted.names import client, dns

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

def addressFailed(error):
    LOG.debug(str(error))
    sleep(5)
    address = client.lookupAddress(host)
    address.addCallback(gotAddress)
    address.addErrback(addressFailed)

def address6Failed(error):
    LOG.debug(str(error))
    sleep(5)
    address6 = client.lookupIPV6Address(host)
    address6.addCallback(gotAddress6)
    address6.addErrback(address6Failed)

def gotAddress(result):
    global addresses, addresses6, addrs
    addresses = []
    for record in result[0]:
        if isinstance(record.payload, dns.Record_A):
            addresses.append(record.payload.dottedQuad())
    addrs = []
    addrs.extend(addresses6)
    addrs.extend(addresses)
    LOG.log("info", "Got the following addresses for " + host + ": " + ", ".join(addrs))
    addrs.reverse()
    connect_next()

def gotAddress6(result):
    global addresses6
    addresses6 = []
    for record in result[0]:
        if isinstance(record.payload, dns.Record_AAAA):
            addresses6.append(socket.inet_ntop(socket.AF_INET6, record.payload.address))
    address = client.lookupAddress(host)
    address.addCallback(gotAddress)
    address.addErrback(addressFailed)

def checkFailure(reconnector):
    failedAttempts =  reconnector._machine._failedAttempts if hasattr(reconnector, '_machine') else reconnector._failedAttempts
    LOG.debug("checkFailure: " + str(failedAttempts))
    if failedAttempts > 1:
        reconnector.stopService()

def connectionFailed(reason):
    LOG.log("crit", "connection failed: "+str(reason))
    connect_next()

def connect_next():
    global addresses, addresses6, addrs
    if len(addrs) is 0:
        """If we tried all available addresses wait a while and do another lookup"""
        sleep(5)
        address_lookup()
    else:
        sleep(1)
        addresses = []
        addresses6 = []
        addr = addrs.pop()
        LOG.log("info", "connecting to " + host + "[" + addr + "] on port "+str(port) + (" using SSL" if usessl else ""))
        if usessl:
            # Don't verify if noverify is set
            if cafile == "noverify":
                LOG.log("warning", "noverify set, not verifying SSL certificate")
                options = ssl.ClientContextFactory()
            # Verify using platformTrust
            elif not cafile:
                options = ssl.optionsForClientTLS(u'{0}'.format(host))
            # Verify using ca-certificate-file
            else:
                certData = Filehandler().getcontent(cafile)
                authority = ssl.Certificate.loadPEM(certData)
                options = ssl.optionsForClientTLS(u'{0}'.format(host), authority)
            endpoint = endpoints.SSL4ClientEndpoint(reactor, addr, port, options)
            #endpoint.connect(factory)
            #reactor.connectSSL(addr, port, factory, ssl.ClientContextFactory())
        else:
            endpoint = endpoints.TCP4ClientEndpoint(reactor, addr, port)
            #reactor.connectTCP(addr, port, factory)
        
        reconnector = ClientService(endpoint, factory)
        #Workaround for twisted < 17.5.0
        checkFailedLoop = task.LoopingCall(checkFailure, reconnector)
        checkFailedLoop.start(1)
        #waitForConnection = reconnector.whenConnected(failAfterFailures=2)
        waitForConnection = reconnector.whenConnected()
        waitForConnection.addCallback(lambda x: checkFailedLoop.stop())
        waitForConnection.addErrback(lambda reason: [checkFailedLoop.stop(), connectionFailed(reason)])
        reconnector.startService()

def address_lookup():
    address6 = client.lookupIPV6Address(host)
    address6.addCallback(gotAddress6)
    address6.addErrback(address6Failed)

class BotFactory(protocol.ClientFactory):
    """A factory for Bots.
    A new protocol instance will be created each time we connect to the server.
    """

    def __init__(self, channel, nickname, password, 
            mqtthost, mqttport, mqttusessl, mqttcafile, mqtttopic, mqttuser, mqttpassword):
        self.channel = channel
        self.protocol = Bot
        self.nickname = nickname
        self.password = password
        self.mqtthost = mqtthost
        self.mqttport = mqttport
        self.mqttusessl = mqttusessl
        self.mqttcafile = mqttcafile
        self.mqtttopic = mqtttopic
        self.mqttuser = mqttuser
        self.mqttpassword = mqttpassword

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

    #read Serversettings from config file
    parser = SafeConfigParser()

    parser.read('./config/network.cfg')
    host=parser.get('network', 'hostname')

    address_lookup()

    port=parser.getint('network', 'port')
    usessl=parser.getboolean('network', 'ssl')
    nickname=parser.get('network', 'nickname')
    password=parser.get('network', 'password')
    try:
        cafile = parser.get('network', 'cafile') if usessl else ""
    except:
        cafile = None

    #Read channels from config file
    parser.read('./config/channels.cfg')
    channels = parser.items( 'channels' )
    chan_list=[]

    for key, channel in channels:
            chan_list.append(channel)

    #Read mqtt-status settings from config
    parser.read('./config/status.cfg')
    mqtthost=parser.get('status', 'hostname')
    mqttport=parser.getint('status', 'port')
    mqttusessl=parser.getboolean('status', 'ssl')
    mqttcafile=parser.get('status', 'cafile')
    mqtttopic=parser.get('status', 'topic')
    mqttuser=parser.get('status', 'username')
    mqttpassword=parser.get('status', 'password')

    #Factory
    factory = BotFactory(chan_list, nickname, password, 
            mqtthost, mqttport, mqttusessl, mqttcafile, mqtttopic, mqttuser, mqttpassword)


    sig = Signalhandler(factory)
    reactor.addSystemEventTrigger('before', 'shutdown', sig.savestates)

    #run
    LOG.log("info", "starting reactor")
    reactor.run()
