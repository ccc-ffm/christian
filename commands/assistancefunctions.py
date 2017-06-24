class AssistanceFunctions(object):

    def pad(self, channel, callback, msg=None, nck=None, pad=None, **kwargs):
        if len(msg) < 1:
            callback.say(channel, "Syntax: !pad <name> [private]")
        elif msg[2] == 'private':
            pad_url='{0}{1}'.format(pad.getPrivateUrl(),msg[1])
            callback.say(channel,pad_url)
        else:
            pad_url='{0}{1}'.format(pad.getPublicUrl(),msg[1])
            callback.say(channel,pad.url)
