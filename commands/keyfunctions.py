class KeyFunctions(object):

    def key(self, channel, callback, msg=None, nck=None, keys=None, **kwargs):

        if len(msg) != 2 or ' ' in msg:
            callback.say(channel, "Syntax: !key user0 user1")
        else:
            if keys.iskeyholder(msg[0]) is True:
                if keys.iskeyholder(msg[1]) is False:
                    keys.removekeyholder(msg[0])
                    keys.addkeyholder(msg[1])
                    self.keys(channel, callback, keys)
                else:
                    callback.say(channel, "Only one key for {0}.".format(msg[1]))
            else:
                callback.say(channel, "User {0} has no key.".format(msg[0]))

    def keys(self, channel, callback, keys=None, **kwargs):
        keylist = keys.getkeyholders()
        callback.say(channel,"All the keys are belong to: %s"%", ".join([str(user) for user in keylist]))
