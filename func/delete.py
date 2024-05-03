import os
import errno

def silentremove(filename) -> bool:
    try:
        os.remove(filename)
        return True
    except OSError as error: # this would be "except OSError, e:" before Python 2.6
        if error.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            return False
    return False
