
class Signalhandler(object):

    def __init__(self, factory):
        self.factory = factory
        self.keyfile = './storage/keys.txt'

    def savestates(self):
        keyholders = self.factory.protocol.keys.keyholders

        statefile=open(self.keyfile,'w+')
        for user in keyholders:
            statefile.write("%s\n" % user)
        statefile.close()
