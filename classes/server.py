from datetime import datetime
from dataclasses import dataclass
import copy

@dataclass
class Server:
    """Class representing a server content"""

    server_id = None
    num_backup_sets = 0
    backup_sets = []
    keep_num_backups = 7
    delete_backups = False

    def __hash__(self):
        # Here we define how we should compute
        # the hash for a given User. In this example
        # we use the hash of the '__email' attribute
        return hash(self.server_id)

    def __init__(self,server_id):
        self.num_backup_sets = 0
        self.server_id = server_id

    def set_server_id(self, server_id):
        self.server_id = server_id

    def set_keep_num_backups(self, num):
        self.keep_num_backups = num

    def add_backup_set_count(self, num):
        self.num_backup_sets += num

    def set_new_backup_set(self, backup_set):
        self.backup_sets = backup_set

    def add_backup_set(self, date, file_name):
        temp = copy.deepcopy(self.backup_sets)
        temp.append({'date': date, 'file_name':file_name})
        temp.sort(key = lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'))
        if len(temp) > self.keep_num_backups:
            self.delete_backups = True
        self.backup_sets = temp
        self.num_backup_sets = len(self.backup_sets)

    def get_backup_set(self):
        return self.backup_sets

    def get_backup_set_count(self):
        return self.num_backup_sets
