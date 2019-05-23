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

    dev_mode = True

    amount = float(sys.argv[1])
    log.info("Deposit Amount: ${:,.2f}".format(amount))

    portfolio = load_portfolio_config()
    log.info("Loaded portfolio configuration...")

    # Populate asset classes and securities with holdings data
    if not dev_mode:
        user, password = load_credentials()
        client = r.login(user, password)
    security_symbols = portfolio.get_all_security_symbols()
    securities = load_security_info(security_symbols, dev_mode)
    log.info("Pulled security data from Robinhood...")
    holdings = load_holding_info(dev_mode)
    log.info("Pulled holdings data from Robinhood...")

    portfolio.update(securities, holdings)
    log.info("Updated portfolio with holdings and security data...")

    log.info("Portfolio before deposit:{}".format(portfolio.for_display()))

    deposit = portfolio.plan_deposit(amount)
    log.info("Deposit:{}".format(deposit.for_display()))

    portfolio.make_deposit(deposit)
    log.info("Portfolio after deposit:{}".format(portfolio.for_display()))
