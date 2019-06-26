# Ricky Galliani
# Hanna
# test/holding.py

from src.holding import Holding
from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.holding


class HoldingTest(unittest.TestCase):
    def test_inequality(self):
        sec1: Security = Security("sec1", "SEC1", price=10.0)
        sec2: Security = Security("sec2", "SEC2", price=20.0)
        h1: Holding = Holding(sec1, 1, 10.0)
        h2: Holding = Holding(sec2, 2, 10.0)
        self.assertNotEqual(h1, h2)

    def test_equality(self):
        sec1: Security = Security("sec1", "SEC1", price=10.0)
        sec2: Security = Security("sec2", "SEC2", price=10.0)
        h1: Holding = Holding(sec1, 1, 10.0)
        h2: Holding = Holding(sec2, 1, 10.0)
        self.assertNotEqual(h1, h2)

    def test_init_negative_num_shares(self):
        sec: Security = Security("sec", "SEC", price=10.0)
        self.assertRaises(Exception, Holding, sec, -3, 10.0)

    def test_get_return(self):
        sec: Security = Security("sec", "SEC", price=11.0)
        hol: Holding = Holding(sec, 3, 10.0)
        self.assertEqual(hol.get_return(), 0.1)


if __name__ == "__main__":
    unittest.main()
