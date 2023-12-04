#!/usr/bin/env python
"""
z.bit

A module for checking and synchronizing data that is stored in a hash table.

The format is the same as for git-lfs, where files are named by their sha256.
Where the the hash is represented as a hexdigest of H[64],
it is stored in a file H[0:2]/H[2:4]/H[4:].
"""

from pathlib import Path
from typing import Union, BinaryIO
from tempfile import NamedTemporaryFile
from hashlib import sha256
from re import compile as re_compile

DEFAULT_BLOCKSIZE = 8192
_HEX_RE = re_compile("[0-9a-f]{64}")
_LFS_DIR_RE = re_compile("^.*/[0-9a-f]{2}/[0-9a-f]{2}$")

def store(
    bit_dir: Union[Path, str], file: BinaryIO, blocksize: int = DEFAULT_BLOCKSIZE
) -> str:

    # Convert bit_dir to a Path
    if not isinstance(bit_dir, Path):
        bit_dir = Path(bit_dir)

    # Check there's a tmp directory in the bit_dir Path
    (bit_dir / "tmp").mkdir(parents=True, exist_ok=True)

    file_hash = sha256()

    with NamedTemporaryFile(dir=(bit_dir / "tmp")) as tmp_file:

        while buffer := file.read(blocksize):
            file_hash.update(buffer)
            tmp_file.write(buffer)

        file_hex = file_hash.hexdigest()

        bit_path = Path(bit_dir / file_hex[:2] / file_hex[2:4] / file_hex[4:])

        if bit_path.exists():
            tmp_file.close()
            return file_hex
        else:
            bit_path.parent.mkdir(parents=True, exist_ok=True)
            bit_path.hardlink_to(tmp_file.name)

    return file_hex


def check(bit_dir: Union[Path, str], blocksize: int = DEFAULT_BLOCKSIZE) -> None:

    # Convert bit_dir to a Path
    if not isinstance(bit_dir, Path):
        bit_dir = Path(bit_dir)

    for file in bit_dir.rglob("*"):

        if file.is_dir():
            continue

        hex_path = file.parent.parent.name + file.parent.name + file.name
        if not _HEX_RE.match(hex_path):
            print("skipping", str(file))

        print(hex_path, end=" > ")

        with file.open("rb") as fd:
            file_hash = sha256()
            while buffer := fd.read(blocksize):
                file_hash.update(buffer)

            if hex_path != file_hash.hexdigest():
                print("ERROR")
            else:
                print("OK")


def sync(
    source_dir: Union[Path, str],
    dest_dir: Union[Path, str],
    blocksize: int = DEFAULT_BLOCKSIZE,
) -> None:

    import paramiko

    source_dir = Path(source_dir)

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect("meru", 22)
    sftp = ssh.open_sftp()

    for local_dir in Path(source_dir).glob("*/*"):

        if not _LFS_DIR_RE.match(str(local_dir)):
            continue

        try:
            sftp.chdir(str(local_dir))
        except FileNotFoundError:
            sftp.mkdir(str(local_dir))
            sftp.chdir(str(local_dir))

        remote_files = sftp.listdir()

        for local_file in local_dir.iterdir():
            if not local_file.name in remote_files:
                print(local_file, "SYNC", file=sys.stderr)
                sftp.put(local_file, str(local_file))


if __name__ == "__main__":

    import sys

    if not len(sys.argv) > 2:
        print("error, not enough arguments")

    cmd = sys.argv[1]
    bit_dir = sys.argv[2]

    match cmd:

        case "store":
            if not len(sys.argv) > 3:
                print("Not enough arguments")
                sys.exit(1)

            for file in sys.argv[3:]:
                print(store(bit_dir, open(file, "rb")), file)

        case "sync":
            if not len(sys.argv) > 3:
                print("Not enough arguments")
                sys.exit(1)

            sync(sys.argv[2], sys.argv[3])

        case "check":
            check(bit_dir)

        case "_":
            print("arguments", sys.argv[1:])
