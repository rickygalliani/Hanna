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
        h1: Holding = Holding(sec1, 1, 10.0, 10.0)
        h2: Holding = Holding(sec2, 2, 20.0, 10.0)
        self.assertNotEqual(h1, h2)

    def test_equality(self):
        sec1: Security = Security("sec1", "SEC1", price=10.0)
        sec2: Security = Security("sec2", "SEC2", price=10.0)
        h1: Holding = Holding(sec1, 1, 10.0, 10.0)
        h2: Holding = Holding(sec2, 1, 10.0, 10.0)
        self.assertNotEqual(h1, h2)

    def test_init_negative_num_shares(self):
        sec: Security = Security("sec", "SEC", price=10.0)
        self.assertRaises(Exception, Holding, sec, -3, 10.0, 10.0)

    def test_init_negative_value(self):
        sec: Security = Security("sec", "SEC", price=10.0)
        self.assertRaises(Exception, Holding, sec, 3, -10.0, 10.0)

    def test_get_return(self):
        sec: Security = Security("sec", "SEC", price=10.0)
        hol: Holding = Holding(sec, 3, 33.0, 10.0)
        self.assertEqual(hol.get_return(), 0.1)

    def test_add_security_mismatch_holding(self):
        sec1: Security = Security("sec1", "SEC1", price=10.0)
        sec2: Security = Security("sec2", "SEC2", price=15.0)
        hol: Holding = Holding(sec1, 3, 30.0, 10.0)
        other_hol: Holding = Holding(sec2, 1, 15.0, 15.0)
        self.assertRaises(Exception, hol.add, other_hol)

    def test_add_normal(self):
        h: Holding = Holding("sec", 1, 100.0, 100.0)
        other_holding: Holding = Holding("sec", 2, 204.0, 102.0)
        h.add(other_holding)
        self.assertEqual(h.get_num_shares(), 3)
        self.assertEqual(h.get_value(), 304.0)
        self.assertEqual(h.get_average_buy_price(), 304.0 / 3)


if __name__ == "__main__":
    unittest.main()
