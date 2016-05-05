"""Service function class"""

from modules.files import Filehandler

class ServiceFunctions(object):
    """Some helper functions"""

    def __init__(self):
        self.fhandler = Filehandler()

    def donnerstag(self, channel, callback):
        """Tell about public meeting"""
        callback.say(channel, \
                self.fhandler.getcontent("./mylines/donnerstag.txt"))
