class KeyFunctions(object):

    def key(self, channel, callback, msg=None, nck=None, hq=None, keys=None, pb=None):

        if len(msg) != 2:
            callback.say(channel, "{0}: Try !key user0 user1".format(nck))
        else:
            if keys.iskeyholder(msg[0]) is True:
                if keys.iskeyholder(msg[1]) is False:
                    keys.removekeyholder(msg[0])
                    keys.addkeyholder(msg[1])
                    self.keys(channel, callback, msg, nck, hq, keys)
                else:
                    callback.say(channel, "Only one key for {0}.".format(msg[1]))
            else:
                callback.say(channel, "User {0} has no key.".format(msg[0]))

    def keys(self, channel, callback, msg=None, nck=None, hq=None, keys=None, pb=None):
        keylist = keys.getkeyholders()
        callback.say(channel,"All the keys are belong to: %s"%", ".join([str(user) for user in keylist]))
        for user in  keylist:
            print user
