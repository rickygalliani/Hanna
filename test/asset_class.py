# Ricky Galliani
# Hanna
# test/asset_class.py

from src.asset_class import AssetClass
from src.holding import Holding
from src.purchase import Purchase
from src.robinhood_holding import RobinhoodHolding
from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.asset_class


class AssetClassTest(unittest.TestCase):

    def test_inequality(self):
        ac1 = AssetClass('ac', target_percentage=1.0)
        ac2 = AssetClass('ac', target_percentage=1.0)
        ac2.add_security(Security('sec'))
        self.assertNotEqual(ac1, ac2)

    def test_equality(self):
        ac1 = AssetClass('ac', target_percentage=1.0)
        ac2 = AssetClass('ac', target_percentage=1.0)
        sec = Security('sec', 1, 100.0)
        ac1.add_security(sec)
        ac2.add_security(sec)
        self.assertEqual(ac1, ac2)

    def test_add_value(self):
        ac = AssetClass('ac', target_percentage=1.0)
        ac.add_value(100.0)
        self.assertEqual(ac.value, 100.0)

    def test_add_security_new(self):
        ac = AssetClass('ac', target_percentage=1.0)
        ac.add_security(Security('sec'))
        self.assertEqual(ac.securities['sec'], Security('sec'))

    def test_add_security_update(self):
        ac = AssetClass('ac', target_percentage=1.0)
        ac.add_security(Security('sec', 'old_name', 25.0))
        ac.add_security(Security('sec', 'sec_name', 15.0))
        self.assertEqual(ac.securities['sec'].name, 'sec_name')
        self.assertEqual(ac.securities['sec'].price, 15.0)

    def test_contains_security_false(self):
        ac = AssetClass('ac', target_percentage=1.0)
        self.assertFalse(ac.contains_security('sec'))

    def test_contains_security_true(self):
        ac = AssetClass('ac', target_percentage=1.0)
        ac.add_security(Security('sec'))
        self.assertTrue(ac.contains_security('sec'))

    def test_get_security(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec = Security('sec')
        ac.add_security(sec)
        self.assertEqual(ac.get_security('sec'), sec)

    def test_add_holding_new(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec = Security('sec', price=5.0)
        ac.add_holding(sec, 3)
        self.assertEqual(ac.holdings[sec.id], Holding('sec', 3, 15.0))
        self.assertEqual(ac.value, 15.0)

    def test_add_holding_update(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec1 = Security('sec', price=5.0)
        ac.add_holding(sec1, 3)
        sec2 = Security('sec', price=10.0)
        ac.add_holding(sec2, 3)
        self.assertEqual(ac.holdings['sec'], Holding('sec', 6, 45.0))
        self.assertEqual(ac.value, 45.0)

    def test_contains_holding_false(self):
        ac = AssetClass('ac', target_percentage=1.0)
        self.assertFalse(ac.contains_holding('sec'))

    def test_contains_holding_true(self):
        ac = AssetClass('ac', target_percentage=1.0)
        ac.add_holding(Security('sec', 'sec_name', 15.0), 3)
        self.assertTrue(ac.contains_holding('sec'))

    def test_get_holding(self):
        ac = AssetClass('ac', target_percentage=1.0)
        ac.add_holding(Security('sec', 'sec_name', 15.0), 3)
        self.assertEqual(ac.get_holding('sec'), Holding('sec', 3, 45.0))

    def test_update(self):
        ac = AssetClass('ac', target_percentage=0.5)
        sec = Security('sec')
        ac.add_security(sec)
        rh = RobinhoodHolding(
            holding_id='sec',
            name='sec_name',
            price=40.0,
            quantity=1,
            average_buy_price=40.0,
            equity=40.0,
            percentage=40.0,
            percent_change=0.0,
            equity_change=0.0,
            holding_type='etp'
        )
        ac.update(rh)
        hol = Holding('sec', 1, 40.0)
        self.assertEqual(ac.value, rh.equity)
        self.assertEqual(ac.securities['sec'], sec)
        self.assertEqual(ac.holdings['sec'], hol)

    def test_plan_deposit_1(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec1 = Security('sec1', 'sec1_name', 33.0)
        sec2 = Security('sec2', 'sec2_name', 49.0)
        ac.add_security(sec1)
        ac.add_security(sec2)
        purchases = ac.plan_deposit(100)
        p1 = Purchase('sec1', 'sec1_name', 3, 33.0)
        p2 = Purchase('sec2', 'sec2_name', 0, 49.0)
        self.assertEqual(purchases['sec1'], p1)
        self.assertEqual(purchases['sec2'], p2)

    def test_plan_deposit_2(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec1 = Security('sec1', 'sec1_name', 33.0)
        sec2 = Security('sec2', 'sec2_name', 49.0)
        ac.add_security(sec1)
        ac.add_security(sec2)
        purchases = ac.plan_deposit(98.5)
        p1 = Purchase('sec1', 'sec1_name', 0, 33.0)
        p2 = Purchase('sec2', 'sec2_name', 2, 49.0)
        self.assertEqual(purchases['sec1'], p1)
        self.assertEqual(purchases['sec2'], p2)


if __name__ == '__main__':
    unittest.main()
