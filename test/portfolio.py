# Ricky Galliani
# Hanna
# test/portfolio.py

from src.asset_class import AssetClass
from src.deposit import Deposit
from src.portfolio import Portfolio
from src.purchase import Purchase
from src.robinhood_holding import RobinhoodHolding
from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.portfolio


class PortfolioTest(unittest.TestCase):

    def test_inequality(self):
        p1 = Portfolio()
        p2 = Portfolio()
        p2.add_asset_class(AssetClass('ac', 1.0))
        self.assertNotEqual(p1, p2)

    def test_equality(self):
        p1 = Portfolio()
        p1.add_asset_class(AssetClass('ac', 1.0))
        p2 = Portfolio()
        p2.add_asset_class(AssetClass('ac', 1.0))
        self.assertEqual(p1, p2)

    def test_get_asset_class(self):
        p = Portfolio()
        ac = AssetClass('ac', 1.0)
        sec = Security('sec', 'sec_name', 10.0)
        ac.add_security(sec)
        ac.add_holding(sec, 3)
        p.add_asset_class(ac)
        self.assertEqual(p.value, 30.0)
        self.assertTrue('ac' in p.asset_classes)

    def test_contains_security_false(self):
        p = Portfolio()
        self.assertFalse(p.contains_security('sec'))

    def test_contains_security_true(self):
        p = Portfolio()
        ac = AssetClass('ac', 1.0)
        p.add_asset_class(ac)
        sec = Security('sec', 'sec_name', 10.0)
        ac.add_security(sec)
        self.assertTrue(p.contains_security('sec'))

    def test_get_asset_class_for_security(self):
        p = Portfolio()
        ac = AssetClass('ac', 1.0)
        p.add_asset_class(ac)
        sec = Security('sec', 'sec_name', 10.0)
        ac.add_security(sec)
        self.assertEqual(p.get_asset_class_for_security('sec'), ac)

    def test_get_asset_class_percentage(self):
        p = Portfolio()
        sec = Security('sec', 'sec_name', 10.0)
        ac1 = AssetClass('ac1', 0.2)
        ac1.add_security(sec)
        ac1.add_holding(sec, 2)
        ac2 = AssetClass('ac2', 0.8)
        ac2.add_security(sec)
        ac2.add_holding(sec, 8)
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        self.assertEqual(p.get_asset_class_percentage('ac1'), 0.2)
        self.assertEqual(p.get_asset_class_percentage('ac2'), 0.8)

    def test_get_security_percentage(self):
        p = Portfolio()
        sec = Security('sec', 'sec_name', 10.0)
        ac = AssetClass('ac', 0.2)
        ac.add_security(sec)
        ac.add_holding(sec, 2)
        p.add_asset_class(ac)
        self.assertEqual(p.get_security_percentage('sec'), 1.0)

    def test_get_asset_class_target_value(self):
        p = Portfolio()
        sec = Security('sec', 'sec_name', 10.0)
        ac1 = AssetClass('ac1', 0.2)
        ac1.add_security(sec)
        ac1.add_holding(sec, 2)
        ac2 = AssetClass('ac2', 0.8)
        ac2.add_security(sec)
        ac2.add_holding(sec, 8)
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        self.assertEqual(p.get_asset_class_target_value('ac1'), 20.0)
        self.assertEqual(p.get_asset_class_target_value('ac2'), 80.0)

    def test_get_asset_class_target_deviation(self):
        p = Portfolio()
        sec = Security('sec', 'sec_name', 10.0)
        ac1 = AssetClass('ac1', 0.15)
        ac1.add_security(sec)
        ac1.add_holding(sec, 2)
        ac2 = AssetClass('ac2', 0.85)
        ac2.add_security(sec)
        ac2.add_holding(sec, 8)
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        self.assertEqual(p.get_asset_class_target_deviation('ac1'), 5.0)
        self.assertEqual(p.get_asset_class_target_deviation('ac2'), -5.0)

    def test_get_asset_class_budgets(self):
        p = Portfolio()
        sec = Security('sec', 'sec_name', 10.0)
        ac1 = AssetClass('ac1', 0.15)
        ac1.add_security(sec)
        ac1.add_holding(sec, 2)
        ac2 = AssetClass('ac2', 0.85)
        ac2.add_security(sec)
        ac2.add_holding(sec, 8)
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        budgets = p.get_asset_class_budgets(100.0)
        self.assertEqual(budgets['ac1'], 10.0)
        self.assertEqual(budgets['ac2'], 90.0)

    def test_update(self):
        p = Portfolio()
        sec1 = Security('sec1', 'sec_name', 10.0)
        sec2 = Security('sec2', 'sec_name', 20.0)
        ac1 = AssetClass('ac1', 0.4)
        ac1.add_security(sec1)
        ac2 = AssetClass('ac2', 0.6)
        ac2.add_security(sec2)
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        rh1 = RobinhoodHolding(
            holding_id='sec1',
            name='sec1_name',
            price=10.0,
            quantity=1,
            average_buy_price=10.0,
            equity=10.0,
            percentage=0.33,
            percent_change=0.0,
            equity_change=0.0,
            holding_type='etp'
        )
        rh2 = RobinhoodHolding(
            holding_id='sec2',
            name='sec2_name',
            price=20.0,
            quantity=1,
            average_buy_price=20.0,
            equity=20.0,
            percentage=0.66,
            percent_change=0.0,
            equity_change=0.0,
            holding_type='etp'
        )
        p.update([rh1, rh2])
        self.assertEqual(p.value, 30.0)

    def test_plan_deposit(self):
        p = Portfolio()
        sec1 = Security('sec1', 'sec1_name', 10.0)
        sec2 = Security('sec2', 'sec2_name', 20.0)
        ac1 = AssetClass('ac1', 0.4)
        ac1.add_security(sec1)
        ac1.add_holding(sec1, 3)
        ac2 = AssetClass('ac2', 0.6)
        ac2.add_security(sec2)
        ac2.add_holding(sec2, 2)
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        deposit = p.plan_deposit(30.0)
        p1 = [Purchase('sec1', 'sec1_name', 1, 10.0)]
        p2 = [Purchase('sec2', 'sec2_name', 1, 20.0)]
        self.assertEqual(deposit.total, 30.0)
        self.assertEqual(deposit.purchases['ac1'], p1)
        self.assertEqual(deposit.purchases['ac2'], p2)

    def test_make_deposit(self):
        p = Portfolio()
        sec = Security('sec', 'sec_name', 10.0)
        ac = AssetClass('ac', 1.0)
        ac.add_security(sec)
        p.add_asset_class(ac)
        d = Deposit()
        d.add_purchase('ac', Purchase('sec', 'sec_name', 1, 10.0))
        p.make_deposit(d)
        self.assertEqual(p.value, 10.0)


if __name__ == '__main__':
    unittest.main()
