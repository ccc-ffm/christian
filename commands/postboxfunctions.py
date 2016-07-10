from utils import Filehandler
from ConfigParser import SafeConfigParser

class PostboxFunctions(object):

    def __init__(self):
        self.fhandler = Filehandler()

    def tell(self, channel, callback, msg=None, nck=None, hq=None, keys=None, pb=None):
        parser = SafeConfigParser()
        parser.read('./config/postbox.cfg')
        accessfile=parser.get('postboxaccess', 'path')

        if len(msg) < 2:
            callback.say(channel,'Syntax: !tell [receipient] [message]')

        else:
            receipient = msg[0]
            try:
                mbstatus=self.fhandler.onaccesslist(receipient, accessfile)
                if mbstatus == 1:
                    pb.savemessage(nck,receipient,msg[1:])
                    callback.say(channel, 'Message saved')
                else:
                    callback.say(channel,'Unknown user {0}'.format(receipient))
            except:
                raise Exception('Could not save message.')
