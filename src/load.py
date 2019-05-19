# Ricky Galliani
# Hanna
# src/load.py

from src.asset_class import AssetClass
from src.portfolio import Portfolio
from src.security import Security

import os
import json

import robin_stocks as r


def load_credentials():
    """
    Loads the target investment portfolio credentials from the credentials
    config.
    """
    config_file = os.path.join(os.getcwd(), 'config', 'credentials.json')
    cr = open(config_file, 'r')
    credentials = json.load(cr)
    cr.close()
    assert('username' in credentials)
    assert('password' in credentials)
    return (credentials['username'], credentials['password'])


def load_portfolio_config():
    """
    Loads the target investment portfolio (weights for asset classes and the
    securities underlying those asset classes) from the portfolio config.
    """
    # Read portfolio configuration
    config_file = os.path.join(os.getcwd(), 'config', 'portfolio.json')
    co = open(config_file, 'r')
    portfolio_config = json.load(co)
    co.close()

    portfolio = Portfolio()
    total_target_pct = 0.0
    for a in portfolio_config:
        # Sanity check for config format
        assert('name' in a)
        assert('target_percentage' in a)
        assert('securities' in a)
        assert('buy_restrictions' in a)

        ac_target_pct = float(a['target_percentage'])
        ac = AssetClass(a['name'], ac_target_pct)
        total_target_pct += ac_target_pct
        for s_symbol, s_id in a['securities'].items():
            s = Security(s_id,
                         s_symbol,
                         buy_restricted=s_symbol in a['buy_restrictions'])
            ac.add_security(s)
        portfolio.add_asset_class(ac)

    assert(abs(total_target_pct) - 1.0 < 1e-10)
    return portfolio


def load_security_info(security_symbols):
    """
    Hits the Robinhood API to pull down security information like the latest
    price and the full security name.
    """
    holding_info = json.load(open('test/data/security_info.json', 'r'))
    for (security, info) in holding_info.items():
        info['price'] = float(info['price'])
    # holding_info = {}
    # for sec_sym in security_symbols:
    #     holding_info[sec_sym] = {
    #         'name': r.get_name_by_symbol(sec_sym),
    #         'price': r.get_latest_price(sec_sym)
    #     }
    return holding_info


def load_holding_info():
    """
    Hits the Robinhood API to pull down user's holdings data.
    """
    # robinhood_resp = r.build_holdings().values()
    robinhood_resp = json.load(open('test/data/holding_info.json', 'r'))
    holdings = {}
    for s in robinhood_resp:
        s_id = s['id']
        holdings[s_id] = {
            'id': s_id,
            'name': s['name'],
            'price': float(s['price']),
            'quantity': int(float(s['quantity'])),
            'average_buy_price': float(s['average_buy_price']),
            'equity': float(s['equity']),
            'percentage': float(s['percentage']),
            'percent_change': float(s['percent_change']),
            'equity_change': float(s['equity_change']),
            'type': s['type']
        }
    return holdings
