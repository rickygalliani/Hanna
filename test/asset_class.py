# Ricky Galliani
# Hanna
# test/asset_class.py

from src.asset_class import AssetClass
from src.holding import Holding
from src.purchase import Purchase
from src.security import Security

from typing import List

import unittest

# Usage: python3 -m unittest --verbose test.asset_class


class AssetClassTest(unittest.TestCase):
    def test_inequality(self) -> None:
        ac1: AssetClass = AssetClass("ac", target_percentage=1.0)
        ac2: AssetClass = AssetClass("ac", target_percentage=1.0)
        ac2.add_security(Security("sec", "SEC"))
        self.assertNotEqual(ac1, ac2)

    def test_equality(self):
        ac1: AssetClass = AssetClass("ac", target_percentage=1.0)
        ac2: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC")
        ac1.add_security(sec)
        ac2.add_security(sec)
        self.assertEqual(ac1, ac2)

    def test_get_purchase_buffer_new(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec1", "SEC1", price=50.0)
        ac.add_security(sec)
        self.assertTrue(abs(ac.get_purchase_buffer() - 7.5) < 10e-10)

    def test_get_purchase_buffer_update(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec1", "SEC1", "sec1_name", 50.0, 0)
        ac.add_security(sec)
        sec.set_price(100.0)
        self.assertTrue(abs(ac.get_purchase_buffer() - 15.0) < 10e-10)

    def test_get_security_exists(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC")
        ac.add_security(sec)
        self.assertEqual(ac.get_security("sec"), sec)

    def test_get_security_not_exists(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        self.assertRaises(Exception, ac.get_security, "sec")

    def test_get_holding_exists(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", "sec_name", 15.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        self.assertEqual(ac.get_holding("sec"), Holding(sec, 3, 15.0))

    def test_get_holding_not_exists(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", "sec_name", 15.0)
        ac.add_security(sec)
        self.assertRaises(Exception, ac.get_holding, "sec")

    def test_get_num_shares(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", "sec_name", 15.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        self.assertEqual(ac.get_num_shares(), 3)
        ac.buy(sec, 7, True)
        self.assertEqual(ac.get_num_shares(), 10)

    def test_get_cost(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", "sec_name", 15.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        self.assertEqual(ac.get_cost(), 45.0)

    def test_get_return_zero(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", "sec_name", 15.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        self.assertEqual(ac.get_return(), 0.0)

    def test_get_return_positive(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", "sec_name", 10.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        sec.set_price(11.0)
        self.assertEqual(ac.get_return(), 0.1)

    def test_get_return_negative(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", "sec_name", 10.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        sec.set_price(9.0)
        self.assertEqual(ac.get_return(), -0.1)

    def test_contains_security_false(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        self.assertFalse(ac.contains_security("sec"))

    def test_contains_security_true(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        ac.add_security(Security("sec", "SEC"))
        self.assertTrue(ac.contains_security("sec"))

    def test_contains_holding_false(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        self.assertFalse(ac.contains_holding("sec"))

    def test_contains_holding_true(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec = Security("sec", "SEC", price=30.0)
        ac.add_security(sec)
        ac.buy(sec, 1, True)
        self.assertTrue(ac.contains_holding("sec"))

    def test_get_value(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", "sec_name", 15.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        self.assertEqual(ac.get_value(), 45.0)

    def test_add_security_exists(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", "sec_name", 15.0)
        ac.add_security(sec)
        self.assertRaises(Exception, ac.add_security, sec)

    def test_add_security_not_exists(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        ac.add_security(Security("sec", "SEC"))
        self.assertEqual(ac.get_security("sec"), Security("sec", "SEC"))

    def test_add_holding_hs_hh(self):
        # TODO
        pass

    def test_add_holding_not_hs_hh(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", price=10.0)
        hol: Holding = Holding(sec, 3, 10.0)
        self.assertRaises(Exception, ac.add_holding, hol)

    def test_add_holding_hs_not_hh(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", price=10.0)
        ac.add_security(sec)
        ac.add_holding(Holding(sec, 3, 10.0))
        holding: Holding = ac.get_holding("sec")
        self.assertEqual(holding.get_value(), 30.0)
        self.assertEqual(holding.get_num_shares(), 3)
        self.assertEqual(holding.get_average_buy_price(), 10.0)

    def test_add_holding_not_hs_not_hh(self):
        # TODO
        pass

    def test_update_security(self):
        ac: AssetClass = AssetClass("ac", target_percentage=0.5)
        sec: Security = Security("sec", "SEC")
        ac.add_security(sec)
        ac.update_security("sec", "Security A", 100.0)
        new_sec: Security = ac.get_security("sec")
        self.assertEqual(new_sec.get_name(), "Security A")
        self.assertEqual(new_sec.get_price(), 100.0)

    def test_update_holding(self):
        ac: AssetClass = AssetClass("ac", target_percentage=0.5)
        sec: Security = Security(
            "sec", "SEC", name="sec_name", price=40.0, buy_restricted=0
        )
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        ac.update_holding("sec", 3, 45.0)
        new_hol: Holding = ac.get_holding("sec")
        self.assertEqual(new_hol.get_num_shares(), 3)
        self.assertEqual(new_hol.get_average_buy_price(), 45.0)

    def test_buy_new(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", price=5.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        self.assertEqual(ac.get_holding("sec"), Holding(sec, 3, 5.0))
        self.assertEqual(ac.get_value(), 15.0)

    def test_buy_update(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec: Security = Security("sec", "SEC", price=5.0)
        ac.add_security(sec)
        ac.buy(sec, 3, True)
        sec.set_price(15.0)
        ac.buy(sec, 3, True)
        self.assertEqual(ac.get_holding("sec"), Holding(sec, 6, 10.0))
        self.assertEqual(ac.get_value(), 90.0)

    def test_plan_purchases_knapsack_test_1(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec1: Security = Security("sec1", "SEC1", price=33.0, buy_restricted=0)
        sec2: Security = Security("sec2", "SEC2", price=49.0, buy_restricted=0)
        ac.add_security(sec1)
        ac.add_security(sec2)
        purchases: List[Purchase] = ac.plan_purchases(100)
        self.assertEqual(purchases, {"sec1": Purchase(sec1, 3)})

    def test_plan_purchases_knapsack_test_2(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec1: Security = Security("sec1", "SEC1", price=33.0, buy_restricted=0)
        sec2: Security = Security("sec2", "SEC2", price=49.0, buy_restricted=0)
        ac.add_security(sec1)
        ac.add_security(sec2)
        purchases: List[Purchase] = ac.plan_purchases(98.5)
        self.assertEqual(purchases, {"sec2": Purchase(sec2, 2)})

    def test_plan_purchases_buy_restricted_test_1(self):
        ac: AssetClass = AssetClass("ac", target_percentage=1.0)
        sec1: Security = Security("sec1", "SEC1", price=33.0, buy_restricted=0)
        sec2: Security = Security("sec2", "SEC2", price=49.0, buy_restricted=1)
        ac.add_security(sec1)
        ac.add_security(sec2)
        purchases: List[Purchase] = ac.plan_purchases(98.5)
        p1: Purchase = Purchase(sec1, 2)
        self.assertEqual(len(purchases), 1)
        self.assertEqual(purchases["sec1"], p1)


if __name__ == "__main__":
    unittest.main()
