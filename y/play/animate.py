from pyglet.sprite import Sprite

from . import log
from .media import MatMedium, image_load


class MatSpin(MatMedium):

    autoincrement = True
    pos = 0

    file = None
    rotation_speed = 0

    def __init__(self, file="img/enso.png", rotation_speed=6, *args, **kwargs):
        super()
        self.file = file
        self.rotation_speed = rotation_speed

        log.debug(f"image loaded")

    def __call__(self, *args, **kwargs):

        _image = image_load(self.file)
        _image.anchor_x = _image.width // 2
        _image.anchor_y = _image.height // 2

        sprite = Sprite(
            _image,
            x=510 + (_image.width / 2),
            y=83 + (_image.height / 2),
        )
        sprite.rotation = self.pos
        sprite.draw()

        del _image

    def __len__(self):
        log.debug(f"q_len {self} = 0")

    def next(self):
        self.pos = self.pos + self.rotation_speed
        log.debug(f"next {self}")

    def prev(self):
        self.pos = self.pos - self.rotation_speed
        log.debug(f"prev {self}")
