#!/usr/bin/env python3

import pygame
from datetime import datetime, timedelta
from constants import *

class Ticker:
    LENGTH = 9
    def __init__(self, surface, font_size=0, offset_y=0):
        self.surface = surface
        self.offset_y = offset_y
        self.preferred_font_size = font_size
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
        if self.preferred_font_size > 0:
            font_size = self.preferred_font_size
        else:
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
