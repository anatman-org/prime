from pathlib import Path
from random import shuffle

from retry import retry

from pyglet.image import AbstractImage, codecs
from pyglet.image import load as image_load

from pyglet.media import Player, StreamingSource
from pyglet.media import load as media_load

from . import log

STATE = {"NONE": 0, "SET": 1, "PLAYING": -1}


class MatMedium:

    autoincrement = False
    pos = 0
    state = STATE["NONE"]

    def __len__(self):
        log.debug(f"q_len {self} = 0")

    def pause(self):
        log.debug(f"pause {self} <None>")

    def next(self):
        log.debug(f"next {self} <None>")
        pass

    def prev(self):
        log.debug(f"prev {self} <None>")


class MatImage(MatMedium):

    _image = None

    def __init__(self, image_filename=None, *args, **kwargs):
        super()
        self.file = image_filename

    def __repr__(self):
        return f"MatImage({self.file})"

    def __call__(self, *args, **kwargs):

        if self.file:
            self._image = image_load(self.file)
            self._image.blit(0, 0, 0)
        else:
            log.error(f"call {self} no image")

    def __len__(self):
        return 1


class MatVideo(MatMedium):
    def __init__(self, file, loop=False, *args, **kwargs):
        super().__init__()

        self.player = Player()
        self.player.loop = loop

        self.source = StreamingSource()
        self.file = file
        self._media = media_load(self.file)

        self.player.queue(self._media)
        self.player.play()

    @property
    def state(self):
        if self.player.playing:
            return STATE["PLAYING"]
        elif self.file:
            return STATE["SET"]
        else:
            return STATE["NONE"]

    @property
    def pos(self):
        return self.player.time

    def __repr__(self):
        return f"MatVideo({self.file}@{self.pos})"

    def __call__(self, *args, **kwargs):
        if self.player.source and self.player.source.video_format:
            self.player.get_texture().blit(0, 0)

    def pause(self):

        if self.player.playing:
            self.player.pause()
            log.debug(f"pause {self}")
        else:
            self.player.play()
            log.debug(f"resume {self}")


class MatImageList(MatImage):

    _image = None

    def __init__(self, image_file_list, pos=0, loop=True, *args, **kwargs):
        super()

        self._filelist = image_file_list
        self._loop = loop

        self.pos = pos
        self.file = self._filelist[self.pos]

    def __repr__(self):
        return f"MatImage({self.file}@)"

    def __call__(self, *args, **kwargs):
        if self.file:
            self._image = image_load(self.file)
            self._image.blit(0, 0, 0)
        else:
            log.error(f"call {self} no image")

    def __len__(self):
        return len(self._filelist)

    def next(self):
        self.pos += 1

        if self._loop and self.pos >= len(self._filelist):
            self.pos = 1

        self.file = self._filelist[self.pos]
        log.debug(f"next {self}@{self.pos}")

    def prev(self):
        self.pos -= 1

        if self._loop and self.pos < 0:
            self.pos = len(self) - 1

        self.file = self._filelist[self.pos]
        log.debug(f"prev {self}@{self.pos}")


class MatImageListRandom(MatImageList):

    _image = None

    def __init__(self, image_file_list, pos=0, loop=True, *args, **kwargs):

        shuffle(image_file_list)
        super().__init__(image_file_list, pos, loop, *args, **kwargs)
