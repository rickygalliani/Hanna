# Ricky Galliani
# Hanna
# test/portfolio.py

from src.asset_class import AssetClass
from src.api import AccountProfile, DividendInfo, HoldingInfo, SecurityInfo
from src.deposit import Deposit
from src.holding import Holding
from src.portfolio import Portfolio
from src.purchase import Purchase
from src.security import Security

import unittest

# Usage: python3 -m unittest --verbose test.portfolio


class PortfolioTest(unittest.TestCase):
    def test_add_asset_class(self):
        p: Portfolio = Portfolio()
        ac: AssetClass = AssetClass("ac", 1.0)
        sec: Security = Security("sec", "SEC", price=10.0)
        ac.add_security(sec)
        ac.buy(sec, 5, True)
        p.add_asset_class(ac)
        self.assertEqual(p.get_value(), 50.0)
        self.assertTrue(ac.get_name() in p.get_asset_class_names())
        self.assertTrue(ac in p.get_asset_classes())

    def test_inequality(self):
        p1: Portfolio = Portfolio()
        p2: Portfolio = Portfolio()
        p2.add_asset_class(AssetClass("ac", 1.0))
        self.assertNotEqual(p1, p2)

    def test_equality(self):
        p1: Portfolio = Portfolio()
        p1.add_asset_class(AssetClass("ac", 1.0))
        p2: Portfolio = Portfolio()
        p2.add_asset_class(AssetClass("ac", 1.0))
        self.assertEqual(p1, p2)

    def test_load_configuration_basic(self):
        portfolio_config = [
            {
                "name": "Asset Class 1",
                "target_percentage": 0.5,
                "securities": ["sec1id"],
                "buy_restrictions": [],
            },
            {
                "name": "Asset Class 2",
                "target_percentage": 0.5,
                "securities": ["sec2id", "sec3id"],
                "buy_restrictions": ["sec3id"],
            },
        ]
        p_load: Portfolio = Portfolio()
        p_load.load_configuration(portfolio_config)
        p_test: Portfolio = Portfolio()
        sec1: Security = Security("sec1id", buy_restricted=0)
        sec2: Security = Security("sec2id", buy_restricted=0)
        sec3: Security = Security("sec3id")
        ac1: AssetClass = AssetClass("Asset Class 1", 0.5)
        ac2: AssetClass = AssetClass("Asset Class 2", 0.5)
        ac_other: AssetClass = AssetClass("Other", 0.0)
        ac1.add_security(sec1)
        ac2.add_security(sec2)
        ac2.add_security(sec3)
        p_test.add_asset_class(ac1)
        p_test.add_asset_class(ac2)
        p_test.add_asset_class(ac_other)
        self.assertEqual(p_load, p_test)

    def test_load_configuration_idempotent(self):
        portfolio_config = [
            {
                "name": "Asset Class 1",
                "target_percentage": 0.5,
                "securities": ["sec1id"],
                "buy_restrictions": [],
            },
            {
                "name": "Asset Class 2",
                "target_percentage": 0.5,
                "securities": ["sec2id", "sec3id"],
                "buy_restrictions": ["sec3id"],
            },
        ]
        p_load: Portfolio = Portfolio()
        p_load.load_configuration(portfolio_config)
        p_load.load_configuration(portfolio_config)
        p_test: Portfolio = Portfolio()
        sec1: Security = Security("sec1id", buy_restricted=0)
        sec2: Security = Security("sec2id", buy_restricted=0)
        sec3: Security = Security("sec3id")
        ac1: AssetClass = AssetClass("Asset Class 1", 0.5)
        ac2: AssetClass = AssetClass("Asset Class 2", 0.5)
        ac_other: AssetClass = AssetClass("Other", 0.0)
        ac1.add_security(sec1)
        ac2.add_security(sec2)
        ac2.add_security(sec3)
        p_test.add_asset_class(ac1)
        p_test.add_asset_class(ac2)
        p_test.add_asset_class(ac_other)
        self.assertEqual(p_load, p_test)

    def test_load_configuration_add(self):
        old_portfolio_config = [
            {
                "name": "Asset Class 1",
                "target_percentage": 0.5,
                "securities": {"SEC1": "sec1id"},
                "buy_restrictions": [],
            },
            {
                "name": "Asset Class 2",
                "target_percentage": 0.5,
                "securities": {"SEC2": "sec2id", "SEC3": "sec3id"},
                "buy_restrictions": ["SEC3"],
            },
        ]
        new_portfolio_config = [
            {
                "name": "Asset Class 1",
                "target_percentage": 0.33,
                "securities": {"SEC1": "sec1id", "SEC4": "sec4id"},
                "buy_restrictions": ["SEC1"],
            },
            {
                "name": "Asset Class 2",
                "target_percentage": 0.33,
                "securities": {"SEC2": "sec2id", "SEC3": "sec3id"},
                "buy_restrictions": ["SEC3"],
            },
            {
                "name": "Asset Class 2",
                "target_percentage": 0.34,
                "securities": {"SEC5": "sec5id", "SEC6": "sec6id"},
                "buy_restrictions": [],
            },
        ]
        p_load: Portfolio = Portfolio()
        p_load.load_configuration(old_portfolio_config)
        p_load.load_configuration(new_portfolio_config)
        p_test: Portfolio = Portfolio()
        p_test.load_configuration(new_portfolio_config)
        self.assertEqual(p_load, p_test)

    def test_get_all_security_symbols(self):
        p: Portfolio = Portfolio()
        ac: AssetClass = AssetClass("ac", 1.0)
        sec1: Security = Security("sec1", symbol="SEC1", price=10.0)
        sec2: Security = Security("sec2", symbol="SEC2", price=15.0)
        ac.add_security(sec1)
        ac.add_security(sec2)
        ac.buy(sec1, 1, True)
        ac.buy(sec2, 1, True)
        p.add_asset_class(ac)
        symbols = sorted(p.get_all_security_symbols())
        self.assertEqual(symbols, ["SEC1", "SEC2"])

    def test_get_cost(self):
        p: Portfolio = Portfolio()
        ac: AssetClass = AssetClass("ac", 1.0)
        sec: Security = Security("sec", "SEC", price=10.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        p.add_asset_class(ac)
        self.assertEqual(p.get_cost(), 30.0)

    def get_dividends(self):
        p: Portfolio = Portfolio()
        ac1: AssetClass = AssetClass("ac1", 0.5)
        sec1: Security = Security("sec1", "SEC1", price=10.0)
        ac1.add_security(sec1)
        ac1.buy(sec1, 3, True)
        p.add_asset_class(ac1)
        hol1: Holding = ac1.get_holding("sec1")
        hol1.set_dividends(10.0)
        ac2: AssetClass = AssetClass("ac2", 0.5)
        sec2: Security = Security("sec2", "SEC2", price=10.0)
        ac2.add_security(sec2)
        ac2.buy(sec2, 3, True)
        p.add_asset_class(ac2)
        hol2: Holding = ac2.get_holding("sec2")
        hol2.set_dividends(5.0)
        self.assertEqual(p.get_dividends(), 15.0)

    def test_get_return(self):
        p: Portfolio = Portfolio()
        ac: AssetClass = AssetClass("ac", 1.0)
        sec: Security = Security("sec", "SEC", price=10.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        p.add_asset_class(ac)
        sec.set_price(11.0)
        self.assertEqual(p.get_return(), 0.1)

    def test_contains_asset_class_false(self):
        p: Portfolio = Portfolio()
        self.assertFalse(p.contains_asset_class("ac"))

    def test_contains_asset_class_true(self):
        p: Portfolio = Portfolio()
        p.add_asset_class(AssetClass("ac", 1.0))
        self.assertTrue(p.contains_asset_class("ac"))

    def test_get_asset_class_names(self):
        p: Portfolio = Portfolio()
        ac: AssetClass = AssetClass("ac", 1.0)
        sec: Security = Security("sec", "SEC", price=10.0)
        ac.add_security(sec)
        p.add_asset_class(ac)
        self.assertTrue("ac" in p.get_asset_class_names())

    def test_contains_security_false(self):
        p: Portfolio = Portfolio()
        self.assertFalse(p.contains_security("sec"))

    def test_contains_security_true(self):
        p: Portfolio = Portfolio()
        ac: AssetClass = AssetClass("ac", 1.0)
        p.add_asset_class(ac)
        sec: Security = Security("sec", "SEC", price=10.0)
        ac.add_security(sec)
        self.assertTrue(p.contains_security("sec"))

    def test_get_asset_class_for_security(self):
        p: Portfolio = Portfolio()
        ac: AssetClass = AssetClass("ac", 1.0)
        p.add_asset_class(ac)
        sec: Security = Security("sec", "SEC", price=10.0)
        ac.add_security(sec)
        self.assertEqual(p.get_asset_class_for_security("sec"), ac)

    def test_get_asset_class_value(self):
        p: Portfolio = Portfolio()
        ac: AssetClass = AssetClass("ac", 1.0)
        p.add_asset_class(ac)
        sec: Security = Security("sec", "SEC", price=10.0)
        ac.add_security(sec)
        holding: Holding = Holding(sec, 3, 10.0)
        ac.add_holding(holding)
        self.assertEqual(p.get_asset_class_value("ac"), 30.0)

    def test_get_asset_class_percentage(self):
        p: Portfolio = Portfolio()
        sec: Security = Security("sec", "SEC", price=10.0)
        ac1: AssetClass = AssetClass("ac1", 0.2)
        ac1.add_security(sec)
        ac1.add_holding(Holding(sec, 2, 10.0))
        ac2: AssetClass = AssetClass("ac2", 0.8)
        ac2.add_security(sec)
        ac2.add_holding(Holding(sec, 8, 10.0))
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        self.assertEqual(p.get_asset_class_percentage("ac1"), 0.2)
        self.assertEqual(p.get_asset_class_percentage("ac2"), 0.8)

    def test_get_security_value(self):
        p: Portfolio = Portfolio()
        ac: AssetClass = AssetClass("ac", 1.0)
        p.add_asset_class(ac)
        sec: Security = Security("sec", "SEC", price=10.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        self.assertEqual(p.get_security_value("sec"), 30.0)

    def test_get_security_percentage(self):
        p: Portfolio = Portfolio()
        sec: Security = Security("sec", "SEC", price=10.0)
        ac: AssetClass = AssetClass("ac", 0.2)
        ac.add_security(sec)
        ac.add_holding(Holding(sec, 2, 10.0))
        p.add_asset_class(ac)
        self.assertEqual(p.get_security_percentage("sec"), 1.0)

    def test_get_asset_class_target_value(self):
        p: Portfolio = Portfolio()
        sec: Security = Security("sec", "SEC", price=10.0)
        ac1: AssetClass = AssetClass("ac1", 0.2)
        ac1.add_security(sec)
        ac1.add_holding(Holding(sec, 2, 10.0))
        ac2: AssetClass = AssetClass("ac2", 0.8)
        ac2.add_security(sec)
        ac2.add_holding(Holding(sec, 8, 10.0))
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        value = p.get_value()
        self.assertEqual(p.get_asset_class_target_value("ac1", value), 20.0)
        self.assertEqual(p.get_asset_class_target_value("ac2", value), 80.0)

    def test_get_asset_class_target_deviation(self):
        p: Portfolio = Portfolio()
        sec: Security = Security("sec", "SEC", price=10.0)
        ac1: AssetClass = AssetClass("ac1", 0.15)
        ac1.add_security(sec)
        ac1.add_holding(Holding(sec, 2, 10.0))
        ac2: AssetClass = AssetClass("ac2", 0.85)
        ac2.add_security(sec)
        ac2.add_holding(Holding(sec, 8, 10.0))
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        value = p.get_value()
        self.assertEqual(p.get_asset_class_target_deviation("ac1", value), 5.0)
        self.assertEqual(
            p.get_asset_class_target_deviation("ac2", value), -5.0
        )

    def test_get_asset_class_budgets(self):
        p: Portfolio = Portfolio()
        sec: Security = Security("sec", "SEC", price=10.0)
        ac1: AssetClass = AssetClass("ac1", 0.15)
        ac1.add_security(sec)
        ac1.add_holding(Holding(sec, 2, 10.0))
        ac2: AssetClass = AssetClass("ac2", 0.85)
        ac2.add_security(sec)
        ac2.add_holding(Holding(sec, 8, 10.0))
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        budgets = p.get_asset_class_budgets(100.0)
        self.assertEqual(budgets["ac1"], 10.0)
        self.assertEqual(budgets["ac2"], 90.0)

    def test_update_basic(self):
        p: Portfolio = Portfolio()
        sec1: Security = Security("sec1", "SEC1", name="sec_name", price=10.0)
        sec2: Security = Security("sec2", "SEC2", name="sec_name", price=20.0)
        ac1: AssetClass = AssetClass("ac1", 0.4)
        ac1.add_security(sec1)
        ac2: AssetClass = AssetClass("ac2", 0.6)
        ac2.add_security(sec2)
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        account_profile = AccountProfile(78.68)
        security_info = {
            "sec1": SecurityInfo("SEC1", "sec1_name", 10.0),
            "sec2": SecurityInfo("SEC2", "sec2_name", 20.0),
        }
        holding_info = {
            "sec1": HoldingInfo(
                "sec1", "sec1_name", 10.0, 1, 10.0, 10.0, 0.33, 0.0, 0.0
            ),
            "sec2": HoldingInfo(
                "sec2", "sec2_name", 20.0, 1, 20.0, 20.0, 0.66, 0.0, 0.0
            ),
        }
        dividend_info = {
            "sec1": DividendInfo("sec1", 10.0),
            "sec2": DividendInfo("sec2", 5.0),
        }
        p.update(account_profile, security_info, holding_info, dividend_info)
        self.assertEqual(p.get_cash(), 78.68)
        self.assertEqual(p.get_value(), 108.68)
        self.assertEqual(p.get_num_shares(), 2)
        self.assertEqual(p.get_dividends(), 15.0)

    def test_update_idempotent(self):
        p: Portfolio = Portfolio()
        sec1: Security = Security("sec1", "SEC1", name="sec_name", price=10.0)
        ac1: AssetClass = AssetClass("ac1", 0.4)
        ac1.add_security(sec1)
        p.add_asset_class(ac1)
        account_profile = AccountProfile(78.68)
        security_info = {"sec1": SecurityInfo("SEC1", "sec1_name", 10.0)}
        holding_info = {
            "sec1": HoldingInfo(
                "sec1", "sec1_name", 10.0, 3, 10.0, 30.0, 0.33, 0.0, 0.0
            )
        }
        dividend_info = {"sec1": DividendInfo("sec1", 1.0)}
        p.update(account_profile, security_info, holding_info, dividend_info)
        self.assertEqual(p.get_cash(), 78.68)
        self.assertEqual(p.get_value(), 108.68)
        self.assertEqual(p.get_num_shares(), 3)
        self.assertEqual(p.get_dividends(), 1.0)
        p.update(account_profile, security_info, holding_info, dividend_info)
        self.assertEqual(p.get_cash(), 78.68)
        self.assertEqual(p.get_value(), 108.68)
        self.assertEqual(p.get_num_shares(), 3)
        self.assertEqual(p.get_dividends(), 1.0)

    def test_plan_deposit_restrict_budget(self):
        p: Portfolio = Portfolio()
        sec: Security = Security("sec1", "SEC1", "sec1_name", 10.0, False)
        ac: AssetClass = AssetClass("ac", 0.4)
        ac.add_security(sec)
        p.add_asset_class(ac)
        p.set_cash(39.5)
        deposit: Deposit = p.plan_deposit(100.0)
        p = [Purchase(sec, 3)]
        self.assertEqual(deposit.get_total(), 30.0)
        self.assertEqual(deposit.get_purchases_for_asset_class("ac"), p)

    def test_plan_deposit(self):
        p: Portfolio = Portfolio()
        sec1: Security = Security("sec1", "SEC1", "sec1_name", 10.0, False)
        sec2: Security = Security("sec2", "SEC2", "sec2_name", 20.0, False)
        ac1: AssetClass = AssetClass("ac1", 0.4)
        ac2: AssetClass = AssetClass("ac2", 0.6)
        ac1.add_security(sec1)
        ac2.add_security(sec2)
        ac1.add_holding(Holding(sec1, 3, 10.0))
        ac2.add_holding(Holding(sec2, 2, 20.0))
        p.add_asset_class(ac1)
        p.add_asset_class(ac2)
        p.set_cash(35.0)
        deposit: Deposit = p.plan_deposit(35.0)
        p1 = [Purchase(sec1, 1)]
        p2 = [Purchase(sec2, 1)]
        self.assertEqual(deposit.get_total(), 30.0)
        self.assertEqual(deposit.get_purchases_for_asset_class("ac1"), p1)
        self.assertEqual(deposit.get_purchases_for_asset_class("ac2"), p2)

    def test_make_deposit(self):
        p: Portfolio = Portfolio()
        sec: Security = Security("sec", "SEC", "sec_name", 10.0, False)
        ac: AssetClass = AssetClass("ac", 1.0)
        ac.add_security(sec)
        p.add_asset_class(ac)
        p.set_cash(24.0)
        d1: Deposit = Deposit()
        d1.add_purchase("ac", Purchase(sec, 1))
        p.make_deposit(d1, True)
        d2: Deposit = Deposit()
        d2.add_purchase("ac", Purchase(sec, 1))
        p.make_deposit(d2, True)
        self.assertEqual(p.get_value(), 24.0)
        self.assertEqual(p.get_num_shares(), 2)


if __name__ == "__main__":
    unittest.main()
