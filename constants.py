#!/usr/bin/env python3

import os
import sys

DEBUG = False

DEFAULT_WIDTH = 520
DEFAULT_ASPECT_RATIO = (52 / 10)

if getattr(sys, 'frozen', False):
    CurrentPath = sys._MEIPASS
else:
    CurrentPath = os.path.dirname(__file__)
DEFAULT_FONT = os.path.join(CurrentPath, 'DSEG14Classic-Italic.ttf')

CONNECTING_TEXT = "CONNECT.!.!."

# colors

BLACK = (0, 0, 0)
GRAY = (20, 20, 20)
RED = (255, 0, 0)

# default colors

COLOR_TEXT_ON = RED
COLOR_TEXT_OFF = GRAY
COLOR_BACKGROUND = BLACK

# '!' is all-off character in DSEG14 font
ALL_OFF_CHAR = "!"

# '~' is all-on character in DSEG14 font
ALL_ON_CHAR = "~"