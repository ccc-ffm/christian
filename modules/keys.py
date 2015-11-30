"""Mange the physical keys"""

class Keyfunctions(object):
    """Class for all key related stuff"""
    def __init__(self):
        self.keyholders = []
        #TODO verfiy that file exists
        self.keyfile = "./storage/keys.txt"
        with open(self.keyfile, 'r') as keyfile:
            for line in keyfile:
                self.keyholders.append(" ".join(line.split()))

    def iskeyholder(self, nickname):
        """Check if person owns a key"""
        return nickname in self.keyholders

    def listkeys(self, user, callback):
        """List current holders of hq keys"""
        keymessage = "All the keys are belong to: "
        keymessage += ", ".join(self.keyholders[:-1])
        keymessage += " & " + self.keyholders[-1]
        callback.msg(user, keymessage)

    def changekeyholders(self, channel, callback, oldholder, newholder):
        """ Hand one key from an holder to another one """
        if newholder in self.keyholders:
            callback.say(channel, "Noooooo! No more than one key for "\
                    +newholder+"!")
            return False

        if oldholder in self.keyholders:
            self.keyholders[self.keyholders.index(oldholder)] = newholder
            self.listkeys(channel, callback)
            with open(self.keyfile, 'w') as keyfile:
                for holder in self.keyholders:
                    print>>keyfile, holder

            return True

        else:
            callback.say(channel, oldholder+ \
                    " has no key, better luck next time!")
            return False
