# Ricky Galliani
# Hanna
# test/deposit.py

from src.deposit import Deposit
from src.purchase import Purchase

import unittest

# Usage: python3 -m unittest --verbose test.deposit

class DepositTest(unittest.TestCase):

    def test_inequality(self):
        d1 = Deposit()
        d1.add_purchase('ac', Purchase('sec', 'sec_name', 5, 10.0))
        d2 = Deposit()
        self.assertNotEqual(d1, d2)

    def test_equality(self):
        pur = Purchase('sec', 'sec_name', 5, 10.0)
        d1 = Deposit()
        d1.add_purchase('ac', pur)
        d2 = Deposit()
        d2.add_purchase('ac', pur)
        self.assertEqual(d1, d2)

    def test_add_purchase(self):
        d = Deposit()
        pur = Purchase('sec', 'sec_name', 5, 10.0)
        d.add_purchase('ac', pur)
        self.assertEqual(d.total, 50.0)
        self.assertTrue(pur in d.purchases['ac'])

    def test_get_asset_class_expenditures(self):
        d = Deposit()
        d.add_purchase('ac', Purchase('sec1', 'sec1_name', 5, 10.0))
        d.add_purchase('ac', Purchase('sec2', 'sec2_name', 10, 5.0))
        self.assertEqual(d.get_asset_class_expenditures('ac'), 100.0)

if __name__ == '__main__':
    unittest.main()