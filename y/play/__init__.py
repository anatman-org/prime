#!/usr/bin/env python
""" The base application for tracking games in play
    It opens two windows, one a "Guide" and another a "Control".
    
    The "Guide" window is intended to project onto the mat,
    providing a virtual two-dimensional surface.
    
    There are two layers:
    
        the base layer is the background that is projected
            and left in play during recording
        the "guide" layer only appears during backstage preparations,
            and is removed during recordin
            
    The control window has feedback on current game and progress.
"""
from datetime import datetime
from time import sleep
import logging
import sys
import traceback

# Setting up log handler
logging.captureWarnings(True)
log = logging.getLogger("lusor")
log.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s", "%m-%d-%Y %H:%M:%S"
)

file_handler = logging.FileHandler("lusor.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)
log.addHandler(file_handler)


def log_exceptions(type, value, tb):
    for line in traceback.TracebackException(type, value, tb).format(chain=True):
        logging.exception(line)
    logging.exception(value)

    sys.__excepthook__(type, value, tb)  # calls default excepthook


if __name__ == "__main__":

    from .main import main

    main()
