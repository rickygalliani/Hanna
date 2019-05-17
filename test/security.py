# Ricky Galliani
# Hanna
# test/security.py

from src.robinhood_holding import RobinhoodHolding
from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.security


class SecurityTest(unittest.TestCase):

    def test_inequality(self):
        sec1 = Security('sec', 'SEC')
        sec2 = Security('sec', 'SEC', 'sec_name', 100.0)
        self.assertNotEqual(sec1, sec2)

    def test_equality(self):
        sec1 = Security('sec', 'SEC', 'sec_name', 100.0)
        sec2 = Security('sec', 'SEC', 'sec_name', 100.0)
        self.assertEqual(sec1, sec2)

    def test_with_cents(self):
        sec = Security('sec', 'SEC', price=167).with_cents()
        self.assertEqual(sec.get_price(), 16700)

if __name__ == '__main__':
    unittest.main()
