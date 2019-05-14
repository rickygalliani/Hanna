# Ricky Galliani
# Hanna
# test/holding.py

from src.robinhood_holding import RobinhoodHolding
from src.holding import Holding

import unittest

# Usage: python3 -m unittest --verbose test.holding


class HoldingTest(unittest.TestCase):

    def test_inequality(self):
        h1 = Holding('sec1', 1, 10.0)
        h2 = Holding('sec2', 2, 20.0)
        self.assertNotEqual(h1, h2)

    def test_equality(self):
        h1 = Holding('sec1', 1, 10.0)
        h2 = Holding('sec2', 1, 10.0)
        self.assertNotEqual(h1, h2)

    def test_add_shares(self):
        h = Holding('sec', 1, 15.0)
        h.add_shares(5)
        self.assertEqual(h.num_shares, 6)

    def test_add_value(self):
        h = Holding('sec', 1, 15.0)
        h.add_value(55.0)
        self.assertEqual(h.value, 70.0)

    def test_update(self):
        h = Holding('sec', 1, 10.0)
        rh = RobinhoodHolding(
            holding_id='sec',
            name='sec_name',
            price=25.0,
            quantity=2,
            average_buy_price=15.0,
            equity=50.0,
            percentage=50.0,
            percent_change=0.0,
            equity_change=0.0,
            holding_type='etp'
        )
        h.update(rh)
        h_check = Holding('sec', 2, 50.0)
        self.assertEqual(h, h_check)

    def test_buy(self):
        h = Holding('sec', 1, 100.0)
        h.buy(2, 101)
        self.assertEqual(h.num_shares, 3)
        self.assertEqual(h.value, 302.0)


if __name__ == '__main__':
    unittest.main()
