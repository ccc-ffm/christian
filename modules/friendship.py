
class Friendship(object):
    def __init__(self, url, user, password, public=True):
        self.url = url
        self.user = user
        self.password = password
        self.public = public

    def getPrivateUrl(self, url=None):
        if not url:
            url = self.url
        proto, address = url.split("//")
        return ((proto + "//{0}:{1}@" + address).format(self.user,self.password))

    def getPublicUrl(self):
        return (self.url)
