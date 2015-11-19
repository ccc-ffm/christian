from datetime import datetime
import sys

class HQ():
    # set fallback status
    isopen = "unknown"

    # list of valid states in which the hq may be left behind
    validStatuses = ["open", "closed", "private"]

    # set time format string
    timeFormat = "%Y-%m-%d %H:%M"

    # set fallback status since
    statusSince = datetime.now().strftime(timeFormat)

    # initialise list of people currently present in the hq
    people = []

    def __init__(self):
        # load last status from file
        with open("./storage/hq.txt") as hqF:
            self.isopen = hqF.readline().strip()
            self.statusSince = hqF.readline().strip()
        sys.stderr.write(self.isopen + "\n")
        sys.stderr.write(self.statusSince + "\n")

        # if status open or private load people from file
        with open("./storage/people.txt") as peopleF:
            for people in peopleF:
                self.people.append(people.strip())
            sys.stderr.write(" - ".join(self.people))

    def SetStatus(self, status):
        time = datetime.now().strftime(self.timeFormat)
        with open("./storage/hq.txt", "w") as hqF:
            if status in ["open", "private", "closed"]:
                hqF.write(status)
                self.isopen = status
            else:
                hqF.write("unknown")
                self.isopen = "unknown"
            hqF.write("\n")
            hqF.write(time)


    def Join(self,channel,cb,users):
        # group already joined users in on message
        for user in users:
            if user in self.people:
                cb.say(channel,user+" is already here!")
            else:
              self.people.append(user)
              with open("./storage/people.txt", "a") as peopleF:
                  peopleF.write(user+"\n")


    def Leave(self,channel,cb,users):
        # group not present users in on message
        for user in users:
            if user in self.people:
                self.people.remove(user)
                with open("./storage/people.txt", "w") as peopleF:
                    for people in self.people:
                        peopleF.write(people+"\n")
            else:
                cb.say(channel,user+" is not here!")

    def Whois(self,channel,cb):
        if not self.people:
            cb.say(channel,"No one is here!")
        else:
            userset = set(self.people)
            if len(self.people) == 1:
                say = ', '.join(userset) +" is here!"
            else:
                say = ', '.join(userset) +" are here!"
            cb.say(channel,say)

    def OpenHQ(self,channel,cb):
        """This changes the channel topic"""
        print "Open"
        if self.isopen != "open":
            #Get Time:
            time = datetime.now().strftime(self.timeFormat)
            self.SetStatus("open")
            cb.say(channel,"HQ is open since: " + time)
            #Set Topic
            cb.topic(channel,"HQ is open since: " + time)

    def PrivateHQ(self,channel,cb):
        """This changes the channel topic"""
        print "Private"
        if self.isopen != "private":
            #Get Time:
            time = datetime.now().strftime(self.timeFormat)
            self.SetStatus("private")
            cb.say(channel,"HQ is open for members only since: " + time)
            #Set Topic
            cb.topic(channel,"HQ is open for members only since: " + time)
    def CloseHQ(self, channel, cb):
	print "Close"
        """This changes the channel topic"""
        if self.isopen != "closed" :
            self.SetStatus("closed")
            cb.say(channel, "HQ is closed!")
            #Set Topic
            cb.topic(channel,"HQ is closed!")
            with open ("./storage/people.txt", "w") as peopleF:
                peopleF.write("")
            self.people = []

