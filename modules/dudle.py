
class Dudle(object):

    def __init__(self):
        self.baseurl = 'https://dudle.inf.tu-dresden.de/?create_poll='

    def getDudle(self, name, type='time', url=''):
        print name
        print type
        print url
        return(self.baseurl + name + '&poll_type=' + type + '&poll_url=' + url)
