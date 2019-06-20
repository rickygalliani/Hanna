# Ricky Galliani
# Hanna
# src/api.py

from typing import Any, Dict, List, Tuple

import os
import json
import logging
import robin_stocks as r


log = logging.getLogger(__name__)


class Credentials:
    def __init__(self, username: str, password: str) -> None:
        self.__username: str = username
        self.__password: str = password

    def get_username(self) -> str:
        return self.__username

    def get_password(self) -> str:
        return self.__password


class AccountProfile:
    def __init__(self, buying_power: float) -> None:
        self.__buying_power: float = buying_power

    def get_buying_power(self) -> float:
        return self.__buying_power


class SecurityInfo:
    def __init__(self, name: str, price: float) -> None:
        self.__name: str = name
        self.__price: float = price

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price


class HoldingInfo:
    def __init__(
        self,
        security_id: str,
        name: str,
        price: float,
        quantity: int,
        average_buy_price: float,
        equity: float,
        percentage: float,
        percent_change: float,
        equity_change: float,
    ) -> None:
        self.__security_id: str = security_id
        self.__name: str = name
        self.__price: float = price
        self.__quantity: int = quantity
        self.__average_buy_price: float = average_buy_price
        self.__equity: float = equity
        self.__percentage: float = percentage
        self.__percent_change: float = percent_change
        self.__equity_change: float = equity_change

    def get_security_id(self) -> str:
        return self.__security_id

    def get_name(self) -> str:
        return self.__name

    def get_price(self) -> float:
        return self.__price

    def get_quantity(self) -> int:
        return self.__quantity

    def get_average_buy_price(self) -> float:
        return self.__average_buy_price

    def get_equity(self) -> float:
        return self.__equity

    def get_percentage(self) -> float:
        return self.__percentage

    def get_percent_change(self) -> float:
        return self.__percent_change

    def get_equity_change(self) -> float:
        return self.__equity_change


def load_credentials() -> Credentials:
    """
    Loads the credentials for the Robinhood account.
    """
    config_file: str = os.path.join(os.getcwd(), "config", "credentials.json")
    cr = open(config_file, "r")
    credentials: Credentials = Credentials(**json.load(cr))
    cr.close()
    return credentials


def load_account_profile(use_mock_data: bool) -> AccountProfile:
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
    buying_power: float = float(
        resp["margin_balances"]["unallocated_margin_cash"]
    )
    return AccountProfile(buying_power)


def load_security_info(
    security_symbols: List[str], use_mock_data: bool
) -> Dict[str, SecurityInfo]:
    """
    Hits the Robinhood API to pull down security information like the latest
    price and the full security name.
    """
    security_info_resp: Dict[str, Any] = {}
    if use_mock_data:
        security_info_resp = json.load(
            open("test/data/security_info.json", "r")
        )
    else:
        for sec_sym in security_symbols:
            security_info_resp[sec_sym] = {
                "name": r.get_name_by_symbol(sec_sym),
                "price": r.get_latest_price(sec_sym),
            }
    security_info: Dict[str, SecurityInfo] = {}
    for (security, info) in security_info_resp.items():
        security_info[security] = SecurityInfo(
            info["name"], float(info["price"][0])
        )
    return security_info


def load_holding_info(use_mock_data: bool) -> Dict[str, HoldingInfo]:
    """
    Hits the Robinhood API to pull down user's holdings data.
    """
    resp: List[Dict[str, Any]] = (
        json.load(open("test/data/holding_info.json", "r"))
        if use_mock_data
        else r.build_holdings().values()
    )
    holdings: Dict[str, HoldingInfo] = {}
    for s in resp:
        s_id: str = s["id"]
        holdings[s_id] = HoldingInfo(
            s_id,
            s["name"],
            float(s["price"]),
            int(float(s["quantity"])),
            float(s["average_buy_price"]),
            float(s["equity"]),
            float(s["percentage"]),
            float(s["percent_change"]),
            float(s["equity_change"]),
        )
    return holdings
