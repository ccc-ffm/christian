class KeyFunctions():

    def __init__(self):
        self.keyholders = []
        #TODO verfiy that file exists
        self.keyfile="./storage/keys.txt"
        with open(self.keyfile, 'r') as keyfile:
            for line in keyfile:
                self.keyholders.append(" ".join(line.split()))

    def ListKeys(self,channel,user,cb):
        """List current holders of hq keys"""
        print("ListKeys")
        keyMessage = "All the keys are belong to: "
        keyMessage += ", ".join(self.keyholders[:-1])
        keyMessage += " & " + self.keyholders[-1]
        cb.msg(user,keyMessage)

    def ChangeKeyholders(self,channel,cb,oldholder,newholder):
        """ Hand one key from an holder to another one """
        if newholder in self.keyholders:
            cb.say(channel, "Noooooo! No more than one key for "+newholder+"!")
            return(False)
        if oldholder in self.keyholders:
            self.keyholders[self.keyholders.index(oldholder)] = newholder
            self.ListKeys(channel,cb)
            with open(self.keyfile, 'w') as keyfile:
                for holder in self.keyholders:
                    print>>keyfile,holder

            return(True)
        else:
            cb.say(channel, oldholder+ " has no key, better luck next time!")
            return(False)

