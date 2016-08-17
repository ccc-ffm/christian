from datetime import datetime

class HQ(object):

    def __init__(self):
        self.people_in_hq = 0
        self.keys_in_hq = 0
        self.joined_users = []
        self.hq_status = 'unknown'
        self.status_since = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.is_clean = True
        self.joined_keys = []

    def update_time(self):
        self.status_since = datetime.now().strftime('%Y-%m-%d %H:%M')

    def hq_open(self):
        self.hq_status = 'open'
        self.update_time()

    def hq_close(self):
        self.hq_status = 'closed'
        self.update_time()
        self.people_in_hq = 0
        del(self.joined_users[:])
        del(self.joined_keys[:])

    def hq_private(self):
        self.hq_status = 'private'
        self.update_time()

    def hq_clean(self):
        self.is_clean = True

    def hq_dirty(self):
        self.is_clean = False

    def hq_join(self,user):
        self.people_in_hq += 1
        self.joined_users.append(user)

    def hq_leave(self,user):
        self.people_in_hq -=1
        self.joined_users.remove(user)

    def hq_keyjoin(self,user):
        self.keys_in_hq +=1
        self.joined_keys.append(user)
        self.hq_join(user)

    def hq_keyleave(self,user):
        self.keys_in_hq -=1
        self.joined_keys.remove(user)
        self.hq_leave(user)

    def get_hq_status(self):
        return self.hq_status, self.status_since

    def get_hq_clean(self):
        return self.is_clean
