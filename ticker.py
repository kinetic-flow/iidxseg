#!/usr/bin/env python3

import argparse
import pygame
import os
import sys
import multiprocessing
from multiprocessing import Process, Queue
from constants import *

# internal
import spiceclient
import widgets
import config

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

def generate_color(option):
    if option == "rgb":
        rgb = pygame.Color(*RED)
        while True:
            hue = rgb.hsva[0]
            hue = (hue + 2) % 360
            rgb.hsva = (hue, *rgb.hsva[1:])
            yield rgb
    else:
        fixed_color = pygame.Color(option)
        while True:
            yield fixed_color

def main():
    args = config.parse_args()

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
    ticker = widgets.Ticker(surface, font_size=args.font_size, offset_y=args.offset)
    if args.clock:
        wallclock = widgets.WallClock(surface, args.time_font_size)
    else:
        wallclock = None

    if args.timer:
        stopwatch = widgets.StopWatch(surface, args.time_font_size)
    else:
        stopwatch = None

    # multiprocessing
    q = Queue(maxsize=2)
    p = Process(
        target=spiceclient.spice_client,
        args=(q, args.host, args.port, args.password))
    p.start()

    # ticker stuff
    last_ticker_text = CONNECTING_TEXT
    color_generator = generate_color(args.color)
    while True:
        # Check for pygame events
        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE)):

                print("exiting ...")
                exit_app(p)

            if event.type == pygame.VIDEORESIZE:
                # reset the preferred window position now that the user changed
                # the size or the location
                os.environ['SDL_VIDEO_WINDOW_POS'] = ""
                surface = __get_display_surface(event.size, flags)
                ticker.on_resize(surface)
                if wallclock:
                    wallclock.on_resize(surface)
                if stopwatch:
                    stopwatch.on_resize(surface)
                pass

        # grab ticker text from queue
        try:
            ticker_text = q.get(block=False)
        except:
            ticker_text = None

        if ticker_text:
            last_ticker_text = ticker_text
        else:
            ticker_text = last_ticker_text

        # Render
        surface.fill(COLOR_BACKGROUND) 
        color = next(color_generator)
        ticker.render(ticker_text, color)
        if wallclock:
            wallclock.render(color)
        if stopwatch:
            stopwatch.render(color)
        pygame.display.flip()
        clock.tick(8)
        pass

def __get_display_surface(size, flags):
    return pygame.display.set_mode(
        size,
        flags=flags
        )

def exit_app(process):
    pygame.quit()
    if process:
        process.terminate()
    sys.exit(0)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
