from syslog import *

class BotLog():
    debug = False
    facility = LOG_LOCAL0
    logid = "christian"
    def __init__(self, debugmode):
        openlog(self.logid,0,LOG_LOCAL0)
        if debugmode == True:
            self.debug = True
            syslog(LOG_DEBUG, "debugmode enabled")

    def log(self, prio, mesg):
        if self.debug == True:
            prio = "debug"
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
                print(mesg)
            syslog(prio, mesg)
        else:
            #if no valid prio was specified, log error
            syslog(LOG_ERR, "Unknown loglevel '" + prio + "' with message '" + mesg + "'")
