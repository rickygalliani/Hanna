# Ricky Galliani
# Hanna
# main.py

from src.portfolio import Portfolio
from src.api import Credentials, load_credentials

import argparse
import json
import logging
import os
import robin_stocks as r


if __name__ == "__main__":

    logging.basicConfig(
        format="%(asctime)-15s %(levelname)s: %(message)s", level=logging.INFO
    )
    log = logging.getLogger("main")

    parser = argparse.ArgumentParser(description="Hanna main program.")
    parser.add_argument(
        "--online", required=False, default=False, action="store_true"
    )
    parser.add_argument(
        "--logging", required=False, default=False, action="store_true"
    )

    args = parser.parse_args()

    portfolio = Portfolio()
    config = os.path.join(os.getcwd(), "config", "portfolio.json")
    portfolio.load_configuration(json.load(open(config, "r")))

    if args.online:
        c: Credentials = load_credentials()
        client = r.login(c.get_username(), c.get_password())

    portfolio.refresh(args.online, args.logging)
    deposit = portfolio.plan_deposit(portfolio.get_cash())
    portfolio.make_deposit(deposit, args.online)
    portfolio.refresh(args.online, args.logging)

    if args.online:
        r.logout()
