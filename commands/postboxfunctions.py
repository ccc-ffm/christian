from utils import Filehandler

class PostboxFunctions(object):

    def __init__(self):
        self.fhandler = Filehandler()

    def tell(self, channel, callback, msg=None, nck=None, hq=None, keys=None, pb=None):
        if len(msg) < 2:
            callback.say(channel,'{0}: Try !tell receipient message'.format(nck))

        else:
            receipient = msg[0]
            try:
                if self.fhandler.onaccesslist(receipient):
                    pb.savemessage(nck,receipient,msg[1:])
                    callback.say(channel, 'Message saved')
                else:
                    callback.say(channel,'Unknown user {0}'.format(receipient))
            except:
                raise Exception('Could not save message.')
