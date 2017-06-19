import time
import os
from ConfigParser import SafeConfigParser

class Postbox(object):

    def __init__(self, postboxdir, quotasize, accessfile):
        self.postboxdir = postboxdir
        self.quotasize = quotasize
        self.accessfile = accessfile

    def savemessage(self,sender,receipient,msg):
        """Delete too big postboxes""" #Is this really the best way? shouldn't we just ignore new messages until the pox has been cleared?
        if os.path.isfile(self.postboxdir + receipient):
            if os.path.getsize(self.postboxdir + receipient) > self.quotasize:
                os.remove(self.postboxdir + receipient)

        receipient = receipient.translate(None,'./')
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
