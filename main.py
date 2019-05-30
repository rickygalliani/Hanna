# Ricky Galliani
# Hanna
# main.py

from src.asset_class import AssetClass
from src.security import Security
from src.load import (
    load_credentials,
    load_portfolio_config,
    load_account_profile,
    load_holding_info,
    load_security_info
)

from random import shuffle

import json
import logging
import robin_stocks as r


if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)-15s %(levelname)s: %(message)s',
        level=logging.INFO
    )
    log = logging.getLogger('main')

    dry_run = True

    portfolio = load_portfolio_config()
    log.info("Loaded portfolio configuration...")

    # Populate asset classes and securities with holdings data
    if not dry_run:
        user, password = load_credentials()
        client = r.login(user, password)
    
    account_profile = load_account_profile(dry_run)
    log.info("Pulled account profile from Robinhood...")
    
    security_symbols = portfolio.get_all_security_symbols()
    securities = load_security_info(security_symbols, dry_run)
    log.info("Pulled security data from Robinhood...")

    holdings = load_holding_info(dry_run)
    log.info("Pulled holdings data from Robinhood...")

    portfolio.update(account_profile, securities, holdings)
    log.info("Updated portfolio with holdings and security data...")

    log.info("Portfolio before deposit:{}".format(portfolio.for_display()))

    deposit = portfolio.plan_deposit(portfolio.get_cash())
    log.info("Deposit:{}".format(deposit.for_display()))

    portfolio.make_deposit(deposit, dry_run)
    log.info("Portfolio after deposit:{}".format(portfolio.for_display()))
