"""Provide Postbox for absent users"""

import time
import os

class Postbox(object):

    def savemessage(self,sender,receipient,msg):
        with open('./postbox/%s',receipient) as postbox:
            time = time.strftime("%Y-%m-%d %H-%M")
            text = 'From '+sender+' @ '+time+": "+msg
            postbox.append(text)
            pstbox.close()


    def hasmessage(self,user):
        return os.stat('./postbox/%s').st_size == 0

    def replaymessageforuser(self,user,callback):
        with open('./postbox/%s',user) as postbox:
            callback.msg(user,postbox.read().replace('\n', ''),128)



