from utils import Filehandler

class ServiceFunctions(object):

    def __init__(self):
        self.fhandler = Filehandler()

    def help(self, channel, callback, msg=None, nck=None, hq=None, keys=None, **kwargs):
        helpmsg = "!donnerstag - Tell something about our public meeting.\n"
        helpmsg += "!status - Get current status of HQ.\n"
        callback.msg(nck, helpmsg)

    def donnerstag(self, channel, callback, hq=None, **kwargs):
        """Tell about public meeting"""
        callback.say(channel,
                     self.fhandler.getcontent("./mylines/donnerstag.txt"))

    def status(self, channel, callback, hq=None, **kwargs):
        """
        Get HQ status
        """
        hqcolor = "04"
        hqstatus = "unknown"
        if hq.status.status == "open":
            hqcolor = "03"
            hqstatus = "open"
        elif hq.status.status == "private" or hq.status.status == "closed":
            hqstatus = "closed"
        message = "HQ is currently " + "\x02\x03" + hqcolor + hqstatus + "\x03\x02\x0F" + "\n"
        callback.msg(channel, message)
