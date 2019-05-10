# Ricky Galliani
# main.py

from src.asset_class import AssetClass
from src.security import Security
from src.load import (
    load_credentials,
    load_portfolio_config,
    load_robinhood_holdings
)

from random import shuffle

import json
import logging
import sys


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)s: %(message)s',
        level=logging.INFO
    )
    log = logging.getLogger('rebalancer')

    # Load command line credentials
    if len(sys.argv) != 2:
        log.error("[USAGE]: python3 rebalancer.py <amount>")
        sys.exit(1)

    amount = float(sys.argv[1])
    log.info("Deposit Amount: ${}".format(amount))

    portfolio = load_portfolio_config()
    log.info("Loaded portfolio configuration...")

    # Populate asset classes and securities with holdings data
    username, password = load_credentials()
    robinhood_holdings = load_robinhood_holdings(username, password)
    log.info("Pulled Robinhood holdings data...")

    portfolio.update(robinhood_holdings)
    log.info("Updated portfolio with Robinhood holdings data...")

    log.info(portfolio.for_display())

    deposit = portfolio.plan_deposit(amount)
    log.info(deposit.for_display())
