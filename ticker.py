#!/usr/bin/env python3

import spiceapi
import argparse
import time
import pygame

DEBUG = False

black = (0, 0, 0)
gray = (12, 12, 12)
red = (255, 0, 0)

X = 520
Y = 100

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
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font("DSEG14Classic-Italic.ttf", 64)

    def render(self, ticker_text):
        self.screen.fill(black) 
        
        self.__render_text(all_on_text, gray)
        self.__render_text(ticker_text, red)
        pygame.display.flip()

    def __render_text(self, text, color):
        text = self.font.render(text, True, color)
        self.text_xy = (X // 2  - text.get_width() // 2, Y // 2  - text.get_height() // 2)
        self.screen.blit(text, self.text_xy)

def main():

    # parse args
    parser = argparse.ArgumentParser(description="IIDXSEG")
    parser.add_argument("host", type=str)
    parser.add_argument("port", type=int)
    parser.add_argument("password", type=str)
    args = parser.parse_args()

    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((X, Y))
    pygame.display.set_caption("IIDXSEG")
    ticker = Ticker(screen)

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

if __name__ == "__main__":
    main()
