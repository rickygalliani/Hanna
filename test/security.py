# Ricky Galliani
# Hanna
# test/security.py

from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.security


class SecurityTest(unittest.TestCase):

    def test_inequality(self):
        sec1 = Security('sec', 'SEC')
        sec2 = Security('sec', 'SEC', name='sec_name', price=100.0)
        self.assertNotEqual(sec1, sec2)

    def test_equality(self):
        sec1 = Security('sec', 'SEC', name='sec_name', price=100.0)
        sec2 = Security('sec', 'SEC', name='sec_name', price=100.0)
        self.assertEqual(sec1, sec2)

    def test_to_dict_with_nones(self):
        sec = Security('sec', 'SEC')
        test = {
            'id': 'sec',
            'symbol': 'SEC',
            'name': None,
            'price': None,
            'purchase_buffer': 0.0,
            'buy_restricted': 1
        }
        self.assertEqual(sec.to_dict(), test)

    def test_set_price_first_time(self):
        sec = Security('sec', 'SEC')
        sec.set_price(100.0)
        self.assertEqual(sec.get_price(), 100.0)
        self.assertEqual(sec.get_purchase_buffer(), 15.0)

    def test_set_price_update(self):
        sec = Security('sec', 'SEC', price=100.0)
        sec.set_price(200.0)
        self.assertEqual(sec.get_price(), 200.0)
        self.assertEqual(sec.get_purchase_buffer(), 30.0)

    def test_restrict_buy(self):
        sec = Security('sec', 'SEC', buy_restricted=0)
        sec.restrict_buy()
        self.assertEqual(sec.get_buy_restricted(), 1)

    def test_enable_buy(self):
        sec = Security('sec', 'SEC', buy_restricted=1)
        sec.enable_buy()
        self.assertEqual(sec.get_buy_restricted(), 0)

    def test_with_cents(self):
        sec = Security('sec', 'SEC', price=167).with_cents()
        self.assertEqual(sec.get_price(), 16700)

if __name__ == '__main__':
    unittest.main()
