from PIL import Image

from . import log
from .media import MatMedium, pil_to_pyg


class MatSpin(MatMedium):
    autoincrement = True
    pos = 0

    file = None
    rotation_speed = 0

    _image = None

    def __init__(self, file="img/enso.png", rotation_speed=6, *args, **kwargs):
        super()
        self.file = file
        self.rotation_speed = rotation_speed
        self._image = Image.open(self.file)

    def __call__(self, *args, **kwargs):
        image = pil_to_pyg(self._image.rotate(-self.pos))
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        image.blit(1920 / 2, 1080 / 2, 0)

    def __len__(self):
        log.debug(f"q_len {self} = 0")

    def next(self):
        self.pos = self.pos + self.rotation_speed
        if self.pos > 360:
            self.pos = self.pos - 360
        log.debug(f"next {self}")

    def prev(self):
        self.pos = self.pos - self.rotation_speed
        if self.pos < 0:
            self.pos = self.pos + 360
        log.debug(f"prev {self}")
