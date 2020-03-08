#!/usr/bin/env python3

import argparse

def parse_args():
    parser = argparse.ArgumentParser(description="IIDXSEG")
    parser.add_argument("host", type=str)
    parser.add_argument("port", type=int)
    parser.add_argument("password", type=str)
    parser.add_argument(
        "--width",
        type=int,
        help="Width of the window")
    parser.add_argument(
        "--height",
        type=int,
        help="Height of the window")
    parser.add_argument(
        "--borderless",
        action="store_true",
        help="Remove window border and title bar")
    parser.add_argument(
        "--x",
        type=int,
        help="Desired x-coordinate for the window position")
    parser.add_argument(
        "--y",
        type=int,
        help="Desired y-coordinate for the window position")
    parser.add_argument(
        "--font_size",
        type=int,
        default=0,
        help="Preferred font size for the ticker. When omitted, the ticker will fill the window")
    parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Desired y-offset in pixels to shift the ticker up (negative) or down (positive)")
    parser.add_argument(
        "--clock",
        action="store_true",
        help="Show the wall clock")
    parser.add_argument(
        "--timer",
        action="store_true",
        help="Show the stop watch")
    parser.add_argument(
        "--time_font_size",
        type=int,
        default=24,
        help="Desired font size for the wall clock and the stop watch")
    parser.add_argument(
        "--color",
        type=str,
        default="0xff0000",
        help="Desired color (e.g., 0x00ff00 for green), or 'rgb'")
    args = parser.parse_args()
    return args
