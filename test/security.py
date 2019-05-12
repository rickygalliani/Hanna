# Ricky Galliani
# Hanna
# test/security.py

from src.robinhood_holding import RobinhoodHolding
from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.security

class SecurityTest(unittest.TestCase):

    def test_inequality(self):
        sec1 = Security('sec')
        sec2 = Security('sec', 'sec_name', 1, 100.0, 100.0)
        self.assertNotEqual(sec1, sec2)

    def test_equality(self):
        sec1 = Security('sec', 'sec_name', 1, 100.0, 100.0)
        sec2 = Security('sec', 'sec_name', 1, 100.0, 100.0)
        self.assertEqual(sec1, sec2)

    def test_with_cents(self):
        sec = Security('sec', price=167).with_cents()
        self.assertEqual(sec.price, 16700)

    def test_update(self):
        sec = Security('sec')
        rh = RobinhoodHolding(
            holding_id='sec',
            name='sec_name',
            price=50.0,
            quantity=1,
            average_buy_price=50.0,
            equity=50.0,
            percentage=50.0,
            percent_change=0.0,
            equity_change=0.0,
            holding_type='etp'
        )
        sec.update(rh)
        sec_check = Security('sec', 'sec_name', 1, 50.0, 50.0)
        self.assertEqual(sec, sec_check)

if __name__ == '__main__':
    unittest.main()