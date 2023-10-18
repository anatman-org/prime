from pathlib import Path
from random import shuffle

from retry import retry

from pyglet.image import AbstractImage, codecs
from pyglet.image import load as image_load

from pyglet.media import Player, StreamingSource
from pyglet.media import load as media_load

from . import log


class MatMedium:

    autoincrement = False
    pos = 0

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

    def __init__(self, image_filename, *args, **kwargs):
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
    def __init__(self, file, *args, **kwargs):
        super().__init__()

        self.player = Player()
        self.source = StreamingSource()
        self.file = file
        self._media = media_load(self.file)

        self.player.queue(self._media)
        self.player.play()

    def __repr__(self):
        return f"MatVideo({self.file})"

    def __call__(self, *args, **kwargs):
        if self.player.source and self.player.source.video_format:
            self.player.get_texture().blit(0, 0)


class MatImageSequence(MatImage):

    def __init__(self, glob, index=0, *args, **kwargs):
        super().__init__("", *args, **kwargs)

        # Set up glob
        self.glob = glob
        log.debug(f"Added glob {self.glob=}")
        self.filelist = [str(f) for f in Path().glob(self.glob)]

        self.pos = index

        self._image = image_load(self.filelist[self.pos])

    def __len__(self):
        return len(self.filelist)

    def next(self):
        self.pos += 1
        self.file = self.filelist[self.pos]
        self._image = image_load(self.file)

    def prev(self):
        self.pos -= 1
        self.file = self.filelist[self.pos]
        self._image = image_load(self.file)


class MatImageCarousel(MatImageSequence):
    def next(self):
        self.pos += 1
        if self.pos >= len(self):
            self.pos = 0
        self.file = self.filelist[self.pos]
        self._image = image_load(self.file)

    def prev(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = len(self) - 1
        self.file = self.filelist[self.pos]
        self._image = image_load(self.file)


class MatImageRandom(MatImageSequence):

    _past = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        shuffle(self.filelist)
