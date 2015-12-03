"""Provides logging for modules and Botcor"""
import datetime, sys, syslog

class BotLog(object):
    """Logging class"""

    facility = syslog.LOG_LOCAL0
    logid = "christian"
    def __init__(self):
        if "--debug" in sys.argv:
            self.debugmode = True
        else:
            self.debugmode = False
        syslog.openlog(self.logid, 0, syslog.LOG_LOCAL0)

    def log(self, prio, mesg):
        """Write to log"""
        if self.debugmode == True:
            time = datetime.datetime.today().strftime('%Y-%m-%dT%H-%M-%S')
            print time + ": " + mesg
        if prio in ["emerg", "alert", "crit", "err", "warning", \
                "notice", "info", "debug",]:
            if prio == "emerg":
                prio = syslog.LOG_EMERG
            elif prio == "alert":
                prio = syslog.LOG_ALERT
            elif prio == "crit":
                prio = syslog.LOG_CRIT
            elif prio == "err":
                prio = syslog.LOG_ERR
            elif prio == "warning":
                prio = syslog.LOG_WARNING
            elif prio == "notice":
                prio = syslog.LOG_NOTICE
            elif prio == "info":
                prio = syslog.LOG_INFO
            elif prio == "debug":
                prio = syslog.LOG_DEBUG
            syslog.syslog(prio, mesg)
        else:
            #if no valid prio was specified, log error
            syslog.syslog(syslog.LOG_ERR, "Unknown loglevel '" + prio \
                    + "' with message '" + mesg + "'")

    def debug(self, mesg):
        """Print to Stdout if debugging is enabled"""
        if self.debugmode == True:
            time = datetime.datetime.today().strftime('%Y-%m-%dT%H-%M-%S')
            print time + ": " + mesg
