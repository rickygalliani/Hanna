# Ricky Galliani
# Hanna
# src/api.py

from datetime import datetime

from typing import Any, Dict, List

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


def load_account_profile(t: datetime, use_mock_data: bool) -> AccountProfile:
    """
    Loads user profile information from Robinhood including total equity,
    cash, and dividend total.
    """
    resp: Dict[str, Any] = {}
    account_profile_output_dir: str = os.path.join(
        "test", "data", "account_profile"
    )
    if not use_mock_data:
        resp = r.load_account_profile()
        if not os.path.exists(account_profile_output_dir):
            os.makedirs(account_profile_output_dir)
        account_profile_output_file = os.path.join(
            account_profile_output_dir,
            "{}.json".format(t.strftime("%Y_%m_%d_%H_%M_%S")),
        )
        with open(account_profile_output_file, "w") as f:
            f.write(json.dumps(resp, indent=4))
    else:
        latest = sorted(
            [
                datetime.strptime(x.replace(".json", ""), "%Y_%m_%d_%H_%M_%S")
                for x in os.listdir(account_profile_output_dir)
            ]
        )[0]
        account_profile_latest_file: str = os.path.join(
            "test",
            "data",
            "account_profile",
            "{}.json".format(latest.strftime("%Y_%m_%d_%H_%M_%S")),
        )
        resp = json.load(open(account_profile_latest_file, "r"))
    assert "margin_balances" in resp
    assert "unallocated_margin_cash" in resp["margin_balances"]
    buying_power: float = float(
        resp["margin_balances"]["unallocated_margin_cash"]
    )
    return AccountProfile(buying_power)


def load_security_info(
    security_symbols: List[str], t: datetime, use_mock_data: bool
) -> Dict[str, SecurityInfo]:
    """
    Hits the Robinhood API to pull down security information like the latest
    price and the full security name.
    """
    resp: Dict[str, Any] = {}
    security_info_output_dir: str = os.path.join(
        "test", "data", "security_info"
    )
    resp: Dict[str, Any] = {}
    if not use_mock_data:
        for sec_sym in security_symbols:
            resp[sec_sym] = {
                "name": r.get_name_by_symbol(sec_sym),
                "price": r.get_latest_price(sec_sym),
            }
        if not os.path.exists(security_info_output_dir):
            os.makedirs(security_info_output_dir)
        security_info_output_file = os.path.join(
            security_info_output_dir,
            "{}.json".format(t.strftime("%Y_%m_%d_%H_%M_%S")),
        )
        with open(security_info_output_file, "w") as f:
            f.write(json.dumps(resp, indent=4))
    else:
        latest = sorted(
            [
                datetime.strptime(x.replace(".json", ""), "%Y_%m_%d_%H_%M_%S")
                for x in os.listdir(security_info_output_dir)
            ]
        )[0]
        security_info_latest_file: str = os.path.join(
            "test",
            "data",
            "security_info",
            "{}.json".format(latest.strftime("%Y_%m_%d_%H_%M_%S")),
        )
        resp = json.load(open(security_info_latest_file, "r"))
    security_info: Dict[str, SecurityInfo] = {}
    for (security, info) in resp.items():
        security_info[security] = SecurityInfo(
            info["name"], float(info["price"][0])
        )
    return security_info


def load_holding_info(
    t: datetime, use_mock_data: bool
) -> Dict[str, HoldingInfo]:
    """
    Hits the Robinhood API to pull down user's holdings data.
    """
    resp: List[Dict[str, Any]] = {}
    holding_info_output_dir: str = os.path.join("test", "data", "holding_info")
    if not use_mock_data:
        resp = r.build_holdings().values()
        if not os.path.exists(holding_info_output_dir):
            os.makedirs(holding_info_output_dir)
        holding_info_output_file = os.path.join(
            holding_info_output_dir,
            "{}.json".format(t.strftime("%Y_%m_%d_%H_%M_%S")),
        )
        with open(holding_info_output_file, "w") as f:
            # TODO fix here!
            f.write(json.dumps(resp.get(), indent=4))
    else:
        latest = sorted(
            [
                datetime.strptime(x.replace(".json", ""), "%Y_%m_%d_%H_%M_%S")
                for x in os.listdir(holding_info_output_dir)
            ]
        )[0]
        holding_info_latest_file: str = os.path.join(
            "test",
            "data",
            "holding_info",
            "{}.json".format(latest.strftime("%Y_%m_%d_%H_%M_%S")),
        )
        resp = json.load(open(holding_info_latest_file, "r"))
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
