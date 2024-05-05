import argparse
import sys
import os
from typing import cast
from dotenv import load_dotenv 
import func.log
from classes.dir_content import DirContent
from func.file_search import find_and_delete_files
from classes.server import Server
from help.array_tool import get_object_from_array_by_value
from func.file_stich import file_split, file_stitch
from func.delete import silentremove
from func.ntfy import send_msg_to_ntfy

func.log.do("Booting application", func.log.Level.SUCCESS)
load_dotenv()

parser = argparse.ArgumentParser()
parser.add_argument('--directory', dest='directory', type=str, help='Directory to search')
parser.add_argument('--action', dest='action', type=str, help='split og merge files', required=True)
parser.add_argument('--deletePartFiles', dest='deletePartFiles', type=bool, help='Delete old .prt backups')
parser.add_argument('--filePathToMerge', dest='filePathToMerge', type=str, help='Path of file to merge into one file')
parser.add_argument('--filePathToMergeOutput', dest='filePathToMergeOutput', type=str, help='Merge output filepath')
parser.add_argument('--fileType', dest='fileType', type=str, help='Search for specific filetype .lzo')
parser.add_argument('--minFileSize', dest='minFileSize', type=str, help='File must be larger than X bytes')
parser.add_argument('--numKeepXBackups', dest='numKeepXBackups', type=int, help='How many backup sets to keep')
parser.add_argument('--backupPartSize', dest='backupPartSize', type=int, help='How many backup sets to keep')

try:
    args = parser.parse_args()
except SystemExit:
    func.log.do("Missing params",  func.log.Level.DEBUG)
    sys.exit(-1)

func.log.do("All command line params received")

# RETSTORE COMMAND
# python3 /mnt/pve/hddstorage/backup-system/main.py --action=merge --filePathToMerge=/mnt/pve/hddstorage/dump/vzdump-qemu-102-2024_04_25-21_19_54.vma_05032024_1250 --filePathToMergeOutput=/mnt/pve/hddstorage/dump/vzdump-qemu-102-2024_04_25-21_19_54.vma.lzo
# PRUNE / DELETE / SPLIT
# python3 /mnt/pve/hddstorage/backup-system/main.py --action=split --directory=/mnt/pve/hddstorage/dump --fileType=.lzo --minFileSize=1000000000 --numKeepXBackups=1 --backupPartSize=1000000000

# send_msg_to_ntfy("Booting application backup-system - DOCKER.BOOMNET.BOMES")
ACTION=args.action

if ACTION == "merge":
    func.log.do("Staring to merge files: " + args.filePathToMerge + " outputing to: " + args.filePathToMergeOutput)
    file_stitch(args.filePathToMerge, args.filePathToMergeOutput)
    sys.exit(1)

KEEP_BACKUPS = args.numKeepXBackups
BACKUP_SPLIT_FILE_PART_SIZE = int(args.backupPartSize)
# 1 Gib file size = 1000000000 bytes
o_dir_content = DirContent(directory=args.directory, file_type=args.fileType, min_file_size=args.minFileSize)
func.log.do("Got files with DirContent. Num files: " + str(len(o_dir_content.get_values())))

list_servers = []

for file in o_dir_content.get_values():
    server_id = file.name.split("-")[2]
    o_current_server = cast(Server, get_object_from_array_by_value(list_servers, {'server_id': server_id}))
    if o_current_server is None:
        o_new_server = Server(server_id)
        o_new_server.set_server_id(server_id)
        o_new_server.set_keep_num_backups(KEEP_BACKUPS)
        o_new_server.add_backup_set(file.date_created, file.file_path)
        list_servers.append(o_new_server)
        continue

    o_current_server.add_backup_set(file.date_created, file.file_path)

## DELETE UNWANTED BACKUPS
for backup_del_server in list_servers:
    o_server = cast(Server , backup_del_server)
    if o_server.delete_backups:
        lst_backups = o_server.get_backup_set()
        lst_backups_to_del = lst_backups[:KEEP_BACKUPS]
        lst_backups_to_keep = lst_backups[len(lst_backups) - KEEP_BACKUPS:]
        o_server.set_new_backup_set(lst_backups_to_keep)
        for backup_set_to_delete in lst_backups_to_del:
            if silentremove(backup_set_to_delete['file_name']):
                ## DELETE OLD .prt files that we dont need anymore
                find_and_delete_files(args.directory, [backup_set_to_delete['file_name'] + '*.prt'], KEEP_BACKUPS)
                func.log.do("Deleted file: " + str(backup_set_to_delete['file_name']))
            else:
                func.log.do("Deleting file ERROR : " + str(backup_set_to_delete['file_name']), func.log.Level.DEBUG)

## SPLIT BACKUPS THAT WE KEEP
for split_backup_server in list_servers:
    o_server = cast(Server , split_backup_server)
    lst_backups = o_server.get_backup_set()
    for backup_set_to_split in lst_backups:
        file_size = os.path.getsize(backup_set_to_split['file_name'])
        mb = file_size / (1024 * 1024)
        # 1000000000 bytes = 1GB
        if file_split(backup_set_to_split['file_name'], None, BACKUP_SPLIT_FILE_PART_SIZE):
            #DELETE FILE
            func.log.do("Splitted backup file:" + str(backup_set_to_split['file_name']))
            if silentremove(backup_set_to_split['file_name']):
                func.log.do("Deleted file that has been split : " + str(backup_set_to_split['file_name']))
            else:
                func.log.do("Deleted file that has been split ERROR : " + str(backup_set_to_split['file_name']), func.log.Level.DEBUG)
            #exit(1)

# send_msg_to_ntfy("Exiting application with success backup-system - DOCKER.BOOMNET.BOMES")
func.log.do("Exiting application with success", func.log.Level.SUCCESS)
