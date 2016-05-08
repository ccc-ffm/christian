"""Help function class"""

from modules.files import Filehandler

class HelpFunctions(object):
    """Some helper functions"""

    def __init__(self):
        self.fhandler = Filehandler()

    def help(self, user, channel, callback):
        """Paste URLs to help"""
        if channel[1:] == callback.factory.getChannel():
            helptext = self.fhandler.getcontent("./mylines/help.txt")
        else:
            helptext = self.fhandler.getcontent("./mylines/help_public.txt")
        callback.msg(user, helptext, 120)

