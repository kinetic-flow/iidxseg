#!/usr/bin/env python3

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

if __name__ == '__main__':
    unittest.main()