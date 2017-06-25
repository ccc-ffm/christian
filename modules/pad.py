
class Pad(object):
    def __init__(self, url, user, password, public=True):
        self.url = url
        self.user = user
        self.password = password
        self.public = public

    def getPrivateUrl(self):
        return ("https://{0}:{1}@chaospad.de/p/".format(self.user,self.password))

    def getPublicUrl(self):
        return ("https://chaospad.de/p/")
