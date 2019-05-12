# Ricky Galliani
# Hanna
# test/asset_class.py

from src.asset_class import AssetClass
from src.purchase import Purchase
from src.robinhood_holding import RobinhoodHolding
from src.security import Security

import unittest

# Usage: python -m unittest --verbose test.asset_class

class AssetClassTest(unittest.TestCase):

    def test_inequality(self):
        ac1 = AssetClass('ac', target_percentage=1.0)
        ac2 = AssetClass('ac', target_percentage=1.0)
        ac2.add_security(Security('sec'))
        self.assertNotEqual(ac1, ac2)

    def test_equality(self):
        ac1 = AssetClass('ac', target_percentage=1.0)
        ac2 = AssetClass('ac', target_percentage=1.0)
        sec = Security('sec', 'sec_name', 100.0, 1, 100.0)    
        ac1.add_security(sec)
        ac2.add_security(sec)
        self.assertEqual(ac1, ac2)

    def test_add_security_without_holdings(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec = Security('sec')
        ac.add_security(sec)
        self.assertEqual(ac.securities[sec.id], sec)
        self.assertEqual(ac.holdings, 0.0)

    def test_add_security_with_holdings(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec = Security('sec', price=10.0, quantity=3, holdings=30.0)
        ac.add_security(sec)
        self.assertEqual(ac.securities[sec.id], sec)
        self.assertEqual(ac.holdings, 30.0)

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
        self.assertEqual(ac.holdings, rh.equity)
        self.assertEqual(ac.securities['sec'], sec)

    def test_plan_deposit_1(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec1 = Security('sec1', 'sec1_name', 33.0, 1, 33.0)
        sec2 = Security('sec2', 'sec2_name', 49.0, 1, 49.0)
        ac.add_security(sec1)
        ac.add_security(sec2)
        purchases = ac.plan_deposit(100)
        p1 = Purchase('sec1', 'sec1_name', 33.0, 3)
        p2 = Purchase('sec2', 'sec2_name', 49.0, 0)
        self.assertEqual(purchases[0], p1)
        self.assertEqual(purchases[1], p2)

    def test_plan_deposit_2(self):
        ac = AssetClass('ac', target_percentage=1.0)
        sec1 = Security('sec1', 'sec1_name', 33.0, 1, 33.0)
        sec2 = Security('sec2', 'sec2_name', 49.0, 1, 49.0)
        ac.add_security(sec1)
        ac.add_security(sec2)
        purchases = ac.plan_deposit(98.5)
        p1 = Purchase('sec1', 'sec1_name', 33.0, 0)
        p2 = Purchase('sec2', 'sec2_name', 49.0, 2)
        self.assertEqual(purchases[0], p1)
        self.assertEqual(purchases[1], p2)

if __name__ == '__main__':
    unittest.main()