# Ricky Galliani
# Hanna
# test/portfolio.py

from src.asset_class import AssetClass
from src.deposit import Deposit
from src.holding import Holding
from src.portfolio import Portfolio
from src.purchase import Purchase
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

    def test_get_all_security_symbols(self):
        p = Portfolio()
        ac = AssetClass('ac', 1.0)
        sec1 = Security('sec1', 'SEC1', 'sec1_name', 10.0)
        sec2 = Security('sec2', 'SEC2', 'sec2_name', 15.0)
        ac.add_security(sec1)
        ac.add_security(sec2)
        p.add_asset_class(ac)
        true_symbols = sorted(p.get_all_security_symbols())
        self.assertEqual(true_symbols, ['SEC1', 'SEC2'])

    def test_contains_asset_class_false(self):
        p = Portfolio()
        self.assertFalse(p.contains_asset_class('ac'))

    def test_contains_asset_class_true(self):
        p = Portfolio()
        p.add_asset_class(AssetClass('ac', 1.0))
        self.assertTrue(p.contains_asset_class('ac'))

    def test_get_asset_class_names(self):
        p = Portfolio()
        ac = AssetClass('ac', 1.0)
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        ac.add_security(sec)
        p.add_asset_class(ac)
        self.assertTrue('ac' in p.get_asset_class_names())

    def test_contains_security_false(self):
        p = Portfolio()
        self.assertFalse(p.contains_security('sec'))

    def test_contains_security_true(self):
        p = Portfolio()
        ac = AssetClass('ac', 1.0)
        p.add_asset_class(ac)
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        ac.add_security(sec)
        self.assertTrue(p.contains_security('sec'))

    def test_get_asset_class_for_security(self):
        p = Portfolio()
        ac = AssetClass('ac', 1.0)
        p.add_asset_class(ac)
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        ac.add_security(sec)
        self.assertEqual(p.get_asset_class_for_security('sec'), ac)

    def test_get_asset_class_value(self):
        p = Portfolio()
        ac = AssetClass('ac', 1.0)
        p.add_asset_class(ac)
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        ac.add_security(sec)
        holding = Holding(sec, 3, 30.0)
        ac.add_holding(holding)
        self.assertEqual(p.get_asset_class_value('ac'), 30.0)

    def test_get_asset_class_percentage(self):
        p = Portfolio()
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        ac1 = AssetClass('ac1', 0.2)
        ac1.add_security(sec)
        ac1.add_holding(Holding(sec, 2, 20.0))
        ac2 = AssetClass('ac2', 0.8)
        ac2.add_security(sec)
        ac2.add_holding(Holding(sec, 8, 80.0))
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        self.assertEqual(p.get_asset_class_percentage('ac1'), 0.2)
        self.assertEqual(p.get_asset_class_percentage('ac2'), 0.8)

    def test_get_security_value(self):
        p = Portfolio()
        ac = AssetClass('ac', 1.0)
        p.add_asset_class(ac)
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        ac.add_security(sec)
        holding = Holding(sec, 3, 30.0)
        ac.add_holding(holding)
        self.assertEqual(p.get_security_value('sec'), 30.0)

    def test_get_security_percentage(self):
        p = Portfolio()
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        ac = AssetClass('ac', 0.2)
        ac.add_security(sec)
        ac.add_holding(Holding(sec, 2, 20.0))
        p.add_asset_class(ac)
        self.assertEqual(p.get_security_percentage('sec'), 1.0)

    def test_get_asset_class_target_value(self):
        p = Portfolio()
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        ac1 = AssetClass('ac1', 0.2)
        ac1.add_security(sec)
        ac1.add_holding(Holding(sec, 2, 20.0))
        ac2 = AssetClass('ac2', 0.8)
        ac2.add_security(sec)
        ac2.add_holding(Holding(sec, 8, 80.0))
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        self.assertEqual(p.get_asset_class_target_value('ac1'), 20.0)
        self.assertEqual(p.get_asset_class_target_value('ac2'), 80.0)

    def test_get_asset_class_target_deviation(self):
        p = Portfolio()
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        ac1 = AssetClass('ac1', 0.15)
        ac1.add_security(sec)
        ac1.add_holding(Holding(sec, 2, 20.0))
        ac2 = AssetClass('ac2', 0.85)
        ac2.add_security(sec)
        ac2.add_holding(Holding(sec, 8, 80.0))
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        self.assertEqual(p.get_asset_class_target_deviation('ac1'), 5.0)
        self.assertEqual(p.get_asset_class_target_deviation('ac2'), -5.0)

    def test_get_asset_class_budgets(self):
        p = Portfolio()
        sec = Security('sec', 'SEC', 'sec_name', 10.0)
        ac1 = AssetClass('ac1', 0.15)
        ac1.add_security(sec)
        ac1.add_holding(Holding(sec, 2, 20.0))
        ac2 = AssetClass('ac2', 0.85)
        ac2.add_security(sec)
        ac2.add_holding(Holding(sec, 8, 80.0))
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        budgets = p.get_asset_class_budgets(100.0)
        self.assertEqual(budgets['ac1'], 10.0)
        self.assertEqual(budgets['ac2'], 90.0)

    def test_update(self):
        p = Portfolio()
        sec1 = Security('sec1', 'SEC1', 'sec_name', 10.0)
        sec2 = Security('sec2', 'SEC2', 'sec_name', 20.0)
        ac1 = AssetClass('ac1', 0.4)
        ac1.add_security(sec1)
        ac2 = AssetClass('ac2', 0.6)
        ac2.add_security(sec2)
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        account_profile = {
            "margin_balances": {
                "unallocated_margin_cash": 78.6800,
            }
        }
        security_info = {
            "SEC1": {"name": "sec1_name", "price": 10.0},
            "SEC2": {"name": "sec2_name", "price": 20.0}
        }
        holding_info = {
            'sec1': {
                'id': 'sec1',
                'name': 'sec1_name',
                'price': 10.0,
                'quantity': 1,
                'average_buy_price': 10.0,
                'equity': 10.0,
                'percentage': 0.33,
                'percent_change': 0.0,
                'equity_change': 0.0,
                'holding_type': 'etp'
            },
            'sec2': {
                'id': 'sec2',
                'name': 'sec2_name',
                'price': 20.0,
                'quantity': 1,
                'average_buy_price': 20.0,
                'equity': 20.0,
                'percentage': 0.66,
                'percent_change': 0.0,
                'equity_change': 0.0,
                'holding_type': 'etp'        
            }
        }
        p.update(account_profile, security_info, holding_info)
        self.assertEqual(p.get_cash(), 78.68)
        self.assertEqual(p.get_value(), 30.0)
        self.assertEqual(p.get_num_shares(), 2)

    def test_plan_deposit(self):
        p = Portfolio()
        sec1 = Security('sec1', 'SEC1', 'sec1_name', 10.0, False)
        sec2 = Security('sec2', 'SEC2', 'sec2_name', 20.0, False)
        ac1 = AssetClass('ac1', 0.4)
        ac1.add_security(sec1)
        ac1.add_holding(Holding(sec1, 3, 30.0))
        ac2 = AssetClass('ac2', 0.6)
        ac2.add_security(sec2)
        ac2.add_holding(Holding(sec2, 2, 40.0))
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        deposit = p.plan_deposit(30.0)
        p1 = [Purchase(sec1, 1)]
        p2 = [Purchase(sec2, 1)]
        self.assertEqual(deposit.get_total(), 30.0)
        self.assertEqual(deposit.get_purchases_for_asset_class('ac1'), p1)
        self.assertEqual(deposit.get_purchases_for_asset_class('ac2'), p2)

    def test_make_deposit(self):
        p = Portfolio()
        sec = Security('sec', 'SEC', 'sec_name', 10.0, False)
        ac = AssetClass('ac', 1.0)
        ac.add_security(sec)
        p.add_asset_class(ac)
        d = Deposit()
        d.add_purchase('ac', Purchase(sec, 1))
        p.make_deposit(d)
        self.assertEqual(p.get_value(), 10.0)
        self.assertEqual(p.get_num_shares(), 1)


if __name__ == '__main__':
    unittest.main()
