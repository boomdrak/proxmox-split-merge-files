import os
from classes.file import File


class DirContent:
    """Class representing a directory content"""

    values = []
    file_type = None
    min_file_size = None

    def __init__(self, directory, file_type=None, min_file_size=None):
        self.directory = directory
        self.file_type = file_type

        try:
            if min_file_size is not None:
                self.min_file_size = int(min_file_size)
        except (ValueError, TypeError):
            self.min_file_size = None

        with os.scandir(self.directory) as entries:
            for entry in entries:

                if file_type is not None:
                    if entry.name.endswith(file_type):
                        self.create_file_object(entry)
                        continue
                else:
                    self.create_file_object(entry)

    def create_file_object(self, o_file_entry):
        b_file_size_tmp = o_file_entry.stat().st_size
        if self.min_file_size is not None:
            if b_file_size_tmp >= self.min_file_size:
                self.values.append(File(o_file_entry))
                return
        else:
            self.values.append(File(o_file_entry))

    def get_values(self):
        return self.values
