class AssistanceFunctions(object):

    def pad(self, channel, callback, msg=None, nck=None, pad=None, **kwargs):
        if len(msg) < 1:
            callback.say(channel, 'Syntax: !pad <name> [public]')
        elif msg[1] == 'public':
            pad_url='{0}{1}'.format(pad.getPublicUrl(),msg[0]
            callback.say(channel,pad_url)
        else:
            pad_url='{0}{1}'.format(pad.getPrivateUrl(),msg[0]
            callback.say(channel,pad.url)

    def help(self, channel, callback, msg=None, nck=None, pad=None, **kwargs):
        helpmsg = "!pad <name> [public] - Create a pad named <name> at chaospad.de "
        helpmsg += "When using the argument public the link returned does not contain the pad credentials.\n"
        callback.msg(nck, helpmsg)
