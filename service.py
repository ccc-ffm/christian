import os

class ServiceFunctions():

    def GetText(self,filename):
        fileCont = ""
        if not os.path.isfile(filename):
            return("Something went terribly wrong, better luck next time!")
        with open(filename, 'r') as inFile:
            for line in inFile:
                fileCont += line.strip() + "\n"
        return fileCont

    def Donnerstag(self,channel,cb):
        cb.say(channel, self.GetText("./mylines/donnerstag.txt"))

    def Help(self, user, channel, cb):
        if channel[1:] == cb.factory.getChannel():
            helpText = self.GetText("./mylines/help.txt")
        else:
            helpText = self.GetText("./mylines/help_public.txt")
        cb.msg(user, helpText, 120)

