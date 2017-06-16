
class Signalhandler(object):

    def __init__(self, factory):
        self.factory = factory
        self.keyfile = './storage/keys.txt'
        self.userfile = './storage/users.txt'

    def savestates(self):
        keyholders = self.factory.protocol.keys.keyholders
        userset = self.factory.protocol.hq.joined_users

        statefile=open(self.keyfile,'w+')
        for user in keyholders:
            statefile.write("%s\n" % user)
        statefile.close()

        userfile=open(self.userfile,'w+')
        for user in userset:
            userfile.write("%s\n" % user)
        userfile.close()
