"""
Class for managing a channels topic
"""

class InternTopic(object):

    def getTopic(self, hq, keys):
        hqstatus = hq.get_hq_status()
        keystatus = keys.getkeyholders()

        return('HQ is {} since {}. Keys: {}'.
               format(hqstatus[0],
                      hqstatus[1],
                      ', '.join([str(user) for user in keystatus])
                     )
               )

