# Ricky Galliani
# Hanna
# test/purchase.py

from src.purchase import Purchase

import unittest

# Usage: python3 -m unittest --verbose test.purchase


class PurchaseTest(unittest.TestCase):

    def test_inequality(self):
        p1 = Purchase('sec', 'sec_name', 5, 10.0)
        p2 = Purchase('sec', 'sec_name', 6, 10.0)
        self.assertNotEqual(p1, p2)

    def test_equality(self):
        p1 = Purchase('sec', 'sec_name', 5, 10.0)
        p2 = Purchase('sec', 'sec_name', 5, 10.0)
        self.assertEqual(p1, p2)


if __name__ == '__main__':
    unittest.main()
