from utils import Filehandler
from ConfigParser import SafeConfigParser
import re

class PostboxFunctions(object):

    def __init__(self):
        self.fhandler = Filehandler()

    def help(self, channel, callback, msg=None, nck=None, hq=None, keys=None, **kwargs):
        helpmsg = "!tell <user> - Store message in <user>s postbox.\n"
        callback.msg(nck, helpmsg)

    def tell(self, channel, callback, msg=None, nck=None, pb=None, **kwargs):
        try:
            parser = SafeConfigParser()
            parser.read('./config/config.cfg')
            accessfile=parser.get('postboxaccess', 'path')
        except:
            raise Exception('Failed to read the config')

        if len(msg) < 2:
            callback.say(channel,'Syntax: !tell [receipient] [message]')

        else:
            try:
                receipient = msg[0]
                mbstatus=self.fhandler.onaccesslist(receipient, accessfile)
                if mbstatus == 1:
                    msgstring=" ".join(msg[1:])
                    if re.search('[a-zA-Z0-9]+',msgstring) is not None:
                        #strip away / and .. from message
                        msgstring = msgstring.translate(None, './')
                        pb.savemessage(nck,receipient,msgstring)
                        callback.say(channel, 'Message saved')
                    else:
                        callback.say(channel, 'Message can\'t be empty')
                else:
                    callback.say(channel,'Unknown user {0}'.format(receipient))
            except:
                raise Exception('Could not save message.')
