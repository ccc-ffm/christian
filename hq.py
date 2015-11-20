"""Class for setting HQ states"""
from datetime import datetime
import sys

class HQ(object):
    """Set states, join and leave people"""
    # set fallback status
    isopen = "unknown"

    # list of valid states in which the hq may be left behind
    validStatuses = ["open", "closed", "private"]

    # set time format string
    timeFormat = "%Y-%m-%d %H:%M"

    # set fallback status since
    statussince = datetime.now().strftime(timeFormat)

    # initialise list of people currently present in the hq
    people = []

    def __init__(self):
        # load last status from file
        with open("./storage/hq.txt") as hqf:
            self.isopen = hqf.readline().strip()
            self.statussince = hqf.readline().strip()
        sys.stderr.write(self.isopen + "\n")
        sys.stderr.write(self.statussince + "\n")

        # if status open or private load people from file
        with open("./storage/people.txt") as peoplef:
            for people in peoplef:
                self.people.append(people.strip())
            sys.stderr.write(" - ".join(self.people))

    def setstatus(self, status):
        """Set hq status"""
        time = datetime.now().strftime(self.timeFormat)
        with open("./storage/hq.txt", "w") as hqf:
            if status in ["open", "private", "closed"]:
                hqf.write(status)
                self.isopen = status
            else:
                hqf.write("unknown")
                self.isopen = "unknown"
            hqf.write("\n")
            hqf.write(time)


    def join(self, channel, callback, users):
        """Join user to hq"""
        # group already joined users in on message
        for user in users:
            if user in self.people:
                callback.say(channel, user+" is already here!")
            else:
                self.people.append(user)
                with open("./storage/people.txt", "a") as peoplef:
                    peoplef.write(user+"\n")


    def leave(self, channel, callback, users):
        """Leave user from hq"""
        # group not present users in on message
        for user in users:
            if user in self.people:
                self.people.remove(user)
                with open("./storage/people.txt", "w") as peoplef:
                    for people in self.people:
                        peoplef.write(people+"\n")
            else:
                callback.say(channel, user+" is not here!")

    def whois(self, channel, callback):
        """List all people who are at the hq"""
        if not self.people:
            callback.say(channel, "No one is here!")
        else:
            userset = set(self.people)
            if len(self.people) == 1:
                say = ', '.join(userset) +" is here!"
            else:
                say = ', '.join(userset) +" are here!"
            callback.say(channel, say)

    def openhq(self, channel, callback):
        """This changes the channel topic"""
        print "Open"
        if self.isopen != "open":
            #Get Time:
            time = datetime.now().strftime(self.timeFormat)
            self.setstatus("open")
            callback.say(channel, "HQ is open since: " + time)
            #Set Topic
            callback.topic(channel, "HQ is open since: " + time)

    def privatehq(self, channel, callback):
        """This changes the channel topic to open for members only"""
        print "Private"
        if self.isopen != "private":
            #Get Time:
            time = datetime.now().strftime(self.timeFormat)
            self.setstatus("private")
            callback.say(channel, "HQ is open for members only since: " + time)
            #Set Topic
            callback.topic(channel, "HQ is open for members only since: "\
                    + time)

    def closehq(self, channel, callback):
        """This changes the channel topic to close"""
        if self.isopen != "closed":
            self.setstatus("closed")
            callback.say(channel, "HQ is closed!")
            #Set Topic
            callback.topic(channel, "HQ is closed!")
            with open("./storage/people.txt", "w") as peoplef:
                peoplef.write("")
            self.people = []

