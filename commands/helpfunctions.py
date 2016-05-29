"""Help function class"""

from utils import Filehandler

class HelpFunctions(object):

    def __init__(self):
        fhandler = Filehandler()

    def help(self, channel, callback, msg=None, nck=None, hq=None, keys=None, pb=None):
        if channel == '#ccc-ffm-intern':
            helptext = self.fhandler.getcontent("./mylines/help.txt")
            callback.msg(nck, helptext, 120)
        elif channel == '#ccc-ffm':
            helptext = self.fhandler.getcontent("./mylines/help_public.txt")
            callback.msg(nck, helptext, 120)
        elif channel == '#ccc-ffm-vorstand':
            pass
        elif channel == '#ccc-ffm-infra':
            pass
        else:
            return None
