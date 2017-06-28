"""Some eastereggs just for fun"""

import random

from utils import Filehandler, BotLog
from time import time

LOG = BotLog()

class EasterEggFunctions(object):
    """Easter Egg functions"""

    timestamp = 0

    def __init__(self):
        self.fhandler = Filehandler()
        self.timestamp = 0

    def darkwing(self, channel, callback, **kwargs):
        """Post a random line"""
        filename = "./mylines/darkwing.txt"
        punchline = self.fhandler.getrandomline(filename)
        start = "Ich bin der Schrecken der die Nacht durchflattert, ... "
        end = " ... Ich bin Darkwing Duck!"
        callback.say(channel, ''.join([start, punchline.rstrip(), end]))

    def balu(self, channel, callback, **kwargs):
        """Post a random line"""
        filename = "./mylines/balu.txt"
        myline = self.fhandler.getrandomline(filename)
        callback.say(channel, myline)

    def raspel(self, channel, callback, **kwargs):
        """Post url to raspel"""
        filename = "./myurls/raspel.url"
        url = self.fhandler.getcontent(filename)
        callback.say(channel, url)

    def fg(self, channel, callback, msg=None, **kwargs):
        """Frag gnom"""
        if len(msg):
            callback.say(channel, "telegnom: " + (" ".join(msg))[:120])

    def fs(self, channel, callback, msg=None, **kwargs):
        """Frag skorpy"""
        if len(msg):
            callback.say(channel, "skorpy: " + (" ".join(msg))[:120])

    def gud3(self, channel, callback, **kwargs):
        self.gude(channel, callback, **kwargs)

    def gude(self, channel, callback, **kwargs):
        seconds = int(time() - self.timestamp)
        if not self.timestamp or seconds > 120:
            self.timestamp = time()
            """Post ascii-art logo"""
            filename = "./mylines/ascii.txt"
            colors = ["\x02\x0300,12", "\x02\x0304,01"]
            color = random.choice(colors)
            endformat = "\x0F"
            gude = ""
            for line in open(filename, "r"):
                gude += color + line.strip() + endformat + "\n"
            callback.say(channel, gude)
        else:
            LOG.log("info", "Flood protection, ignoring command")
