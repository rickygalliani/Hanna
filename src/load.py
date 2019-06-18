# Ricky Galliani
# Hanna
# src/load.py

from typing import Any, Dict, List, Tuple

import os
import json
import logging
import robin_stocks as r


log = logging.getLogger(__name__)


def load_credentials() -> Tuple[str, str]:
    """
    Loads the credentials for the Robinhood account.
    """
    config_file: str = os.path.join(os.getcwd(), "config", "credentials.json")
    cr = open(config_file, "r")
    credentials: Dict[str, str] = json.load(cr)
    cr.close()
    assert "username" in credentials
    assert "password" in credentials
    return (credentials["username"], credentials["password"])


def load_account_profile(use_mock_data: bool) -> Dict[str, Any]:
    """
    Loads user profile information from Robinhood including total equity,
    cash, and dividend total.
    """
    account_profile_mock_file: str = "test/data/account_profile.json"
    resp: Dict[str, Any] = (
        json.load(open(account_profile_mock_file, "r"))
        if use_mock_data
        else r.load_account_profile()
    )
    assert "margin_balances" in resp
    assert "unallocated_margin_cash" in resp["margin_balances"]
    cash: float = resp["margin_balances"]["unallocated_margin_cash"]
    resp["margin_balances"]["unallocated_margin_cash"] = float(cash)
    return resp


def load_security_info(
    security_symbols: List[str], use_mock_data: bool
) -> Dict[str, Any]:
    """
    Hits the Robinhood API to pull down security information like the latest
    price and the full security name.
    """
    security_info: Dict[str, Any] = {}
    if use_mock_data:
        security_info = json.load(open("test/data/security_info.json", "r"))
    else:
        security_info = {}
        for sec_sym in security_symbols:
            security_info[sec_sym] = {
                "name": r.get_name_by_symbol(sec_sym),
                "price": r.get_latest_price(sec_sym),
            }
    for (security, info) in security_info.items():
        info["price"] = float(info["price"][0])
    return security_info


def load_holding_info(use_mock_data: bool) -> Dict[str, Any]:
    """
    Hits the Robinhood API to pull down user's holdings data.
    """
    resp: List[Dict[str, Any]] = (
        json.load(open("test/data/holding_info.json", "r"))
        if use_mock_data
        else r.build_holdings().values()
    )
    holdings: Dict[str, Any] = {}
    for s in resp:
        s_id: str = s["id"]
        holdings[s_id] = {
            "id": s_id,
            "name": s["name"],
            "price": float(s["price"]),
            "quantity": int(float(s["quantity"])),
            "average_buy_price": float(s["average_buy_price"]),
            "equity": float(s["equity"]),
            "percentage": float(s["percentage"]),
            "percent_change": float(s["percent_change"]),
            "equity_change": float(s["equity_change"]),
            "type": s["type"],
        }
    return holdings
