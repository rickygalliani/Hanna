# Ricky Galliani
# Hanna
# main.py

from src.asset_class import AssetClass
from src.portfolio import Portfolio
from src.security import Security
from src.load import load_credentials

from random import shuffle

import argparse
import json
import logging
import robin_stocks as r


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)s: %(message)s',
        level=logging.INFO
    )
    log = logging.getLogger('main')

    parser = argparse.ArgumentParser(description='Hanna main program.')
    parser.add_argument(
        '--real',
        required=False,
        default=False,
        action='store_true'
    )
    args = parser.parse_args()
    print("args = {}".format(args))

    portfolio = Portfolio()

    # Populate asset classes and securities with holdings data
    if args.real:
        user, password = load_credentials()
        client = r.login(user, password)

    portfolio.update(not args.real)
    log.info("Updated portfolio with holdings and security data...")

    log.info("Portfolio before deposit:{}".format(portfolio.for_display()))

    deposit = portfolio.plan_deposit(portfolio.get_cash())
    log.info("Deposit:{}".format(deposit.for_display()))

    portfolio.make_deposit(deposit, not args.real)
    log.info("Portfolio after deposit:{}".format(portfolio.for_display()))

    if args.real:
        r.logout()
