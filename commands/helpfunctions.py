"""Help function class"""

class HelpFunctions(object):

    def help(self, channel, callback, nck=None, **kwargs):
        callback.msg(nck, "usage: [command] [arg]\n")
