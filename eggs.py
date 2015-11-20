"""Some eastereggs just for fun"""
import random, os

class EasterEggs(object):
    """Easter Egg functions"""

    def __init__(self):
        pass

    @classmethod
    def getrandomline(cls, filename):
        """Return a random line from a file"""
        #Random Selection from Jonathan Kupferman:
        #http://www.regexprn.com/2008/11/read-random-line-in-large-file-in.html
        #Open the file:

        my_file = open(filename, 'r')

        #Get the total file size
        file_size = os.stat(filename)[6]

        #seek to a place in the file which is a random distance away
        #Mod by file size so that it wraps around to the beginning
        my_file.seek((my_file.tell()+random.randint(0, file_size-1))%file_size)

        #dont use the first readline since it may fall in the middle of a line
        my_file.readline()

        #this will return the next (complete) line from the file
        line = my_file.readline()
        my_file.close()
        return line

    @classmethod
    def geturl(cls, filename):
        """Read url from filename"""
        my_file = open(filename, 'r')
        url = my_file.readline()
        my_file.close()
        return url


    def darkwing(self, channel, callback):
        """Post a random line"""
        filename = "./mylines/darkwing.txt"
        myline = self.getrandomline(filename)
        callback.say(channel, myline)

    def balu(self, channel, callback):
        """Post a random line"""
        filename = "./mylines/balu.txt"
        myline = self.getrandomline(filename)
        callback.say(channel, myline)

    def raspel(self, channel, callback):
        """Post url to raspel"""
        filename = "./myurls/raspel.url"
        url = self.geturl(filename)
        callback.say(channel, url)


