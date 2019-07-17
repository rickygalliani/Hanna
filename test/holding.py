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

    def test_get_dividends(self):
        sec: Security = Security("sec", "SEC", price=10.0)
        hol: Holding = Holding(sec, 3, 10.0)
        self.assertEqual(hol.get_dividends(), 0.0)
        hol.set_dividends(5.0)
        self.assertEqual(hol.get_dividends(), 5.0)

    def test_get_cost(self):
        sec: Security = Security("sec", "SEC", price=10.0)
        hol: Holding = Holding(sec, 3, 10.0)
        self.assertEqual(hol.get_cost(), 30.0)

    def test_get_return(self):
        sec: Security = Security("sec", "SEC", price=11.0)
        hol: Holding = Holding(sec, 3, 10.0)
        self.assertEqual(hol.get_return(), 0.1)

    def test_get_return_with_dividends(self):
        sec: Security = Security("sec", "SEC", price=11.0)
        # Value: $33
        # Dividends: $7
        # Cost: $30
        # Return = (Value + Dividends - Cost) / Cost
        #        = (33 + 7 - 30) / 30
        #        = 10 / 30 = 0.33
        hol: Holding = Holding(sec, 3, 10.0, 7.0)
        self.assertEqual(hol.get_return(), 1.0 / 3.0)


if __name__ == "__main__":
    unittest.main()
