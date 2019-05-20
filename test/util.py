# Ricky Galliani
# Hanna
# test/util.py

from src.util import dollar_str, pct_str

import unittest

# Usage: python3 -m unittest --verbose test.util


class UtilTest(unittest.TestCase):

    def test_dollar_str(self):
        self.assertEqual(dollar_str(100.892342), '$100.89')

    def test_pct_str(self):
        self.assertEqual(pct_str(0.351783423234), '35.2%')