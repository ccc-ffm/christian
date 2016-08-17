"""Help function class"""

from utils import Filehandler

class HelpFunctions(object):

    def __init__(self):
        self.fhandler = Filehandler()

    def help(self, channel, callback, nck=None, **kwargs):
        if channel == '#ccc-ffm-intern':
            helptext = self.fhandler.getcontent("./mylines/help.txt")
            callback.msg(nck, helptext, 120)
        elif channel == '#ccc-ffm':
            helptext = self.fhandler.getcontent("./mylines/help_public.txt")
            callback.msg(nck, helptext, 120)
        elif channel == '#ccc-ffm-vorstand':
            helptext = self.fhandler.getcontent("./mylines/help_vorstand.txt")
            callback.msg(nck, helptext, 120)
        elif channel == '#ccc-ffm-infra':
            helptext = self.fhandler.getcontent("./mylines/help_infra.txt")
            callback.msg(nck, helptext, 120)
        else:
            return None
