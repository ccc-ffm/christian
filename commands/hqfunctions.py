"""Class for setting HQ states"""
from datetime import datetime
import sys

from modules import InternTopic

class HQFunctions(object):


    def join(self, channel, callback, msg=None, nck=None, hq=None, keys=None, **kwargs):
        """
        Join users to HQ, update the status
        """
        #Open HQ if its closed
        if hq.hq_status is 'closed':
            self.open(channel, callback, msg, nck, hq, keys)

        if len(msg) == 0:
            msg.append(nck)

        for user in msg:
            user = user.strip()
            if user in hq.joined_users:
                callback.say(channel,'{0} is already here'.format(nck))
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


    def whois(self, channel, callback, msg=None, nck=None, hq=None, **kwargs):
        """
        List all persons in the hq
        """

        if hq.people_in_hq == 0:
            callback.msg(nck,'No one is here')
        else:
            userset = set(hq.joined_users)
            if hq.people_in_hq == 1:
                callback.msg(nck,'%s is here.' %', '.join(userset))
            else:
                callback.msg(nck,'%s are here.' %', '.join(userset))

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
