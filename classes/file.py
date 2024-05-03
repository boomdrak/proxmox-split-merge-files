import os
import time

class File :
    name = None
    size_human = None
    size = None
    date_created = None
    file_path = None

    def __init__(self, file_entryobject):
        self.name = file_entryobject.name
        self.size_human = self.sizeof_fmt(file_entryobject.stat().st_size)
        self.size = file_entryobject.stat().st_size
        self.date_created =time.strptime(time.ctime(os.path.getctime(file_entryobject)))
        self.date_created = time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(time.ctime(os.path.getctime(file_entryobject))))

        self.file_path = os.path.abspath(file_entryobject.path)

    def sizeof_fmt(self, num, suffix="B"):
        for unit in ("", "Ki", "Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
            if abs(num) < 1024.0:
                return f"{num:3.1f}{unit}{suffix}"
            num /= 1024.01
        return f"{num:.1f}Yi{suffix}"
