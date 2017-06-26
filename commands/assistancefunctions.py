from modules import Dudle

class AssistanceFunctions(object):

    def pad(self, channel, callback, msg=None, nck=None, friendship=None, **kwargs):
        if len(msg) < 1:
            callback.say(channel, 'Syntax: !pad <name> [public]')
        elif len(msg) > 1 and msg[1] == 'public':
            pad_url='{0}{1}'.format(friendship.getPublicUrl(),msg[0])
            callback.say(channel,pad_url)
        else:
            pad_url='{0}{1}'.format(friendship.getPrivateUrl(),msg[0])
            callback.say(channel,pad_url)

    def dudle(self, channel, callback, msg=None, nck=None, friendship=None, **kwargs):
        type = 'time'
        url = ''
        if len(msg) < 1:
            callback.say(channel, 'Syntax: !dudle <name> [time|normal] [url]')
        else:
            if(len(msg) > 1) and msg[1] == 'normal':
                type = 'normal'
            if len(msg) > 2:
                url = msg[2]
            callback.say(channel, Dudle().getDudle(msg[0], type, url))

    def help(self, channel, callback, msg=None, nck=None, friendship=None, **kwargs):
        helpmsg = "!pad <name> [public] - Create a pad named <name> at chaospad.de.\n"
        helpmsg += "\tThe optional argument `public` causes the link to be returned without credentials.\n"
        helpmsg += "!dudle <name> [time|normal] [url] - Create a dudle named <name> at dudle.inf.tu-dresden.de.\n"
        helpmsg += "\tThe first optional argument defaults to `time`.\n"
        helpmsg += "\tThe second optional argument defines a custom url.\n"
        callback.msg(nck, helpmsg)
