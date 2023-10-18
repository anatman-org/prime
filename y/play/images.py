from pathlib import Path
from random import shuffle

from retry import retry

from pyglet.image import AbstractImage, codecs
from pyglet.image import load as image_load

from pyglet.media import Player, StreamingSource
from pyglet.media import load as media_load

from . import log


class ImageSequenceException(Exception):
    pass


class ImageNull(AbstractImage):
    def __init__(self, width=0, height=0, anchor_x=0, anchor_y=0, *args, **kwargs):
        super().__init__(width, height)

    def __len__(self):
        return 0

    @retry(codecs.DecodeException, tries=3, delay=2)
    def load(self):
        pass

    def blit(self, x, y, z=0):
        pass

    def blit_into(self, source, x, y, z=0):
        pass

    def next(self):
        pass

    def prev(self):
        pass


class VideoStatic(Player):
    def __init__(self, *args, **kwargs):
        super().__init__()

        self.file = kwargs.get("file")

        self._source = StreamingSource()
        self._media = media_load(self.file)
        self.queue(self._media)
        self.play()

    def blit(self, x, y, z=0):
        self.get_texture().blit()

    def blit_into(self, source, x, y, z=0):
        self.blit()

    def __len__(self):
        return 0

    def next(self):
        pass

    def prev(self):
        pass


class ImageStatic(AbstractImage):

    _image = None

    def __init__(self, *args, **kwargs):
        super().__init__(0, 0)

        self.file = kwargs.get("file")
        if not self.file:
            log.error(f"No file passed to {self.__class__}")
            raise Exception("Invalid File exception")

        self._image = image_load(self.file)
        log.info(f"Added static file {self.file=}")

    def __len__(self):
        return 0

    def blit(self, x, y, z=0):
        self._image.blit(x, y, z=z)

    def blit_into(self, source, x, y, z=0):
        self._image.blit(source, x, y, z=z)

    def next(self):
        pass

    def prev(self):
        pass


class ImageSequence(AbstractImage):

    _image = None
    autoincrement = False
    filelist = []

    def __init__(self, width, height, anchor_x=0, anchor_y=0, *args, **kwargs):
        super().__init__(width, height)

    def __len__(self):
        return 0

    @retry(codecs.DecodeException, tries=3, delay=2)
    def load(self):
        pass

    def blit(self, x, y, z=0):

        self.load()

        if self._image:
            self._image.blit(x, y, z=z)
        else:
            log.error("Blit called before image defined")
            raise IndexError

    def blit_into(self, source, x, y, z=0):

        if self._image:
            self._image.blit(source, x, y, z=z)
        else:
            log.error("Blit called before image defined")
            raise IndexError

        pass

    def next(self):
        pass

    def prev(self):
        pass


class ImageGlobSequence(ImageSequence):

    autoincrement = False
    _past = None
    _future = None

    def __init__(self, width=0, height=0, anchor_x=0, anchor_y=0, *args, **kwargs):
        super().__init__(width, height, anchor_x=anchor_x, anchor_y=anchor_y)

        # Set up glob
        self.glob = kwargs.get("glob")
        if not self.glob:
            log.error(f"No file glob passed to {self.__class__}")
            raise Exception("Invalid Glob exception")

        log.info(f"Added glob {self.glob=}")
        self.filelist = [str(f) for f in Path().glob(self.glob)]

        # for f in self.filelist:
        #    log.info(f"Added file {f}")

        # Find index
        if idx := kwargs.get("index"):
            self.pos = int(idx)
        else:
            self.pos = 0

        if self.pos > len(self.filelist):
            log.error(
                "Image sequence position {self.pos} out of { len(self.filelist) } for {self.glob} "
            )
            raise ImageSequenceException(
                "Image sequence position {self.pos} out of { len(self.filelist) } for {self.glob}"
            )

        # Set increment
        if auto := kwargs.get("autoincrement"):
            if auto in (True, "True", 1, "1", "Yes"):
                self.autoincrement = True

        # Clean up
        self.load()

    @retry(codecs.DecodeException, tries=3, delay=2)
    def load(self):

        # use _past and _future to optimize this

        try:
            self._image = image_load(self.filelist[self.pos])
        except Exception as e:
            log.error(f"Loading image {self.pos} of {len(self.filelist)}")
            raise ImageSequenceException(e)

    def __getitem__(self, index):
        return self._image

    def __len__(self):
        return len(self.filelist)

    def next(self):
        self.pos += 1
        if self.pos > len(self):
            log.error(f"Request to go past end of image sequence")
            raise IndexError
        log.info(f"{self} loading image {self.pos}")
        self.load()

    def prev(self):
        self.pos -= 1
        if self.pos < 0:
            log.error(f"Request to go before beginning of image sequence")
            raise IndexError
        log.info(f"{self} loading image {self.pos}")
        self.load()


class ImageGlobCarousel(ImageGlobSequence):
    def next(self):
        self.pos += 1
        if self.pos >= len(self):
            self.pos = 0
        self.load()

    def prev(self):
        self.pos -= 1
        if self.pos < 0:
            self.pos = len(self) - 1
        self.load()


class ImageGlobRandom(ImageGlobSequence):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        shuffle(self.filelist)
        log.info(f"{self} sorted {len(self)} files")
