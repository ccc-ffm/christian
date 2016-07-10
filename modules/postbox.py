import time
import os
from ConfigParser import SafeConfigParser

class Postbox(object):

    parser = SafeConfigParser()
    parser.read('./config/postbox.cfg')
    quotasize=parser.get('quota', 'size')
    postboxdir=parser.get('postboxpath','path')

    def savemessage(self,sender,receipient,msg):
        """Delete too big postboxes"""
        if os.path.isfile(self.postboxdir + receipient):
            if os.path.getsize(self.postboxdir + receipient) > self.quotasize:
                os.remove(self.postboxdir + receipient)


        with open( self.postboxdir+receipient,'ab+') as postbox:
            msgtime = time.strftime("%Y-%m-%d %H-%M")
            msgstr = ' '.join(str(part) for part in msg)
            text = 'From '+sender+'@'+msgtime+': '+msgstr+'\n'
            postbox.write(text)

    def hasmessage(self,user):
        return os.path.exists(self.postboxdir + user)

    def replaymessage(self,user,callback):
        with open(self.postboxdir+user, 'r') as postbox:
            callback.msg(user,postbox.read(),128)
        self.removepostbox(user)

    def removepostbox(self,user):
        os.remove(self.postboxdir + user)
