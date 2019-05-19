# Ricky Galliani
# Hanna
# test/asset_class.py

from src.asset_class import AssetClass
from src.holding import Holding
from src.purchase import Purchase
from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.asset_class


class AssetClassTest(unittest.TestCase):

    def test_inequality(self):
        ac1 = AssetClass('ac', target_percentage=1.0)
        ac2 = AssetClass('ac', target_percentage=1.0)
        ac2.add_security(Security('sec', 'SEC'))
        self.assertNotEqual(ac1, ac2)

    def test_equality(self):
        ac1 = AssetClass('ac', target_percentage=1.0)
        ac2 = AssetClass('ac', target_percentage=1.0)
        sec = Security('sec', 'SEC', 1, 100.0)
        ac1.add_security(sec)
        ac2.add_security(sec)
        self.assertEqual(ac1, ac2)

    def test_add_value(self):
        ac = AssetClass('ac', target_percentage=1.0)
        ac.add_value(100.0)
        self.assertEqual(ac.get_value(), 100.0)

    def test_add_security_new(self):
        ac = AssetClass('ac', target_percentage=1.0)
        ac.add_security(Security('sec', 'SEC'))
        self.assertEqual(ac.get_security('sec'), Security('sec', 'SEC'))

    def test_add_security_update(self):
        ac = AssetClass('ac', target_percentage=1.0)
        ac.add_security(Security('sec', 'SEC', 'old_name', 25.0))
        ac.add_security(Security('sec', 'SEC', 'sec_name', 15.0))
        self.assertEqual(ac.get_security('sec').get_name(), 'sec_name')
        self.assertEqual(ac.get_security('sec').get_price(), 15.0)

    def test_contains_security_false(self):
        ac = AssetClass('ac', target_percentage=1.0)
        self.assertFalse(ac.contains_security('sec'))

    def test_contains_security_true(self):
        ac = AssetClass('ac', target_percentage=1.0)
        ac.add_security(Security('sec', 'SEC'))
        self.assertTrue(ac.contains_security('sec'))

    def test_get_security(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec = Security('sec', 'SEC')
        ac.add_security(sec)
        self.assertEqual(ac.get_security('sec'), sec)

    def test_add_holding_new(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec = Security('sec', 'SEC', price=5.0)
        ac.add_holding(sec, 3)
        self.assertEqual(ac.get_holding('sec'), Holding(sec, 3, 15.0))
        self.assertEqual(ac.get_value(), 15.0)

    def test_add_holding_update(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec = Security('sec', 'SEC', price=5.0)
        ac.add_holding(sec, 3)
        sec.set_price(15.0)
        ac.add_holding(sec, 3)
        self.assertEqual(ac.get_holding('sec'), Holding(sec, 6, 60.0))
        self.assertEqual(ac.get_value(), 60.0)

    def test_contains_holding_false(self):
        ac = AssetClass('ac', target_percentage=1.0)
        self.assertFalse(ac.contains_holding('sec'))

    def test_contains_holding_true(self):
        ac = AssetClass('ac', target_percentage=1.0)
        ac.add_holding(Security('sec', 'SEC', 'sec_name', 15.0), 3)
        self.assertTrue(ac.contains_holding('sec'))

    def test_get_holding(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec = Security('sec', 'SEC', 'sec_name', 15.0)
        ac.add_holding(sec, 3)
        self.assertEqual(ac.get_holding('sec'), Holding(sec, 3, 45.0))

    def test_update_security(self):
        ac = AssetClass('ac', target_percentage=0.5)
        sec = Security('sec', 'SEC')
        ac.add_security(sec)
        sec_info = {"name": "Security A", "price": 100.0}
        ac.update_security('sec', sec_info)
        self.assertEqual(ac.get_security('sec'), sec)

    def test_update_holding(self):
        ac = AssetClass('ac', target_percentage=0.5)
        sec = Security('sec', 'SEC', 'sec_name', 40.0, 0)
        ac.add_security(sec)
        holding_info = {
            'id': 'sec',
            'name': 'sec_name',
            'price': 40.0,
            'quantity': 5,
            'average_buy_price': 40.0,
            'equity': 200.0,
            'percentage': 40.0,
            'percent_change': 0.0,
            'equity_change': 0.0,
            'holding_type': 'etp'
        }
        ac.add_holding(sec, 1)
        ac.update_holding(sec, holding_info)
        self.assertEqual(ac.get_holding('sec'), Holding(sec, 5, 200))

    def test_plan_purchases_knapsack_test_1(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec1 = Security('sec1', 'SEC1', 'sec1_name', 33.0, 0)
        sec2 = Security('sec2', 'SEC2', 'sec2_name', 49.0, 0)
        ac.add_security(sec1)
        ac.add_security(sec2)
        purchases = ac.plan_purchases(100)
        p1 = Purchase(sec1, 3)
        p2 = Purchase(sec2, 0)
        self.assertEqual(purchases['sec1'], p1)
        self.assertEqual(purchases['sec2'], p2)

    def test_plan_purchases_knapsack_test_2(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec1 = Security('sec1', 'SEC1', 'sec1_name', 33.0, 0)
        sec2 = Security('sec2', 'SEC2', 'sec2_name', 49.0, 0)
        ac.add_security(sec1)
        ac.add_security(sec2)
        purchases = ac.plan_purchases(98.5)
        p1 = Purchase(sec1, 0)
        p2 = Purchase(sec2, 2)
        self.assertEqual(purchases['sec1'], p1)
        self.assertEqual(purchases['sec2'], p2)

    def test_plan_purchases_buy_restricted_test_1(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec1 = Security('sec1', 'SEC1', 'sec1_name', 33.0, 0)
        sec2 = Security('sec2', 'SEC2', 'sec2_name', 49.0, 1)
        ac.add_security(sec1)
        ac.add_security(sec2)
        purchases = ac.plan_purchases(98.5)
        p1 = Purchase(sec1, 2)
        self.assertEqual(len(purchases), 1)
        self.assertEqual(purchases['sec1'], p1)

if __name__ == '__main__':
    unittest.main()
