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

    def help(self, user, channel, callback):
        """Paste URLs to help"""
        if channel[1:] == callback.factory.getChannel():
            helptext = self.fhandler.getcontent("./mylines/help.txt")
        else:
            helptext = self.fhandler.getcontent("./mylines/help_public.txt")
        callback.msg(user, helptext, 120)

