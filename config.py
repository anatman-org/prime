from pathlib import Path
from random import shuffle

from y.play.media import *
from y.play.animate import *

###############################################################################
DEBUG = False

# MEDIA_BASE_DIR = str(Path().home())
MEDIA_BASE_DIR = "/data"

# FNAME_TEMPLATE = MEDIA_BASE_DIR + "/out/bean/{now:%Y%m%d-%H%M%S-%f}.png"
# FNAME_TEMPLATE = MEDIA_BASE_DIR + "/home/bean/stash/media/clips/{now:%Y%m%d-%H%M%S-%f}.png"

FNAME_TEMPLATE = MEDIA_BASE_DIR + "/out/d62b31da/{now:%Y%m%d-%H%M%S-%f}.png"



###############################################################################

# BACK = MatImage(MEDIA_BASE_DIR + "/background.png")
# BACK = MatVideo(MEDIA_BASE_DIR + "/background.mp4", volume=0)
# _BACK_FILES = [str(f) for f in Path(MEDIA_BASE_DIR).glob("out/*/*.png")]
# shuffle(_BACK_FILES)
# BACK = MatImageList(_BACK_FILES)
BACK = MatSpin(file="img/enso.png", rotation_speed=6)

# STAGE = MatImage(MEDIA_BASE_DIR + "/mark-0.png")
_STAGE_FILES = [str(f) for f in Path(MEDIA_BASE_DIR).glob("mark*.png")]
STAGE = MatImageList(_STAGE_FILES)
# STAGE = MatVideo(MEDIA_BASE_DIR + "/clips/BasQZAidNKc.mp4", volume=0, autoplay=False)

###############################################################################
# Stuff that really shouldn't change

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
SND_buzz = StaticSource(media_load(MEDIA_BASE_DIR + "/buzz.wav"))
SND_shutter_start = StaticSource(media_load(MEDIA_BASE_DIR + "/shutter_start.wav"))
SND_shutter_end = StaticSource(media_load(MEDIA_BASE_DIR + "/shutter_end.wav"))

if DEBUG:
    DASH_SCREEN = 0
    PLAY_SCREEN = 0

    PLAY_FULLSCREEN = False
    DASH_FULLSCREEN = False

