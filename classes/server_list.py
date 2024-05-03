class ServerList:
    """Class representing a server list"""

    def __init__(self):
        self.list = []

    def add_server(self, server):
        self.list.append(server)

    def get_server_list(self):
        return self.list

    def get_server_in_list(self, server_id):
        for server in self.list:
            if server.server_id == server_id:
                return server
        return None

    # def get_backup_set_count(self):
    #     return self.num_backup_sets
