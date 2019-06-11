# Ricky Galliani
# Hanna
# main.py

from src.portfolio import Portfolio
from src.load import load_credentials

import argparse
import logging
import os
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

    portfolio = Portfolio()
    config = os.path.join(os.getcwd(), 'config', 'portfolio.json')
    portfolio.load_from_config(config)

    if args.real:
        user, password = load_credentials()
        client = r.login(user, password)

    portfolio.refresh(not args.real)
    deposit = portfolio.plan_deposit(portfolio.get_cash())
    portfolio.make_deposit(deposit, not args.real)
    portfolio.refresh(not args.real)

    if args.real:
        r.logout()
