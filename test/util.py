# Ricky Galliani
# Hanna
# test/util.py

from src.util import dollar_str, difference_in_millis, latency_str, pct_str

from datetime import datetime, timedelta

import unittest

# Usage: python3 -m unittest --verbose test.util


class UtilTest(unittest.TestCase):
    def test_dollar_str(self):
        self.assertEqual(dollar_str(100.892342), "$100.89")

    def test_pct_str(self):
        self.assertEqual(pct_str(0.351783423234), "35.2%")

    def test_difference_in_millis(self):
        start = datetime(2019, 1, 1)
        end = start + timedelta(milliseconds=1000)
        self.assertEqual(difference_in_millis(start, end), 1000)

    def test_latency_str(self):
        start = datetime(2019, 1, 1)
        end = start + timedelta(milliseconds=1000)
        self.assertEqual(latency_str(start, end), "1000 ms")
