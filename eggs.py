import random,os

class EasterEggs():

    def GetRandomLine(self,filename):

        #Random Selection from Jonathan Kupferman:
        #http://www.regexprn.com/2008/11/read-random-line-in-large-file-in.html
        #Open the file:

        file = open(filename,'r')

        #Get the total file size
        file_size = os.stat(filename)[6]

        #seek to a place in the file which is a random distance away
        #Mod by file size so that it wraps around to the beginning
        file.seek((file.tell()+random.randint(0,file_size-1))%file_size)

        #dont use the first readline since it may fall in the middle of a line
        file.readline()

        #this will return the next (complete) line from the file
        line = file.readline()
        file.close()
        return line


    def GetURL(self,filename):
        file = open(filename,'r')
        url = file.readline()
        file.close()
        return url


    def DarkWing(self,channel,cb):
        filename = "./mylines/darkwing.txt"
        myline = self.GetRandomLine(filename)
        cb.say(channel,myline)

    def Balu(self,channel,cb):
        filename = "./mylines/balu.txt"
        myline = self.GetRandomLine(filename)
        cb.say(channel,myline)

    def Raspel(self,channel,cb):
        filename = "./myurls/raspel.url"
        url = self.GetURL(filename)
        cb.say(channel,url)


