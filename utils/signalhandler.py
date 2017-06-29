
class Signalhandler(object):

    def __init__(self, factory):
        self.factory = factory

    def savestates(self):
        self.factory.keys.savestates()

        self.factory.hq.savestates()
