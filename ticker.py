#!/usr/bin/env python3

import spiceapi
import argparse
import time
import pygame
from collections import namedtuple

DEBUG = False

# colors

black = (0, 0, 0)
gray = (12, 12, 12)
red = (255, 0, 0)

all_off_char = "!"

# '!' is all-off character in DSEG14 font
all_off_text = "!!!!!!!!!"

# '~' is all-on character in DSEG14 font
all_on_text = "~~~~~~~~~"

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
    text = text.replace("m", "." + all_off_char)
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
    text = text.replace(" ", all_off_char)
    return text

def get_ticker(con):
    text = spiceapi.iidx_ticker_get(con)
    return convert_ticker_text(text[0])

class Ticker:
    def __init__(self, surface):
        self.surface = surface
        self.__update_font()

    def on_resize(self, new_surface):
        self.surface = new_surface
        self.__update_font()

    def render(self, ticker_text):
        self.surface.fill(black) 
        
        self.__render_text(all_on_text, gray)
        self.__render_text(ticker_text, red)
        pygame.display.flip()

    def __render_text(self, text, color):
        text = self.font.render(text, True, color)

        x, y = self.surface.get_size()
        self.text_xy = (x // 2  - text.get_width() // 2, y // 2  - text.get_height() // 2)
        self.surface.blit(text, self.text_xy)

    def __update_font(self):
        font_size = 8
        while True:
            x, y = self.surface.get_size()
            font = self.__get_font(font_size + 2)
            font_x, font_y = font.size(all_on_text)
            if font_x <= x and font_y <= y:
                font_size += 2
            else:
                break

        self.font = self.__get_font(font_size)
        pass

    def __get_font(self, size):
        return pygame.font.Font("DSEG14Classic-Italic.ttf", size)

def main():

    # parse args
    parser = argparse.ArgumentParser(description="IIDXSEG")
    parser.add_argument("host", type=str)
    parser.add_argument("port", type=int)
    parser.add_argument("password", type=str)
    parser.add_argument("--width", type=int, default=520)
    parser.add_argument("--height", type=int, default=100)
    args = parser.parse_args()

    pygame.init()
    clock = pygame.time.Clock()

    # initialize the screen
    surface = __get_display_surface((args.width, args.height))
    pygame.display.set_caption("IIDXSEG")
    ticker = Ticker(surface)

    quitting = False
    con = None
    reconnect = False

    while not quitting:
        # Check for pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quitting = True
                pygame.quit() 
                quit()

            if event.type == pygame.VIDEORESIZE:
                surface = __get_display_surface(event.size)
                ticker.on_resize(surface)
                pass

        if con is None:
            try:
                con = spiceapi.Connection(host=args.host, port=args.port, password=args.password)
                print("reconnecting ...")
            except:
                con = None

        ticker_text = all_on_text
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
        ticker.render(ticker_text)
        clock.tick(8)
        pass

def __get_display_surface(size):
    flags = pygame.RESIZABLE
    return pygame.display.set_mode(
        size,
        flags=flags
        )

if __name__ == "__main__":
    main()
