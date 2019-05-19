# Ricky Galliani
# Hanna
# test/holding.py

from src.holding import Holding
from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.holding


class HoldingTest(unittest.TestCase):

    def test_inequality(self):
        sec1 = Security('sec1', 'SEC1', price=10.0)
        sec2 = Security('sec2', 'SEC2', price=20.0)
        h1 = Holding(sec1, 1, 10.0)
        h2 = Holding(sec2, 2, 20.0)
        self.assertNotEqual(h1, h2)

    def test_equality(self):
        sec1 = Security('sec1', 'SEC1', price=10.0)
        sec2 = Security('sec2', 'SEC2', price=10.0)    
        h1 = Holding(sec1, 1, 10.0)
        h2 = Holding(sec2, 1, 10.0)
        self.assertNotEqual(h1, h2)

    def test_buy(self):
        h = Holding('sec', 1, 100.0)
        h.buy(2, 101)
        self.assertEqual(h.get_num_shares(), 3)
        self.assertEqual(h.get_value(), 302.0)

if __name__ == '__main__':
    unittest.main()
