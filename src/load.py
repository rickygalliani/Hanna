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
    Loads the credentials for the Robinhood account.
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


def load_account_profile(use_mock_data):
    """
    Loads user profile information from Robinhood including total equity,
    cash, and dividend total.
    """
    account_profile_mock_file = 'test/data/account_profile.json'
    if use_mock_data:
        resp = json.load(open(account_profile_mock_file, 'r'))
    else:
        resp = r.load_account_profile()
    assert('margin_balances' in resp)
    assert('unallocated_margin_cash' in resp['margin_balances'])
    cash = resp['margin_balances']['unallocated_margin_cash']
    resp['margin_balances']['unallocated_margin_cash'] = float(cash)
    return resp


def load_security_info(security_symbols, use_mock_data):
    """
    Hits the Robinhood API to pull down security information like the latest
    price and the full security name.
    """
    if use_mock_data:
        holding_info = json.load(open('test/data/security_info.json', 'r'))
    else:
        holding_info = {}
        for sec_sym in security_symbols:
            holding_info[sec_sym] = {
                'name': r.get_name_by_symbol(sec_sym),
                'price': r.get_latest_price(sec_sym)
            }
    for (security, info) in holding_info.items():
        info['price'] = float(info['price'][0])
    return holding_info


def load_holding_info(use_mock_data):
    """
    Hits the Robinhood API to pull down user's holdings data.
    """
    if use_mock_data:
        resp = json.load(open('test/data/holding_info.json', 'r'))
    else:
        resp = r.build_holdings().values()
    holdings = {}
    for s in resp:
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
