
class Pad(object):
    def __init__(self, url, user, password, public=True):
        self.url = url
        self.user = user
        self.password = password
        self.public = public

    def getPrivateUrl(self):
        proto, address = self.url.split("//")
        return ((proto + "//{0}:{1}@" + address).format(self.user,self.password))

    def getPublicUrl(self):
        return (self.url)
