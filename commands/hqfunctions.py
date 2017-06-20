"""Class for setting HQ states"""
from datetime import datetime
import sys

from modules import InternTopic

class HQFunctions(object):


    def help(self, channel, callback, msg=None, nck=None, hq=None, keys=None, **kwargs):
        helpmsg = "!join [<user> ...  <user>] - Join users to HQ. Joins yourself if no argument is given.\n"
        helpmsg += "!leave [<user> ... <user>] - Leave users. Leaves yourself if no argument is given.\n"
        helpmsg += "!whois - List people in HQ.\n"
        helpmsg += "!open - Set HQ status to open.\n"
        helpmsg += "!private - Set HQ status to private.\n"
        helpmsg += "!close - Set HQ status to closed.\n"
        helpmsg += "!dirty - Set HQ to dirty.\n"
        helpmsg += "!clean - Set HQ to clean.\n"
        helpmsg += "!status - Display status of HQ.\n"
        callback.msg(nck, helpmsg)

    def join(self, channel, callback, msg=None, nck=None, hq=None, keys=None, **kwargs):
        """
        Join users to HQ, update the status
        """
        #Open HQ for members if it is closed
        if hq.hq_status is 'closed' or hq.hq_status is 'unknown':
            self.private(channel, callback, msg, nck, hq, keys)

        if len(msg) == 0:
            msg.append(nck)

        for user in msg:
            user = user.strip()
            if user in hq.joined_users:
                callback.say(channel,'{0} is already here'.format(user))
            elif user.isspace() is False and len(user) != 0:
                if keys.iskeyholder(user) is False:
                    hq.hq_join(user)
                else:
                    hq.hq_keyjoin(user)

    def leave(self, channel, callback, msg=None, nck=None, hq=None,keys=None, **kwargs):
        """
        Leave person from HQ, update the status
        """
        if len(msg) == 0:
            msg.append(nck)

        for user in msg:
            user = user.strip()
            if keys.iskeyholder(user) is False:
                hq.hq_leave(user)
            else:
                hq.hq_keyleave(user)
                if hq.keys_in_hq == 0:
                    callback.say(channel,'{0} has got the last key. Lock the frontdoor!'.format(user))

    def status(self, channel, callback, msg=None, nck=None, hq=None, keys=None, **kwargs):
        """
        Get HQ status
        """
        hqcolor = "04"
        if hq.status.status == "open":
            hqcolor = "03"
        elif hq.status.status == "private":
            hqcolor = "07"
        message = "HQ is currently " + "\x02\x03" + hqcolor + hq.status.status + "\x03\x02\x0F" + "\n"
        message += "Buntes Licht is " + "\x02\x03" + ("03" if hq.status.bunteslicht_s == "on" else "04") + hq.status.bunteslicht_s + "\x03\x02\x0F" + "\n"
        message += "Sound is " + "\x02\x03" + ("03" if hq.status.sound_s == "on" else "04") + hq.status.sound_s + "\x03\x02\x0F" + "\n"
        message += "Switch is " + "\x02\x03" + ("03" if hq.status.switch_s == "on" else "04") + hq.status.switch_s + "\x03\x02\x0F" + "\n"
        message += "Ambient Light (Lab) is " + "\x02\x03" + ("03" if hq.status.ambientlight_s == "on" else "04") + hq.status.ambientlight_s + "\x03\x02\x0F" + "\n"
        message += "Current power consumption: " + "\x02" + hq.status.power_s + "\x02\x0F" + " Watts\n"

        callback.msg(channel, message)


    def whois(self, channel, callback, msg=None, nck=None, hq=None, **kwargs):
        """
        List all persons in the hq
        """

        if hq.people_in_hq == 0:
            callback.msg(channel,'No one is here')
        else:
            userset = set(hq.joined_users)
            if hq.people_in_hq == 1:
                callback.msg(channel,'%s is here.' %', '.join(userset))
            else:
                callback.msg(channel,'%s are here.' %', '.join(userset))

    def open(self, channel, callback, msg=None, nck=None, hq=None, keys=None, **kwargs):
        """
        Opens the HQ
        """
        #If HQ is not open, open it and set topic
        if hq.hq_status is not 'open':
            hq.hq_open()
            topic = InternTopic()
            callback.topic(channel, topic.getTopic(hq, keys))

            if hq.get_hq_clean() is False:
                callback.say(channel,'The HQ is dirty, please clean it.')

        #HQ is open
        else:
            callback.say(channel,'The HQ is already open since {0}.'.format(hq.status_since))


    def private(self, channel, callback, msg=None, nck=None, hq=None, keys=None, **kwargs):
        """
        Open the HQ for members only
        """
        if hq.hq_status is not 'private':
            hq.hq_private()
            topic = InternTopic()
            callback.topic(channel, topic.getTopic(hq, keys))

            if hq.get_hq_clean() is False:
                callback.say(channel,'The HQ is dirty, please clean it.')

        #HQ is open for members only
        else:
            callback.say(channel,'The HQ is already open for members only since {0}.'.format(hq.status_since))

    def close(self, channel, callback, msg=None, nck=None, hq=None, keys=None, **kwargs):
        """
        Change HQ status to closed
        Update topic
        """
        if hq.hq_status is not 'closed':
            hq.hq_close()
            topic = InternTopic()
            callback.topic(channel, topic.getTopic(hq, keys))
        else:
            callback.say(channel, 'The HQ is already closed since {}'.format(hq.status_since))

    def dirty(self, channel, callback, msg=None, nck=None, hq=None, **kwargs):
        hq.hq_dirty()
        callback.say(channel,'The HQ is dirty!')

    def clean(self, channel, callback, msg=None, nck=None, hq=None, **kwargs):
        hq.hq_clean()
        callback.say(channel,'The HQ is clean \o/')
