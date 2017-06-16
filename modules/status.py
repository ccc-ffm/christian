import paho.mqtt.client as mqtt
import ssl

from utils import BotLog

LOG = BotLog()

class Status(object):

    def __init__(self):
        self.callback = None
        self.status = self.bunteslicht_s = self.sound_s = self.switch_s = self.ambientlight_s = self.power_s = "unknown"
    
    def connect(self, host, port, usessl, cafile, topic, user, password,
            identity, bunteslicht, sound, switch, ambientlight, power):
        self.host = host
        self.port = port
        self.topic = topic
        self.bunteslicht = bunteslicht
        self.sound = sound
        self.switch = switch
        self.ambientlight = ambientlight
        self.power = power
        self.user = user
        self.password = password
        self.identity = identity
        self.client = mqtt.Client(client_id=identity)
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

    def disconnect(self):
        self.client.loop_stop()
        self.client.disconnect()

    def on_connect(self, client, userdata, flags, rc):
        LOG.log("info", "Connected to mqtt-broker")
        self.client.subscribe(self.topic)
        self.client.subscribe(self.bunteslicht)
        self.client.subscribe(self.sound)
        self.client.subscribe(self.switch)
        self.client.subscribe(self.ambientlight)
        self.client.subscribe(self.power)

    def on_message(self, client, userdata, msg):
        LOG.log("info", "Received message from mqtt-broker: " + msg.topic + " " + msg.payload)
        if msg.topic == self.topic:
            if not msg.payload == self.status:
                self.status = msg.payload
                if self.callback:
                    self.callback(self.status)
        elif msg.topic == self.bunteslicht:
            if not msg.payload == self.bunteslicht_s:
                self.bunteslicht_s = msg.payload
        elif msg.topic == self.sound:
            if not msg.payload == self.sound_s:
                self.sound_s = msg.payload
        elif msg.topic == self.switch:
            if not msg.payload == self.switch_s:
                self.switch_s = msg.payload
        elif msg.topic == self.ambientlight:
            if not msg.payload == self.ambientlight_s:
                self.ambientlight_s = msg.payload
        elif msg.topic == self.power:
            if not msg.payload == self.power_s:
                self.power_s = msg.payload

    def getStatus(self):
        return self.status

    def setStatus(self, status):
        self.status = status
        self.client.publish(self.topic, self.status) 
