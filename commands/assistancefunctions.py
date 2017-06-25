class AssistanceFunctions(object):

    def pad(self, channel, callback, msg=None, nck=None, pad=None, **kwargs):
        if len(msg) < 1:
            callback.say(channel, 'Syntax: !pad <name> [private]')
        elif msg[2] == 'private':
            pad_url='{0}{1}'.format(pad.getPrivateUrl(),msg[1])
            callback.say(channel,pad_url)
        else:
            pad_url='{0}{1}'.format(pad.getPublicUrl(),msg[1])
            callback.say(channel,pad.url)

    def help(self, channel, callback, msg=None, nck=None, pad=None, **kwargs):
        helpmsg = "!pad <name> [private] - Create a pad named <name> at chaospad.de .\ņ"
        helpmsg += "When using the argument private the link returned does not contain the pad credentials .\n"
        callback.msg(nck, helpmsg)
