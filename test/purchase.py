# Ricky Galliani
# Hanna
# test/purchase.py

from src.purchase import Purchase
from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.purchase


class PurchaseTest(unittest.TestCase):

    def test_inequality(self):
        p1 = Purchase(Security('sec', 'SEC', 'sec_name', 10.0), 5)
        p2 = Purchase(Security('sec', 'SEC', 'sec_name', 10.0), 6)
        self.assertNotEqual(p1, p2)

    def test_equality(self):
        p1 = Purchase(Security('sec', 'SEC', 'sec_name', 10.0), 5)
        p2 = Purchase(Security('sec', 'SEC', 'sec_name', 10.0), 5)
        self.assertEqual(p1, p2)

    def test_init_security_null_price(self):
        # TODO
        pass

    def test_init_zero_shares(self):
        # TODO
        pass

if __name__ == '__main__':
    unittest.main()
