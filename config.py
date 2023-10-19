from pathlib import Path

from pyglet.media import load as media_load
from pyglet.media import StaticSource

from y.play.media import *

HOME_PATH=Path().home()

SND_buzz = StaticSource(media_load("/data/buzz.wav"))
SND_shutter_start = StaticSource(media_load("/data/shutter_start.wav"))
SND_shutter_end = StaticSource(media_load("/data/shutter_end.wav"))

# BACK = MatImage("media/background.png")
# BACK = MatImageList([str(f) for f in HOME_PATH.glob("media/data/out/202310*/*.png")])
# BACK = MatImageList([str(f) for f in HOME_PATH.glob("media/data/background*.png")])
BACK = MatVideo(str(HOME_PATH) + "/media/bean-stash/background.mp4")

# STAGE = MatImage(str(HOME_PATH) + "media/marks-1a.png")
STAGE = MatImageList([str(f) for f in HOME_PATH.glob("media/bean-stash/mark*.png")])

FNAME_TEMPLATE = str(HOME_PATH) + "/media/bean-stash/{now:%Y%m%d}/{now:%Y%m%d-%H%M%S-%f}.png"

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


DEBUG = False
if DEBUG:
    DASH_SCREEN = 0
    PLAY_SCREEN = 0

    PLAY_FULLSCREEN = False
    DASH_FULLSCREEN = False
