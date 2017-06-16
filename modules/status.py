import paho.mqtt.client as mqtt
import ssl

from utils import BotLog

LOG = BotLog()

class Status(object):

    def __init__(self):
        self.callback = None
        self.status = "unknown"
    
    def connect(self, host, port, usessl, cafile, topic, user, password):
        self.host = host
        self.port = port
        self.topic = topic
        self.user = user
        self.password = password
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        if usessl:
            # Don't verify hostname (Fix This!)
            self.client.tls_insecure_set(True)
            self.client.tls_set(cafile, certfile=None, keyfile=None, cert_reqs=ssl.CERT_REQUIRED,
                        tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
        self.client.username_pw_set(self.user, self.password)
        self.client.connect(self.host, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        LOG.log("info", "Connected to mqtt-broker")
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        LOG.log("info", "Received message from mqtt-broker: " + msg.topic + " " + msg.payload)
        if msg.topic == self.topic:
            if not msg.payload == self.status:
                self.status = msg.payload
                if self.callback:
                    self.callback(self.status)

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status
        self.ignore = True
        self.client.publish(self.topic, self.status) 
