# Ricky Galliani
# Hanna
# main.py

from src.asset_class import AssetClass
from src.security import Security
from src.load import (
    load_credentials,
    load_portfolio_config,
    load_holding_info,
    load_security_info
)

from random import shuffle

import json
import logging
import robin_stocks as r
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
    log.info("Deposit Amount: ${:,.2f}".format(amount))

    portfolio = load_portfolio_config()
    log.info("Loaded portfolio configuration...")

    # Populate asset classes and securities with holdings data
    user, password = load_credentials()
    # client = r.login(username, password)
    holding_info = load_holding_info()
    log.info("Pulled holdings data from Robinhood...")
    security_info = load_security_info(portfolio.get_all_security_symbols())
    log.info("Pulled security data from Robinhood...")

    portfolio.update(holding_info, security_info)
    log.info("Updated portfolio with holdings and security data...")

    log.info("Portfolio before deposit:{}".format(portfolio.for_display()))

    deposit = portfolio.plan_deposit(amount)
    log.info("Deposit:{}".format(deposit.for_display()))

    portfolio.make_deposit(deposit)
    log.info("Portfolio after deposit:{}".format(portfolio.for_display()))
