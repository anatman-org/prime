from pyglet.canvas import get_display
from pyglet.clock import tick
from pyglet.app import platform_event_loop

from . import log
from .mat import MatWindow
from .dash import DashWindow
from .images import ImageGlobSequence, ImageGlobCarousel

from config import *


def main():

    display = get_display()
    screens = display.get_screens()

    win_mat = MatWindow(
        1920,
        1080,
        fullscreen=PLAY_FULLSCREEN,
        # style=MatWindow.WINDOW_STYLE_OVERLAY,         # transparent window
        screen=screens[PLAY_SCREEN],
        background_image=BACK_IMAGE,
        stage_image=STAGE_IMAGE,
    )

    win_dash = DashWindow(fullscreen=DASH_FULLSCREEN, screen=screens[DASH_SCREEN])
    win_dash.mat = win_mat

    while True:

        tick()
        platform_event_loop.step(1 / 30)

        win_dash.loop()
