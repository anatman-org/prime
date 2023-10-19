from pathlib import Path

from pyglet.media import load as media_load
from pyglet.media import StaticSource

from random import shuffle

from y.play.media import *

DEBUG = False
HOME_PATH = "/run/media/bean/bean-stash"
FNAME_TEMPLATE = HOME_PATH + "/out/{now:%Y%m%d}/{now:%Y%m%d-%H%M%S-%f}.png"

##### Etup

# BACK_FILES = [str(f) for f in Path(HOME_PATH).glob("out/*/*.png")]
# shuffle(BACK_FILES)
# BACK = MatImageList(BACK_FILES)
BACK = MatVideo(HOME_PATH + "/background.mp4", mute=True)
# BACK = MatImage(HOME_PATH + "/background.png")

# STAGE = MatImage(HOME_PATH + "/mark-0.png")
STAGE = MatImageList([str(f) for f in Path(HOME_PATH).glob("mark*.png")])


#! python -m y.play.test
# 0 Screen at <pyglet.canvas.xlib.XlibDisplay object at 0x7fd600f9e750> at 0 0 with 2560x1440
# 1 Screen at <pyglet.canvas.xlib.XlibDisplay object at 0x7fd600f9e750> at 2560 600 with 1920x1080
# 2 Screen at <pyglet.canvas.xlib.XlibDisplay object at 0x7fd600f9e750> at 2560 0 with 1024x600
DASH_SCREEN = 2
PLAY_SCREEN = 1

PLAY_FULLSCREEN = True
DASH_FULLSCREEN = True

CAMERA = 1
CAMERA_SLEEP = 0.5


if DEBUG:
    DASH_SCREEN = 0
    PLAY_SCREEN = 0

    PLAY_FULLSCREEN = False
    DASH_FULLSCREEN = False


# Stuff that really shouldn't change
SND_buzz = StaticSource(media_load(HOME_PATH + "/buzz.wav"))
SND_shutter_start = StaticSource(media_load(HOME_PATH + "/shutter_start.wav"))
SND_shutter_end = StaticSource(media_load(HOME_PATH + "/shutter_end.wav"))
