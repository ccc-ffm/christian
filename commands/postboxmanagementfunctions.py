from utils import Filehandler

class PostboxMgmtFunctions(object):

    def __init__(self):
        self.fhandler = Filehandler()

    def postbox(self, channel, callback, msg=None, nck=None, hq=None, keys=None, pb=None):

        knowncommands = ['add','del','list']

        if msg[0] not in knowncommands:
            callback.say(channel, 'Syntax: !postbox add|del|list [user]')
            return

        else:
            if msg[0] == 'add':
                if self.fhandler.onaccesslist(msg[1]):
                    callback.say(channel, '{0} already has a mailbox'.format(msg[1]))
                else:
                    self.fhandler.addtoaccesslist(msg[1])
                    if self.fhandler.onaccesslist(msg[1]):
                        callback.say(channel, 'Created mailbox for {0}'.format(msg[1]))
                    else:
                        callback.say(channel, 'Failed to create mailbox')

            elif msg[0] == 'del':
                if not self.fhandler.onaccesslist(msg[1]):
                    callback.say(channel, '{0} has no mailbox'.format(msg[1]))
                else:
                    self.fhandler.deletefromaccesslist(msg[1])
                    if not self.fhandler.onaccesslist(msg[1]):
                        callback.say(channel, 'Deleted mailbox for {0}'.format(msg[1]))
                    else:
                        callback.say(channel, 'Failed to delete mailbox')
            elif msg[0] == 'list':
                if len(msg) > 1:
                    if self.fhandler.onaccesslist(msg[1]):
                        callback.say(channel, '{0} already has Mailbox'.format(msg[1]))
                    else:
                        callback.say(channel, '{0} has no Mailbox'.format(msg[1]))
                else:
                    callback.say(channel, 'Syntax: !postbox list user')
