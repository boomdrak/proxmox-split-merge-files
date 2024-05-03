import os
import glob
import hashlib
from datetime import datetime
import func.log

VERSION = 'v.1.4'

VERBOSE = False


def file_split(file, parts=None, chunk_size=None):
    '''
    Splits files into parts, or in chunk_size
    '''
    if not file:
        return False
    if not parts and not chunk_size:
        return False

    fsize = os.path.getsize(file)

    if chunk_size and chunk_size > fsize:
        raise ValueError('Chunk size cannot be greater than file size')

    vvprint(f'Source file: {file}')
    vvprint(f'Size: {fsize}')

    segment_size = 0

    if parts:
        segment_size = fsize // parts
    else:
        segment_size = chunk_size

    if segment_size < 1: # type: ignore
        raise ValueError('At least 1 byte required per part')

    vvprint(f'Segment Size: {segment_size}')

    fdir, fname = os.path.split(file)
    fname = os.path.splitext(fname)[0]

    start_time = datetime.today().strftime("%m%d%Y_%H%M")

    vvprint(f'Hash: {hash}\n\n')
    vvprint(f'Reading file: {file}')

    with open(file,'rb') as f_h:
        fpart = 1
        while f_h.tell() != fsize:
            if parts:
                # check if this is the last part
                if fpart == parts:
                    # size of the file - wherever the file pointer is
                    # the last part would contain segment_size + whatever is left of the file
                    segment_size = fsize - f_h.tell()

            chunk = f_h.read(segment_size)
            part_filename = os.path.join(fdir, f'{fname}_{start_time}_{fpart}.prt')
            vvprint(f'{part_filename} Segment size: {segment_size} bytes')
            with open(part_filename, 'wb') as chunk_fh:
                chunk_fh.write(chunk)
            fpart += 1

        return True


def file_stitch(file, outfile=None):
    '''
    Stitches the parts together
    '''
    # d:\\somedir\\somefile.txt to
    # d:\\somedir and somefile.txt

    if not file:
        return False

    fdir, fname = os.path.split(file)
    # fname = fname.split('.')[0]
    # fname = os.path.splitext(fname)[0]

    file_parts = glob.glob(os.path.join(fdir,  f'{fname}_*.prt'))
    file_parts = sort_file_parts(file_parts)

    if not file_parts:
        raise FileNotFoundError('Split files not found')

    if outfile:
        # if just the filename
        if os.path.split(outfile)[0] == '':
            # create the file in input dir (fdir)
            outfile = os.path.join(fdir, outfile)

    vvprint(f'Output: {outfile or file}')

    with open(outfile or file, 'wb') as f_h:
        for filename in file_parts:
            buffer = b''
            vvprint(f'Reading {filename}')
            with open(filename, 'rb') as prt_fh:
                buffer = prt_fh.read()
                f_h.write(buffer)

    vvprint(f'Written {os.path.getsize(outfile or file)} bytes')
    return True


def gethash(file):
    '''
    Returns the hash of file
    '''
    hash_bit = None
    with open(file, 'rb') as f_h:
        hash_bit = hashlib.sha256(f_h.read()).hexdigest()
    return hash_bit


def checkhash(file, hashfile):
    '''
    Compares hash of a file with original hash read from a file
    '''
    curhash = None
    orghash = None
    curhash = gethash(file)
    with open(hashfile, 'r', encoding="utf-8") as f_h:
        orghash = f_h.read()

    return curhash == orghash

def vvprint(text):
    '''
    print function to function only when verbose mode is on
    '''
    func.log.do(text)


def getpartno(filepart):
    '''
    Returns the part number from a part filename
    Ex: flask_05112022_1048_3.prt -> 3
    '''
    return int(filepart.split('_')[-1].split('.')[0])


def sort_file_parts(file_part_list):
    '''
    Returns a sorted list of part filenames based on the part number
    Ex: ['flask_05112022_1048_3.prt', 'flask_05112022_1048_1.prt', 'flask_05112022_1048_2.prt'] ->
        ['flask_05112022_1048_1.prt', 'flask_05112022_1048_2.prt', 'flask_05112022_1048_3.prt']
    '''
    # creates list of (prt_no, part)
    fparts = [(getpartno(prt), prt) for prt in file_part_list]
    fparts.sort(key=lambda x: x[0])
    fparts = [prt[1] for prt in fparts]
    return fparts
