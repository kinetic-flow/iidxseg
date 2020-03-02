#!/usr/bin/env python3

# python -m unittest tickertest.py

import unittest
import ticker

class TestTickerTextConversion(unittest.TestCase):

    def test_upper(self):
        self.assertEqual(
            ticker.convert_ticker_text("SSSSSSSSS"),
            "555555555")
        self.assertEqual(
            ticker.convert_ticker_text("[][][][]["),
            "()()()()(")
        self.assertEqual(
            ticker.convert_ticker_text("         "),
            "!!!!!!!!!")

class TestWindowSizeArgs(unittest.TestCase):

    def test(self):
        self.assertEqual(
           ticker.get_width_and_height(None, None),
           (520, 100))

        self.assertEqual(
           ticker.get_width_and_height(100, None),
           (100, 19))

        self.assertEqual(
           ticker.get_width_and_height(None, 200),
           (1040, 200))

        self.assertEqual(
           ticker.get_width_and_height(0, 1),
           (0, 1))

if __name__ == '__main__':
    unittest.main()