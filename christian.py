#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# twisted.words.protocols.irc not ported to python 3 yet m(

#USAGE: ./christian.py Channel

from time import sleep

#twisted imports
from twisted.internet import reactor, protocol, ssl, endpoints, task
from twisted.application.internet import ClientService
from twisted.names import client, dns

#system imports
import sys, os
from ConfigParser import SafeConfigParser

#Import the bots we want to create
from bots import Bot
from utils import BotLog, Signalhandler, Filehandler

from modules import Keys, HQ, Postbox, Friendship

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

    def __init__(self, channel, nickname, password, MQTT_host, MQTT_port,
            MQTT_ssl, MQTT_ca, MQTT_topic, MQTT_user, MQTT_pass, MQTT_id,
            MQTT_bunteslicht, MQTT_sound, MQTT_switch, MQTT_ambientlight,
            MQTT_power, keys, hq, postbox, useraliases, friendship, url_list,
            cmdaliases):
        self.channel = channel
        self.protocol = Bot
        self.nickname = nickname
        self.password = password
        self.MQTT_host = MQTT_host
        self.MQTT_port = MQTT_port
        self.MQTT_ssl = MQTT_ssl
        self.MQTT_ca = MQTT_ca
        self.MQTT_topic = MQTT_topic
        self.MQTT_user = MQTT_user
        self.MQTT_pass = MQTT_pass
        self.MQTT_id = MQTT_id
        self.MQTT_bunteslicht = MQTT_bunteslicht
        self.MQTT_sound = MQTT_sound
        self.MQTT_switch = MQTT_switch
        self.MQTT_ambientlight = MQTT_ambientlight
        self.MQTT_power = MQTT_power
        self.keys = keys
        self.hq = hq
        self.postbox = postbox
        self.useraliases = useraliases
        self.friendship = friendship
        self.url_list = url_list
        self.cmdaliases = cmdaliases

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

    if "--config" in sys.argv:
        config = sys.argv[sys.argv.index("--config") + 1]
    else:
        config = "./config/config.cfg"
    if os.path.isfile(config):
        parser.read(config)
    else:
        LOG.log("error", "Configuration file not found")
        exit(1)

    #parser.read('./config/network.cfg')
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
    #parser.read('./config/channels.cfg')
    channels = parser.items( 'channels' )
    chan_list = {channel: channel_functions.split(",") for channel, channel_functions in channels}

    chan_list_stripped = {}
    for chan, actions in chan_list.iteritems():
        chan_list_stripped[chan] = [x.strip() for x in actions]

    chan_list = chan_list_stripped

    keypath = parser.get('keys', 'path')
    userpath = parser.get('users', 'path')
    quotasize=parser.get('quota', 'size')
    postboxdir=parser.get('postboxpath','path')
    accessfile=parser.get('postboxaccess', 'path')

    useraliases = parser.get('aliases', 'users')
    try:
        cmdaliases = parser.get('aliases', 'commands')
    except:
        cmdaliases = "./config/cmd_aliases"

    #Read mqtt-status settings from config
    #parser.read('./config/status.cfg')
    MQTT_host=parser.get('status', 'hostname')
    MQTT_port=parser.getint('status', 'port')
    MQTT_ssl=parser.getboolean('status', 'ssl')
    MQTT_ca=parser.get('status', 'cafile')
    MQTT_topic=parser.get('status', 'topic')
    MQTT_user=parser.get('status', 'username')
    MQTT_pass=parser.get('status', 'password')
    try:
        MQTT_id = parser.get('status', 'identity')
    except:
        MQTT_id = None
    try:
        MQTT_bunteslicht = parser.get('status', 'bunteslicht')
    except:
        MQTT_bunteslicht = None
    try:
        MQTT_sound = parser.get('status', 'sound')
    except:
        MQTT_sound = None
    try:
        MQTT_switch = parser.get('status', 'switch')
    except:
        MQTT_switch = None
    try:
        MQTT_ambientlight = parser.get('status', 'ambientlight')
    except:
        MQTT_ambientlight = None
    try:
        MQTT_power = parser.get('status', 'power')
    except:
        MQTT_power = None

    #Read pad settings from file
    pad_url=parser.get('pad', 'url')
    pad_user=parser.get('chaos-credentials', 'user')
    pad_password=parser.get('chaos-credentials','password')

    chaos_urls = parser.get('chaos-urls', 'urls')
    url_list = chaos_urls.split(",")
    url_list_stripped = [x.strip() for x in url_list]

    url_list = url_list_stripped

    #Factory
    factory = BotFactory(chan_list, nickname, password, MQTT_host, MQTT_port,
            MQTT_ssl, MQTT_ca, MQTT_topic, MQTT_user, MQTT_pass, MQTT_id,
            MQTT_bunteslicht, MQTT_sound, MQTT_switch, MQTT_ambientlight,
            MQTT_power, Keys(keypath), HQ(userpath, keypath),
            Postbox(postboxdir, quotasize, accessfile), useraliases,
            Friendship(pad_url,pad_user,pad_password), url_list,
            cmdaliases)

    sig = Signalhandler(factory)
    reactor.addSystemEventTrigger('before', 'shutdown', sig.savestates)

    #run
    LOG.log("info", "starting reactor")
    reactor.run()
