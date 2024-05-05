import fnmatch
import os
from datetime import datetime, timedelta
import func.log

# function to loop and search patterns and rm files.
def find_and_delete_files(dir_to_clean: str, patterns: list, days_old_to_delete: int):
    file_list = []
    days_ago = datetime.now() - timedelta(days=days_old_to_delete)
    for root, dirs, files in os.walk(dir_to_clean):
        for pattern in patterns:
            for filename in fnmatch.filter(files, pattern):
                file_list.append(os.path.join(root, filename))
                file_list.sort()

    for file in file_list:
        file_ctime = datetime.fromtimestamp(os.path.getctime(file))
        if file_ctime < days_ago:
            if os.path.isfile(file):
                try:
                    func.log.do(f"Removing old prt file :[{0}]".format(file))
                    os.remove(file)
                except OSError as e:
                    func.log.do(f"Old File prt clean up failed: [{0}]".format(e), func.log.Level.DEBUG)
