from pathlib import Path

from pyglet.media import load as media_load
from pyglet.media import StaticSource

from y.play.media import *

SND_buzz = StaticSource(media_load("media/buzz.wav"))
SND_shutter_start = StaticSource(media_load("media/shutter_start.wav"))
SND_shutter_end = StaticSource(media_load("media/shutter_end.wav"))

#BACK = MatImage("media/background.png")
BACK = MatVideo("media/background.mp4")

#STAGE = MatImage("media/marks-1a.png")
STAGE = MatImageList( [ str(f) for f in Path.cwd().glob("media/marks-*.png") ] )

FNAME_TEMPLATE = "media/out/{now:%Y%m%d}/{now:%Y%m%d-%H%M%S-%f}.png"

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

    CAMERA = 0
