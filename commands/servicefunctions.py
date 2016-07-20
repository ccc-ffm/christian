from utils import Filehandler

class ServiceFunctions(object):

    def __init__(self):
        self.fhandler = Filehandler()

    def donnerstag(self, channel, callback, **kwargs):
        """Tell about public meeting"""
        callback.say(channel,
                     self.fhandler.getcontent("./mylines/donnerstag.txt"))
