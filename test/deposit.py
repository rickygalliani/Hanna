# Ricky Galliani
# Hanna
# test/deposit.py

from src.deposit import Deposit
from src.purchase import Purchase
from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.deposit


class DepositTest(unittest.TestCase):

    def test_inequality(self):
        d1 = Deposit()
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        d1.add_purchase('ac', Purchase(sec, 5))
        d2 = Deposit()
        self.assertNotEqual(d1, d2)

    def test_equality(self):
        sec = Security('sec', 'SEC', 'sec_name', 10.0, False)
        pur = Purchase(sec, 5)
        d1 = Deposit()
        d1.add_purchase('ac', pur)
        d2 = Deposit()
        d2.add_purchase('ac', pur)
        self.assertEqual(d1, d2)

    def test_get_purchase_for_asset_class(self):
        # TODO
        self.assertTrue(True)

    def test_add_purchase(self):
        d = Deposit()
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        pur = Purchase(sec, 5)
        d.add_purchase('ac', pur)
        self.assertEqual(d.get_total(), 50.0)
        self.assertTrue(pur in d.get_purchases_for_asset_class('ac'))

    def test_get_asset_class_expenditures(self):
        d = Deposit()
        sec1 = Security('sec1', 'SEC1', 'sec1_name', 10.0, False)
        sec2 = Security('sec2', 'SEC2', 'sec2_name', 5.0, False)
        d.add_purchase('ac', Purchase(sec1, 5))
        d.add_purchase('ac', Purchase(sec2, 10))
        self.assertEqual(d.get_asset_class_expenditures('ac'), 100.0)


if __name__ == '__main__':
    unittest.main()
