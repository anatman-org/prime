"""
    Multipart-data reading and writing for
    the Zoidberg Conspiracy

    Multipart-Data files here are files with
    multiple delimited structures,
    that allow multiple objects to map into a single data object.
    Usually, this means markdown data with a YAML header,
    though it can also be multiple blocks of YAML and/or data.
    The purpose is to allow streams of YAML objects,
    mixed with document contents,
    to be handled seamlessly across concatenations.

    Blocks are delimited by three dashes ("---")
    at the start of any new line.

    Blocks will automatically be parsed as YAML,
    and if the YAML parsing fails,
    it will assume that the block is content,
    and append it to the current object in queue.

    If a block is a new YAML document,
    then the object in queue will be yielded,
    and the new YAML document will be in the queue.
    Any object in queue when the stream reaches EOF
    will also be yielded before the program returns.

    Blocks starting delimiters
    can optionally be followed by a space and key label,
    and the data in the following block will be
    assigned to that key in the queued object.
    The default label is "_".
    If the key exists in the queued object, 
    the key value is interpreted as a list,
    and the new content is appended to the end of that list.
    This allows adding multiple blocks to a single
    key in an object seamlessly.

    Example:

        ---
        id: 9c9ade4f-dedb-4fed-a253-95b89eadef75
        title: The Glass Bead Game
        --- review
        A glance at a portrait of Hermann Hesse—austere,
        unpretentiously bar ricaded behind steel‐rimmed glasses,
        yet sensitively open—reveals the in ner contradictions of the man,
        his reputation, his work.
        And each time we meet with a new critical appraisal or another translation,
        these contra dictions impress themselves upon us anew.

        The wavering course of Hesse's popularity illuminates his paradoxes,
        for throughout his career, but espe cially in his surprising revival in America,
        he has appealed both to young people and to adults,
        to an underground and to an establish ment,
        to a comfortable middle class and to the disenchanted young sharing
        his contempt for our indus trial civilization.
        On the one hand, he has projected a fresh vision of man hostile to
        our rationalistic, mercan tile culture;
        on the other hand, this vision can be endured,
        and has even been enjoyed, by those whom he pro fessed to reject.
        --- url
        https://www.nytimes.com/1970/01/04/archives/the-glass-bead-game-glass-bead.html
        --- review
        Set in the 23rd century,
        The Glass Bead Game is the story of Joseph Knecht,
        who has been raised in Castalia,
        which has provided for the intellectual elite to grow and flourish.

        Since childhood, Knecht has been consumed with mastering the Glass Bead Game,
        which requires a synthesis of aesthetics and scientific arts,
        such as mathematics, music, logic, and philosophy,
        which he achieves in adulthood, becoming a Magister Ludi (Master of the Game).
        --- url
        https://inverarity.livejournal.com/297236.html 
        ---

    This will result in the data structure:

        {
            "id": "9c9ade4f-dedb-4fed-a253-95b89eadef75",
            "title": "The Glass Bead Game",
            "review":
                [ "A glance at ...",
                  "Set in the 23rd ..." ]
            "url":
                [ "https://www.nytimes.com/...",
                 "https://inverarity.livejournal.com/..." ]
        }

    TODO:

      [ ] add supports for aliases in blocks.
"""

from io import StringIO, BufferedReader
from typing import TextIO, Optional
from collections.abc import Iterator

from yaml import load
from yaml import CLoader as Loader, CDumper as _Dumper, dump as _dump
from yaml.scanner import ScannerError
from yaml.parser import ParserError
from yaml.composer import ComposerError
from yaml.reader import ReaderError

# from yaml.scanner import ScannerError
# from yaml.constructor import DuplicateKeyError


class Dumper(_Dumper):
    def increase_indent(self, flow=False, *args, **kwargs):
        return super().increase_indent(flow=flow, indentless=False)


def dump(obj, stream=None, *kwargs):
    return _dump(
        obj, stream=stream, explicit_start=True, allow_unicode=True, Dumper=Dumper
    )


def add_key(data: dict, key: str, value: str) -> dict:

    old_value = data.get(key)

    if not old_value:
        data[key] = value
        return data

    if isinstance(old_value, list):
        data[key].append(value)
        return data
    else:
        data[key] = [old_value, value]


def parse_block(block: str):
    """Return a yaml-parsed object
    or return a string
    """

    try:
        data = load(block, Loader=Loader)
    except (ScannerError, ParserError, ReaderError, ComposerError):
        return block

    return data or block


def parse_stream(stream: TextIO) -> Iterator[dict | list | None]:
    """Parse a whole stream and yield objects"""

    buffer = None
    block = ""
    label = None
    eof = False
    new_label = None

    while 1:

        line = stream.readline()
        if not line:
            eof = True

        # A new block begins
        if line.startswith("---"):
            # Check if this block has a key
            if len(line.strip()) > 3:
                new_label = line[3:].strip()
                ## TODO, make sure label is valid YAML key
            else:
                new_label = None

        elif line:
            block = block + line
            continue

        # An existing block needs to be parsed and flushed
        if block.strip():

            data = parse_block(block)
            key = label or "_"

            # New data object
            if isinstance(data, (dict, list)):
                if buffer:
                    yield buffer
                buffer = data
                block = ""
                label = new_label
                continue

            # A simple string
            elif isinstance(data, (str, int, float)):

                if isinstance(data, (int, float)):
                    data = str(data)

                if isinstance(buffer, dict):
                    add_key(buffer, key, data)
                    block = ""
                    label = new_label
                    continue

            # Everything else unhandled for now
            raise ValueError(
                f"Can't add data of { type(data) } to { type(buffer) }: { block[:25] }"
            )

        # No line and EOF means quit
        if eof:
            yield buffer
            return

    yield buffer
    return


def dump_md(data: dict, file: TextIO):

    if body := data.get("Body", None):
        del data["Body"]

    dump(data, stream=file)
    if body:
        file.write("---\n")
        file.write(body)
        file.write("\n")


if __name__ == "__main__":
    from pprint import pprint
    from sys import stdin

    for o in parse_stream(stdin):
        pprint(o)
        print()
