from pyglet.sprite import Sprite

from . import log
from .media import MatMedium, image_load


class MatEnso(MatMedium):

    autoincrement = True
    pos = 0

    file = "img/enso.png"
    rotation_speed = 6

    def __init__(self, image_filename=None, *args, **kwargs):
        super()

        log.debug(f"image loaded")

    def __repr__(self):
        return f"{self.__class__}({self.file}@{self.pos})"

    def __call__(self, *args, **kwargs):
        self._image = image_load("img/enso.png")
        self._image.anchor_x = self._image.width // 2
        self._image.anchor_y = self._image.height // 2

        sprite = Sprite(
            self._image,
            x=510 + (self._image.width / 2),
            y=83 + (self._image.height / 2),
        )
        sprite.rotation = self.pos
        sprite.draw()

    def __len__(self):
        log.debug(f"q_len {self} = 0")

    def next(self):
        self.pos = self.pos + self.rotation_speed
        log.debug(f"next {self}")

    def prev(self):
        self.pos = self.pos - self.rotation_speed
        log.debug(f"prev {self}")
