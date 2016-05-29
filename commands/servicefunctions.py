from utils import Filehandler

class ServiceFunctions(object):
    """Some helper functions"""

    def __init__(self):
        self.fhandler = Filehandler()

    def donnerstag(self, channel, callback, msg=None, nck=None, hq=None, keys=None, pb=None):
        """Tell about public meeting"""
        callback.say(channel, \
                self.fhandler.getcontent("./mylines/donnerstag.txt"))
