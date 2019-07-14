# Ricky Galliani
# Hanna
# onboard.py

from typing import Any, Dict, Tuple

import logging
import os
import robin_stocks as r


def setup_security() -> Tuple[str, bool]:
    """
    Collects user input to set up a security".
    """
    sec_sym: str = input("\t\tEnter the security symbol: ")
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


def setup_asset_class() -> Dict[str, str]:
    """
    Collects user input to set up an asset class.
    """
    asset_class: Dict[str, Any] = {}

    # Get name
    ac_name: str = input("Enter the name of the asset class: ")
    asset_class["name"] = ac_name

    # Get target percentage
    ac_target_pct: str = input(
        "\tEnter target percentage of the asset class (in [0, 1]): "
    )
    asset_class["target_percentage"] = float(ac_target_pct)

    # Get securities and buy restrictions
    asset_class["securities"] = []
    asset_class["buy_restrctions"] = []
    add_sec_str: str = input("\tAdd security to {}? [Y/n] ".format(ac_name))
    add_sec: bool = add_sec_str.lower() == "y" or add_sec_str == ""
    while add_sec:
        security: Tuple[str, bool] = setup_security()
        security_id: str = security[0]
        allow_purchase: bool = security[1]
        asset_class["securities"].append(security_id)
        if not allow_purchase:
            asset_class["buy_restrctions"].append(security_id)
        add_sec_str: str = input(
            "\tAdd another security to {}? [Y/n] ".format(ac_name)
        )
        add_sec: bool = add_sec_str.lower() == "y" or add_sec_str == ""

    return asset_class


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s: %(message)s", level=logging.INFO
    )
    log = logging.getLogger("onboard")

    config = os.path.join(os.getcwd(), "config", "test_portfolio.json")

    add_asset_class_str: str = input("\nAdd an asset class? [Y/n] ")
    add_asset_class: bool = (
        add_asset_class_str.lower() == "y" or add_asset_class_str == ""
    )
    if add_asset_class:
        ac: Dict[str, str] = setup_asset_class()
        print("ac = {}".format(ac))
