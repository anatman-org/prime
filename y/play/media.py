from pyglet.media import load as media_load
from pyglet.media import StaticSource

from config import *

# pyglet.options['audio'] = ('pulse', 'xaudio2')

snd_buzz = StaticSource(media_load("m/buzz.wav"))
snd_shutter_start = StaticSource(media_load("m/shutter_start.wav"))
snd_shutter_end = StaticSource(media_load("m/shutter_end.wav"))
