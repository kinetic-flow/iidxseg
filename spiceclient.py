#!/usr/bin/env python3

import spiceapi
import time
import pygame
from constants import *

def spice_client(q, host, port, password):
    con = None
    reconnect = False
    failed_connection_attempt = 0
    clock = pygame.time.Clock()
    while True:
        ticker_text = CONNECTING_TEXT
        if (con is None and
            (time.time() - failed_connection_attempt) > 10):

            try:
                print("connecting ...")
                con = spiceapi.Connection(
                          host=host,
                          port=port,
                          password=password)

            except:
                con = None

            if con is None:
                failed_connection_attempt = time.time()

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

        try:
            q.put(ticker_text)
        except:
            pass

        clock.tick(8)
        pass

def get_ticker(con):
    text = spiceapi.iidx_ticker_get(con)
    return convert_ticker_text(text[0])

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

def print_text_in_hex(text):
    print(text)
    for c in text:
        print(ord(c), end=" ")

    print("")
