"""Class for setting HQ states"""
from datetime import datetime
import sys

class HQFunctions(object):

    def join(self, channel, callback, msg=None, nck=None, hq=None, keys=None, pb=None):
        """
        Join users to HQ, update the status
        """
        #Open HQ if its closed
        if hq.hq_status is 'closed':
            self.open(channel, callback, msg, nck, hq, keys, pb)


        #user is joining himself
        if len(msg) == 0:
            if nck in hq.joined_users:
                callback.say(channel,'{0} is already here'.format(nck))
            else:
                hq.hq_join(nck)
                callback.topic(channel,hq.get_hq_status())

                #Check if he owns a key, update key list
                if keys.iskeyholder(nck):
                    hq.hq_keyjoin(nck)
        else:
            #Add users to the list of joined users.
            for user in msg:
                if user in hq.joined_users:
                    callback.say(channel,'{0} is already here'.format(user))
                else:
                    hq.hq_join(user)

                    #Check if they own a key, update key list
                    if keys.iskeyholder(user):
                        hq.hq_keyjoin(user)

            callback.topic(channel,hq.get_hq_status())

    def leave(self, channel, callback, msg=None, nck=None, hq=None,keys=None, pb=None):
        """
        Leave person from HQ, update the status
        """

        if len(msg) == 0:
            if nck in hq.joined_users:
                hq.hq_leave(nck)

                if keys.iskeyholder(nck):
                    hq.hq_keyleave(nck)

                    if hq.keys_in_hq == 0:
                        callback.say(channel,'{0} has got the last key. Lock the frontdoor!'.format(user))
                        callback.msg(user,'You have got the last key. Lock the frontdoor!')

        else:
            #Remove them from the list if they are joined
            for user in msg:
                if user in hq.joined_users:
                    hq.hq_leave(user)

                if keys.iskeyholder(user):
                    hq.hq_keyleave(user)

                #If last keyholder is about to leave inform him
                    if hq.keys_in_hq == 0:
                        callback.say(channel,'{0} has got the last key. Lock the frontdoor!'.format(user))

            #Update the topic
            callback.topic(channel,hq.get_hq_status())

    def whois(self, channel, callback, msg=None, nck=None, hq=None,keys=None, pb=None):
        """
        List all persons in the hq
        """

        if hq.people_in_hq == 0:
            callback.say(channel,'No one is here')
        else:
            userset = set(hq.joined_users)
            if hq.people_in_hq == 1:
                callback.say(channel,'%s is here.' %', '.join(userset))
            else:
                callback.say(channel,'%s are here.' %', '.join(userset))

    def open(self, channel, callback, msg=None, nck=None, hq=None,keys=None, pb=None):
        """
        Opens the HQ
        """
        #If HQ is not open, open it and set topic
        if hq.hq_status is not 'open':
            hq.hq_open()
            callback.topic(channel,hq.get_hq_status())

            if hq.get_hq_clean() is False:
                callback.say(channel,'The HQ is dirty, please clean it.')

        #HQ is open
        else:
            callback.say(channel,'The HQ is already open since {0}.'.format(hq.status_since))


    def private(self, channel, callback, msg=None, nck=None, hq=None,keys=None, pb=None):
        """
        Open the HQ for members only
        """
        if hq.hq_status is not 'private':
            hq.hq_private()
            callback.topic(channel, hq.get_hq_status())

            if hq.get_hq_clean() is False:
                callback.say(channel,'The HQ is dirty, please clean it.')

        #HQ is open for members only
        else:
            callback.say(channel,'The HQ is already open for members only since {0}.'.format(hq.status_since))

    def close(self, channel, callback, msg=None, nck=None, hq=None,keys=None, pb=None):
        """
        Change HQ status to closed
        Update topic
        """
        if hq.hq_status is 'closed':
            callback.say(channel,'HQ is closed since {0}'.format(hq.status_since))
        else:
            hq.hq_close()
            callback.topic(channel,hq.get_hq_status())

    def dirty(self, channel, callback, msg=None, nck=None, hq=None,keys=None, pb=None):
        hq.hq_dirty()
        callback.say(channel,'The HQ is dirty!')

    def clean(self, channel, callback, msg=None, nck=None, hq=None,keys=None, pb=None):
        hq.hq_clean()
        callback.say(channel,'The HQ is clean \o/')
