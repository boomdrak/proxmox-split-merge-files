# proxmox-split-merge-files

proxmox-split-merge-files is a python 3 program to split large proxmox backup files.
Run it from cli

The progran can split and merge files back togeter

## Requirements

Install these pip modules

```bash
pip install dotenv
pip install requests
pip install argparse
pip install typing
pip install loguru
```

## Usage

```python
# RETSTORE COMMAND
python3 /mnt/pve/hddstorage/backup-system/main.py --action=merge --filePathToMerge=/mnt/pve/hddstorage/dump/vzdump-qemu-102-2024_04_25-21_19_54.vma_05032024_1250 --filePathToMergeOutput=/mnt/pve/hddstorage/dump/vzdump-qemu-102-2024_04_25-21_19_54.vma.lzo

# PRUNE / DELETE / SPLIT
python3 /mnt/pve/hddstorage/backup-system/main.py --action=split --directory=/mnt/pve/hddstorage/dump --fileType=.lzo --minFileSize=1000000000 --numKeepXBackups=1 --backupPartSize=1000000000

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.