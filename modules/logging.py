from syslog import *
import datetime, sys

class BotLog():
    facility = LOG_LOCAL0
    logid = "christian"
    def __init__(self):
        if "--debug" in sys.argv:
            self.debugmode = True
        else:
            self.debugmode = False
        openlog(self.logid,0,LOG_LOCAL0)

    def log(self, prio, mesg):
        if self.debugmode == True:
            time = datetime.datetime.today().strftime('%Y-%m-%dT%H-%M-%S')
            print(time + ": " + mesg)
        if prio in ["emerg", "alert", "crit", "err", "warning", "notice", "info", "debug",]:
            if prio == "emerg":
                prio = LOG_EMERG
            elif prio == "alert":
                prio = LOG_ALERT
            elif prio == "crit":
                prio = LOG_CRIT
            elif prio == "err":
                prio = LOG_ERR
            elif prio == "warning":
                prio = LOG_WARNING
            elif prio == "notice":
                prio = LOG_NOTICE
            elif prio == "info":
                prio = LOG_INFO
            elif prio == "debug":
                prio = LOG_DEBUG
            syslog(prio, mesg)
        else:
            #if no valid prio was specified, log error
            syslog(LOG_ERR, "Unknown loglevel '" + prio + "' with message '" + mesg + "'")

    def debug(self, mesg):
        if self.debugmode == True:
            time = datetime.datetime.today().strftime('%Y-%m-%dT%H-%M-%S')
            print(time + ": " + mesg)
