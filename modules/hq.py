import os
from datetime import datetime

class HQ(object):

    def __init__(self, fpath, kpath):
        self.people_in_hq = 0
        self.keys_in_hq = 0
        self.joined_users = []
        self.hq_status = 'unknown'
        self.status_since = datetime.now().strftime('%Y-%m-%d %H:%M')
        self.is_clean = True
        self.joined_keys = []
        self.status = None
        self.fpath = fpath

        if os.path.isfile(fpath) and os.path.getsize(fpath) > 0:
            with open(fpath, 'r') as userfile:
                self.joined_users = [line.strip() for line in userfile]
                self.is_clean = True if self.joined_users[0] == "clean" else False
                self.joined_users.pop(0)
        self.joined_users = list(set(self.joined_users))
        self.people_in_hq = len(self.joined_users)

        if os.path.isfile(kpath) and os.path.getsize(kpath) > 0:
            with open(kpath, 'r') as statefile:
                keys = [line.strip() for line in statefile]
        keys = list(set(self.joined_users))
        for user in self.joined_users:
            if user in keys:
                self.joined_keys.append(user)
        self.keys_in_hq = len(self.joined_keys)

    def hq_set(self, status):
        if status == "open":
            self.hq_open()
        elif status == "closed":
            self.hq_close()
        elif status == "private":
            self.hq_private()

    def update_time(self):
        self.status_since = datetime.now().strftime('%Y-%m-%d %H:%M')

    def hq_open(self):
        self.hq_status = 'open'
        self.update_time()
        self.status.setStatus('open')

    def hq_close(self):
        self.hq_status = 'closed'
        self.update_time()
        self.people_in_hq = 0
        self.keys_in_hq = 0
        del(self.joined_users[:])
        del(self.joined_keys[:])
        self.status.setStatus('closed')

    def hq_private(self):
        self.hq_status = 'private'
        self.update_time()
        self.status.setStatus('private')

    def hq_clean(self):
        self.is_clean = True
        self.savestates()

    def hq_dirty(self):
        self.is_clean = False
        self.savestates()

    def hq_join(self,user):
        self.people_in_hq += 1
        self.joined_users.append(user)
        self.savestates()

    def hq_leave(self,user):
        if user in self.joined_users:
            self.people_in_hq -=1
            self.joined_users.remove(user)
            self.savestates()

    def hq_keyjoin(self,user):
        self.keys_in_hq +=1
        self.joined_keys.append(user)
        self.hq_join(user)

    def hq_keyleave(self,user):
        if user in self.joined_keys:
            self.keys_in_hq -=1
            self.joined_keys.remove(user)
        self.hq_leave(user)

    def get_hq_status(self):
        return self.hq_status, self.status_since

    def get_hq_clean(self):
        return self.is_clean

    def savestates(self):
        userfile=open(self.fpath,'w+')
        userfile.write("clean\n" if self.is_clean else "dirty\n")
        for user in set(self.joined_users):
            userfile.write("%s\n" % user)
        userfile.close()
