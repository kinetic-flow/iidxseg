#!/usr/bin/env python3

import spiceapi
import argparse
from datetime import datetime
from datetime import timedelta
import time
import pygame
import os
import sys

DEBUG = False

DEFAULT_WIDTH = 520
DEFAULT_ASPECT_RATIO = (52 / 10)
DEFAULT_FONT = "DSEG14Classic-Italic.ttf"

# colors

BLACK = (0, 0, 0)
GRAY = (20, 10, 10)
RED = (255, 0, 0)

# default colors

COLOR_TEXT_ON = RED
COLOR_TEXT_OFF = GRAY
COLOR_BACKGROUND = BLACK

# '!' is all-off character in DSEG14 font
ALL_OFF_CHAR = "!"

# '~' is all-on character in DSEG14 font
ALL_ON_CHAR = "~"

def print_text_in_hex(text):
    print(text)
    for c in text:
        print(ord(c), end=" ")

    print("")

def convert_ticker_text(original_text):
    text = original_text

    if DEBUG:
        print_text_in_hex(original_text)

    # HT (horizontal tab) is sent after !
    text = text.replace(chr(9), " ")
    text = text.replace("!", "./")

    # lower case m = period
    text = text.replace("m", "." + ALL_OFF_CHAR)
    text = text.replace("q", "'")
    text = text.replace("u", ",")
    
    # Make S look more like IIDX
    text = text.replace("S", "5")
    # [ ] are not supported
    text = text.replace("[", "(")
    text = text.replace("]", ")")
    text = text.replace("~", "-")

    # Lastly, blank space must be replaced by all-off character to keep
    # monospace
    text = text.replace(" ", ALL_OFF_CHAR)
    return text

def get_width_and_height(arg_width, arg_height):
    if (arg_width is not None) and (arg_height is not None):
        width = arg_width
        height = arg_height
    elif (arg_width is not None) and (arg_height is None):
        width = arg_width
        height = int(arg_width / DEFAULT_ASPECT_RATIO)
    elif (arg_width is None) and (arg_height is not None):
        width = int(arg_height * DEFAULT_ASPECT_RATIO)
        height = arg_height
    else:
        width = DEFAULT_WIDTH
        height = int(DEFAULT_WIDTH / DEFAULT_ASPECT_RATIO)

    return (width, height)

def get_ticker(con):
    text = spiceapi.iidx_ticker_get(con)
    return convert_ticker_text(text[0])

class Ticker:
    LENGTH = 9
    def __init__(self, surface, offset_y=0):
        self.surface = surface
        self.offset_y = offset_y
        self.__update_font()

    def on_resize(self, new_surface):
        self.surface = new_surface
        self.__update_font()

    def render(self, ticker_text):
        self.__render_text(ALL_ON_CHAR * self.LENGTH, COLOR_TEXT_OFF)
        self.__render_text(ticker_text, COLOR_TEXT_ON)

    def __render_text(self, text, color):
        text = self.font.render(text, True, color)
        x, y = self.surface.get_size()
        text_xy = (x // 2  - text.get_width() // 2,
                   y // 2  - text.get_height() // 2 + self.offset_y)

        self.surface.blit(text, text_xy)

    def __update_font(self):
        font_size = 8
        while True:
            x, y = self.surface.get_size()
            font = self.__get_font(font_size + 2)
            font_x, font_y = font.size(ALL_ON_CHAR * self.LENGTH)
            if font_x <= (x - 20) and font_y <= (y - 10):
                font_size += 2
            else:
                break

        self.font = self.__get_font(font_size)
        pass

    def __get_font(self, size):
        try:
            font = pygame.font.Font(DEFAULT_FONT, size)
            return font
        except:
            print(f"ERROR: font {DEFAULT_FONT} not found! Exiting...")
            sys.exit(-1)

class WallClock:
    DEFAULT_TEXT = ALL_ON_CHAR * 2 + ":" + ALL_ON_CHAR * 2
    def __init__(self, surface, font_size):
        self.surface = surface
        self.font_size = font_size
        self.__update_font()

    def on_resize(self, new_surface):
        self.surface = new_surface
        self.__update_font()

    def render(self):
        self.__render_text(self.DEFAULT_TEXT, COLOR_TEXT_OFF)
        now = datetime.now()
        if (now.microsecond < (500000)) == 0:
            separator = ":"
        else:
            separator = " "
        ticker_text = now.strftime("%I" + separator + "%M")
        self.__render_text(ticker_text, COLOR_TEXT_ON)

    def __render_text(self, text, color):
        text = self.font.render(text, True, color)
        x, y = self.surface.get_size()
        text_xy = (x - text.get_width() - 12,
                   y - text.get_height() - 12)

        self.surface.blit(text, text_xy)

    def __update_font(self):
        self.font = self.__get_font(self.font_size)
        pass

    def __get_font(self, size):
        return pygame.font.Font(DEFAULT_FONT, size)

class StopWatch:
    DEFAULT_TEXT = ALL_ON_CHAR + ":" + ALL_ON_CHAR * 2 + ":" + ALL_ON_CHAR * 2
    def __init__(self, surface, font_size):
        self.surface = surface
        self.font_size = font_size
        self.__update_font()
        self.start_time = datetime.now()

    def on_resize(self, new_surface):
        self.surface = new_surface
        self.__update_font()

    def render(self):
        self.__render_text(self.DEFAULT_TEXT, COLOR_TEXT_OFF)
        time_diff = datetime.now() - self.start_time
        # time_diff += timedelta(hours=9, minutes=59, seconds=50)
        seconds = time_diff.seconds % 60
        minutes = (time_diff.seconds // 60) % 60
        hours = (time_diff.seconds // 60 // 60) % 10
        ticker_text = f"{hours:01}:{minutes:02}:{seconds:02}"
        self.__render_text(ticker_text, COLOR_TEXT_ON)

    def __render_text(self, text, color):
        text = self.font.render(text, True, color)
        x, y = self.surface.get_size()
        text_xy = (12,
                   y - text.get_height() - 12)

        self.surface.blit(text, text_xy)

    def __update_font(self):
        self.font = self.__get_font(self.font_size)
        pass

    def __get_font(self, size):
        return pygame.font.Font(DEFAULT_FONT, size)

def main():

    # parse args
    parser = argparse.ArgumentParser(description="IIDXSEG")
    parser.add_argument("host", type=str)
    parser.add_argument("port", type=int)
    parser.add_argument("password", type=str)
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)
    parser.add_argument("--borderless", action="store_true")
    parser.add_argument("--x", type=int)
    parser.add_argument("--y", type=int)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--clock", action="store_true")
    parser.add_argument("--timer", action="store_true")
    parser.add_argument("--time_font_size", type=int, default=24)
    args = parser.parse_args()

    # give hints to the window manager
    if (args.x is not None) and (args.y is not None):
        os.environ['SDL_VIDEO_WINDOW_POS'] = str(args.x) + "," + str(args.y)

    # init framework
    pygame.init()
    clock = pygame.time.Clock()

    # window properties
    flags = pygame.RESIZABLE
    if args.borderless:
        flags |= pygame.NOFRAME

    # window sizing
    width, height = get_width_and_height(args.width, args.height)

    # set up surface to draw on
    surface = __get_display_surface((width, height), flags)
    pygame.display.set_caption("IIDXSEG")
    ticker = Ticker(surface, offset_y=args.offset)
    if args.clock:
        wallclock = WallClock(surface, args.time_font_size)
    else:
        wallclock = None

    if args.timer:
        stopwatch = StopWatch(surface, args.time_font_size)
    else:
        stopwatch = None

    con = None
    reconnect = False
    failed_connection_attempt = 0

    while True:
        # Check for pygame events
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE)):

                print("exiting ...")
                pygame.quit() 
                sys.exit(0)

            if event.type == pygame.VIDEORESIZE:
                surface = __get_display_surface(event.size, flags)
                ticker.on_resize(surface)
                if wallclock:
                    wallclock.on_resize(surface)
                if stopwatch:
                    stopwatch.on_resize(surface)
                pass

        if (con is None and
            (time.time() - failed_connection_attempt) > 10):

            try:
                print("connecting ...")
                con = spiceapi.Connection(
                          host=args.host,
                          port=args.port,
                          password=args.password)

            except:
                con = None

            if con is None:
                failed_connection_attempt = time.time()

        ticker_text = "CONNECT.!.!."
        if con is not None:
            try:
                ticker_text = get_ticker(con)
            except:
                reconnect = True

            if reconnect:
                try:
                    reconnect = False
                    con.reconnect()
                except:
                    pass
            

        # Render
        surface.fill(COLOR_BACKGROUND) 
        ticker.render(ticker_text)
        if wallclock:
            wallclock.render()
        if stopwatch:
            stopwatch.render()
        pygame.display.flip()
        clock.tick(8)
        pass

def __get_display_surface(size, flags):
    return pygame.display.set_mode(
        size,
        flags=flags
        )

if __name__ == "__main__":
    main()
