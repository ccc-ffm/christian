import os

class Keys(object):

    def __init__(self, fpath):
        self.keyholders = []
        self.fpath = fpath
        if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
            with open(fpath, 'r') as statefile:
                self.keyholders = [line.strip() for line in statefile]

    def iskeyholder(self, nickname):
        return nickname in self.keyholders

    def addkeyholder(self, nickname):
        self.keyholders.append(nickname)
        self.savestates()

    def removekeyholder(self, nickname):
        self.keyholders.remove(nickname)
        self.savestates()

    def getkeyholders(self):
        for user in self.keyholders:
            yield user

    def savestates(self):
        statefile=open(self.fpath,'w+')
        for user in self.keyholders:
            statefile.write("%s\n" % user)
        statefile.close()
