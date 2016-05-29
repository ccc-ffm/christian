import os

class Keys(object):

    def __init__(self):
        fpath = './storage/keys.txt'
        if  not os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
            self.keyholders = []
        else:
            with open('./storage/keys.txt','r') as statefile:
                self.keyholders = [line.strip() for line in statefile]

    def iskeyholder(self, nickname):
        return nickname in self.keyholders

    def addkeyholder(self, nickname):
        self.keyholders.append(nickname)

    def removekeyholder(self, nickname):
        self.keyholders.remove(nickname)

    def getkeyholders(self):
        for user in self.keyholders:
            yield user
