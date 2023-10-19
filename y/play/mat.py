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


class Mat:

    window = None
    background = None
    stage = None
    show_stage = False

    fname_list = []
    pos = 0

    def __init__(self, window, background, stage, *args, **kwargs):

        self.window = window
        self.window.config.alpha_size = 8

        self.background = background
        self.stage = stage
        self.show_stage = False

        self.window.on_draw = self.on_draw

    def __call__(self, *args, **kwargs):
        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event("on_draw")
        self.window.flip()

    def on_draw(self):
        self.window.switch_to()

        self.window.clear()
        glEnable(GL_BLEND)

        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.background()

        if self.show_stage:
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            self.stage()
