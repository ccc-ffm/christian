"""Service function class"""
import os

class ServiceFunctions(object):
    """Some helper functions"""

    def __init__(self):
        pass

    @classmethod
    def gettext(cls, filename):
        """Return filecontent"""
        filecont = ""
        if not os.path.isfile(filename):
            return "Something went terribly wrong, better luck next time!"
        with open(filename, 'r') as infile:
            for line in infile:
                filecont += line.strip() + "\n"
        return filecont

    def donnerstag(self, channel, callback):
        """Tell about public meeting"""
        callback.say(channel, self.gettext("./mylines/donnerstag.txt"))

    def help(self, user, channel, callback):
        """Paste URLs to help"""
        if channel[1:] == callback.factory.getChannel():
            helptext = self.gettext("./mylines/help.txt")
        else:
            helptext = self.gettext("./mylines/help_public.txt")
        callback.msg(user, helptext, 120)

