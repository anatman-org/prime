from pyglet.window import Window
from pyglet.canvas import get_display
from pyglet.clock import tick
from pyglet.app import platform_event_loop

from . import log
from .mat import Mat
from .dash import DashWindow
from .images import ImageGlobSequence, ImageGlobCarousel

from config import *


def main():

    display = get_display()
    screens = display.get_screens()

    win_mat = Window(
        1920,
        1080,
        screen=screens[PLAY_SCREEN],
        fullscreen=PLAY_FULLSCREEN,
        # style=MatWindow.WINDOW_STYLE_OVERLAY,         # transparent window
    )

    mat = Mat(win_mat, BACK_IMAGE, STAGE_IMAGE)

    dash = DashWindow(fullscreen=DASH_FULLSCREEN, screen=screens[DASH_SCREEN])
    dash.mat = mat

    while True:

        tick()
        platform_event_loop.step(1 / 30)

        dash.loop()
