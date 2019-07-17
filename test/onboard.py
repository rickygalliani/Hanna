# Ricky Galliani
# Hanna
# test/onboard.py

from onboard import (
    ask_allow_purchase,
    ask_asset_class_name,
    ask_confirm_security,
    ask_target_pct,
)

from unittest.mock import patch

import unittest

# Usage: python3 -m unittest --verbose test.onboard


class OnboardTest(unittest.TestCase):
    @patch("onboard.ask_user_input", return_value="y")
    def test_ask_security(self, _):
        # TODO: can't call get_instruments_by_symbol() offline
        pass

    @patch("onboard.ask_user_input", return_value="y")
    def test_ask_confirm_security_y(self, _):
        self.assertTrue(ask_confirm_security("Sec Name"))

    @patch("onboard.ask_user_input", return_value="Y")
    def test_ask_confirm_security_Y(self, _):
        self.assertTrue(ask_confirm_security("Sec Name"))

    @patch("onboard.ask_user_input", return_value="")
    def test_ask_confirm_security_blank(self, _):
        self.assertTrue(ask_confirm_security("Sec Name"))

    @patch("onboard.ask_user_input", return_value="n")
    def test_ask_confirm_security_n(self, _):
        self.assertFalse(ask_confirm_security("Sec Name"))

    @patch("onboard.ask_user_input", return_value="N")
    def test_ask_confirm_security_N(self, _):
        self.assertFalse(ask_confirm_security("Sec Name"))

    @patch("onboard.ask_user_input", return_value="y")
    def test_ask_allow_purchase_y(self, _):
        self.assertTrue(ask_allow_purchase())

    @patch("onboard.ask_user_input", return_value="Y")
    def test_ask_allow_purchase_Y(self, _):
        self.assertTrue(ask_allow_purchase())

    @patch("onboard.ask_user_input", return_value="")
    def test_ask_allow_purchase_blank(self, _):
        self.assertTrue(ask_allow_purchase())

    @patch("onboard.ask_user_input", return_value="n")
    def test_ask_allow_purchase_n(self, _):
        self.assertFalse(ask_allow_purchase())

    @patch("onboard.ask_user_input", return_value="N")
    def test_ask_allow_purchase_N(self, _):
        self.assertFalse(ask_allow_purchase())

    @patch("onboard.ask_user_input", return_value="Sample AC Name")
    def test_ask_asset_class_name(self, _):
        self.assertEqual(ask_asset_class_name(True), "Sample AC Name")

    @patch("onboard.ask_user_input", return_value="0.5345")
    def test_ask_target_pct(self, _):
        self.assertEqual(ask_target_pct("Sample AC Name", 1.0), 0.5345)


if __name__ == "__main__":
    unittest.main()
