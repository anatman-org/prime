import os
from datetime import datetime
from time import sleep
from pathlib import Path

# import pyglet
from pyglet.window import Window
from pyglet.text import Label
from pyglet.image import load as image_load
from pyglet.window import key as key_code

os.environ["OPENCV_LOG_LEVEL"] = "FATAL"
from cv2 import VideoCapture, imwrite, imshow

from . import log

from config import *


class DashWindow(Window):

    state: str = "ready"
    mat = None
    back = None
    camera = None
    count = 0

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.camera = VideoCapture(CAMERA)

    def on_draw(self):
        self.clear()
        dash_cmd = Label(
            self.state,
            font_name="Arial",
            bold=True,
            font_size=24,
            x=self.width // 2,
            y=self.height // 2,
            anchor_x="center",
            anchor_y="center",
        )
        dash_cmd.draw()

    def on_key_release(self, key, modifier):

        if key in [key_code.ENTER, key_code.SPACE, key_code.NUM_ENTER]:
            self.snapshot()

        # Background Keys
        elif key in [key_code._1, key_code.NUM_1]:
            self.mat.background.prev()

        elif key in [key_code._2, key_code.NUM_2]:
            self.mat.background.pause()

        elif key in [key_code._3, key_code.NUM_2]:
            self.mat.background.next()

        # Stage Keys
        elif key in [key_code._0, key_code.NUM_0]:
            self.mat.show_stage = not self.mat.show_stage
            self.mat()

        elif key in [key_code._4, key_code.NUM_4]:
            self.mat.stage.prev()

        elif key in [key_code._5, key_code.NUM_5]:
            self.mat.stage.pause()

        elif key in [key_code._6, key_code.NUM_6]:
            self.mat.stage.next()

        elif key in [key_code._5, key_code.NUM_5]:
            self.mat.stage.pause()

        # Break
        elif key == key_code.B:
            exit()

    def loop(self):

        self.mat()

        self.switch_to()
        self.dispatch_events()
        self.dispatch_event("on_draw")
        self.flip()

    def take_photo(self, fname):
        sleep(CAMERA_SLEEP)

        result, image = self.camera.read()

        if not result:
            raise Exception(f"Failed to get result for {fname}")

        directory = Path(fname).parent
        if not directory.exists():
            directory.mkdir(parents=True)

        size = imwrite(fname, image)
        if not size:
            raise Exception(f"Failed to write {fname}")

        self.mat.background.next()
        if self.mat.stage.autoincrement:
            try:
                self.mat.stage.next()
            except:
                log.error("Caught error trying to advance stage")
                pass

    def snapshot(self):

        now = datetime.now()
        fname = eval('f"' + FNAME_TEMPLATE + '"')

        self.state = f"Taking {fname}"

        need_to_unpause = False
        if self.mat.background.state < 0:
            self.mat.background.pause()
            need_to_unpause = True

        old_mat_state = self.mat.show_stage
        self.mat.show_stage = False

        self.loop()

        SND_shutter_start.play()
        self.take_photo(fname)
        SND_shutter_end.play()

        # Return states
        self.mat.show_stage = old_mat_state
        if need_to_unpause:
            self.mat.background.pause()

        self.loop()

        self.count += 1

        self.state = f"TOOK {fname} [{self.count}]"
        log.info(self.state)
