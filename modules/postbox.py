"""Provide Postbox for absent users"""

import time
import os

class Postbox(object):

    def savemessage(self,sender,receipient,msg):
        with open('./postbox/%s' %receipient,'ab+') as postbox:
            msgtime = time.strftime("%Y-%m-%d %H-%M")
            msgstr = ' '.join(str(part) for part in msg)
            text = 'From '+sender+'@'+msgtime+": "+msgstr+"\n"
            postbox.write(text)
            postbox.close()


    def hasmessage(self,user):
        return os.stat('./postbox/%s').st_size == 0

    def replaymessageforuser(self,user,callback):
        with open('./postbox/%s' % user, 'r') as postbox:
            callback.msg(user,postbox.read().replace('\n', ''),128)


