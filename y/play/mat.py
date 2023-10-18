from shutil import copy as file_copy
from pathlib import Path

from pyglet.window import Window
from pyglet.image import load as image_load
from pyglet.image import codecs
from pyglet.gl import (
    glEnable,
    glBlendFunc,
    GL_BLEND,
    GL_SRC_ALPHA,
    GL_ONE_MINUS_SRC_ALPHA,
)

from .media import *
from . import log

from config import *


class MatWindow(Window):

    background = None
    stage = None
    show_stage = False

    fname_list = []
    pos = 0

    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **{
                k: kwargs[k]
                for k in kwargs
                if k not in ["background_image", "stage_image"]
            }
        )

        self.config.alpha_size = 8

        self.background = kwargs.get("background_image")
        self.stage = kwargs.get("stage_image")
        self.show_stage = False

        self.switch_to()

    def on_draw(self):
        self.switch_to()

        self.clear()
        glEnable(GL_BLEND)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.background.blit(0, 0)

        if self.show_stage:
            try:
                glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                self.stage.blit(0, 0)
            except:
                log.error("Couldn't show stage")
