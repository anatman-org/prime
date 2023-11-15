#!/usr/bin/env python
"""
prajna functions
"""
from io import SEEK_END, SEEK_SET, BytesIO
from json import loads
from uuid import UUID
from pathlib import Path

import requests
from splitstream import splitfile

# HACK
import sys

sys.path.append(".")

from z.md import dump_md

ITER_SIZE = 65536
PRAJNA_URL = "https://prajna.io"

# From https://gist.github.com/obskyr/b9d4b4223e7eaf4eedcd9defabb34f13
class ResponseStream:
    def __init__(self, request_iterator):
        self._bytes = BytesIO()
        self._iterator = request_iterator

    def _load_all(self):
        self._bytes.seek(0, SEEK_END)
        for chunk in self._iterator:
            self._bytes.write(chunk)

    def _load_until(self, goal_position):
        current_position = self._bytes.seek(0, SEEK_END)
        while current_position < goal_position:
            try:
                current_position = self._bytes.write(next(self._iterator))
            except StopIteration:
                break

    def tell(self):
        return self._bytes.tell()

    def read(self, size=None):
        left_off_at = self._bytes.tell()
        if size is None:
            self._load_all()
        else:
            goal_position = left_off_at + size
            self._load_until(goal_position)

        self._bytes.seek(left_off_at)
        return self._bytes.read(size)

    def seek(self, position, whence=SEEK_SET):
        if whence == SEEK_END:
            self._load_all()
        else:
            self._bytes.seek(position, whence)


def dump(args: list[str]):

    headers = {"Accept": "application/json", "Accept-Encoding": "gzip, deflate"}
    r = requests.get(PRAJNA_URL, {"q": args}, stream=True, headers=headers)

    for data in [
        loads(raw)
        for raw in splitfile(ResponseStream(r.iter_content(ITER_SIZE)), format="json")
    ]:

        _id = data.get("ID")
        print(_id)
        fname = f"p/{_id[0]}/{_id[1]}/{_id[2]}/{_id[3]}/{_id[4:]}.md"
        file = Path(fname)

        file.parent.mkdir(parents=True, exist_ok=True)

        with open(file, "w") as fd:
            dump_md(data, fd)


if __name__ == "__main__":

    from sys import argv

    dump(argv[1:])
