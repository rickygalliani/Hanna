# Ricky Galliani
# Hanna
# onboard.py

from typing import Any, Dict, Tuple

import logging
import os
import robin_stocks as r


def setup_security(sec_num: int) -> Tuple[str, bool]:
    """
    Collects user input to set up a security".
    """
    sec_sym: str = input(
        "\t\tEnter the symbol of security {}: ".format(sec_num)
    )
    instrument: Dict[str, Any] = r.get_instruments_by_symbols([sec_sym])[0]
    security_id: str = instrument["id"]
    security_name: str = instrument["name"]
    confirm_security_str: str = input(
        "\t\t\tConfirm {}: [Y/n] ".format(security_name)
    )
    confirm_security: bool = (
        confirm_security_str.lower() == "y" or confirm_security_str == ""
    )
    if not confirm_security:
        setup_security()
    allow_purchase_str: str = input(
        "\t\t\tAllow purchase: [Y/n] ".format(security_name)
    )
    allow_purchase: bool = (
        allow_purchase_str.lower() == "y" or allow_purchase_str == ""
    )
    return (security_id, allow_purchase)


def setup_asset_class(ac_num: int) -> Dict[str, str]:
    """
    Collects user input to set up an asset class.
    """
    asset_class: Dict[str, Any] = {}

    # Get name
    ac_name: str = input("Enter the name of asset class {}: ".format(ac_num))
    asset_class["name"] = ac_name

    # Get target percentage
    ac_target_pct: str = input(
        "\tEnter target percentage of the {} (in [0, 1]): ".format(ac_name)
    )
    asset_class["target_percentage"] = float(ac_target_pct)

    # Get securities and buy restrictions
    asset_class["securities"] = []
    asset_class["buy_restrctions"] = []
    sec_num: int = 1
    add_sec: bool = True
    while add_sec:
        security: Tuple[str, bool] = setup_security(sec_num)
        security_id: str = security[0]
        allow_purchase: bool = security[1]
        asset_class["securities"].append(security_id)
        if not allow_purchase:
            asset_class["buy_restrctions"].append(security_id)
        add_sec_str: str = input(
            "\tAdd another security to {}? [Y/n] ".format(ac_name)
        )
        add_sec = add_sec_str.lower() == "y" or add_sec_str == ""
        sec_num += 1
    return asset_class


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s: %(message)s", level=logging.INFO
    )
    log = logging.getLogger("onboard")

    config = os.path.join(os.getcwd(), "config", "test_portfolio.json")

    ac_num: int = 1
    add_asset_class: bool = True
    while add_asset_class:
        ac: Dict[str, str] = setup_asset_class(ac_num)
        add_asset_class_str: str = input("\nAdd an additional class? [Y/n] ")
        add_asset_class = (
            add_asset_class_str.lower() == "y" or add_asset_class_str == ""
        )
        ac_num += 1
