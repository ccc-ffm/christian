import time
import os
from ConfigParser import SafeConfigParser

class Postbox(object):

    def __init__(self):
        parser = SafeConfigParser()

        parser.read('./config/postbox.cfg')
        self.quotasize=parser.get('quota', 'size')

    def savemessage(self,sender,receipient,msg):
        """Delete too big postboxes"""
        if os.path.isfile('./postbox/%s' %receipient):
            if os.path.getsize('./postbox/%s' %receipient) > self.quotasize:
                os.remove('./postbox/%s' %receipient)

        with open('./postbox/%s' %receipient,'ab+') as postbox:
            msgtime = time.strftime("%Y-%m-%d %H-%M")
            msgstr = ' '.join(str(part) for part in msg)
            text = 'From '+sender+'@'+msgtime+': '+msgstr+'\n'
            postbox.write(text)
            postbox.close()


    def hasmessage(self,user):
        return os.path.exists('./postbox/%s' %user)

    def replaymessage(self,user,callback):
        with open('./postbox/%s' %user, 'r') as postbox:
            callback.msg(user,postbox.read(),128)
        self.removepostbox(user)

    def removepostbox(self,user):
        os.remove('./postbox/%s' %user)
