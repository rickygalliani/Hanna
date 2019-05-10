# Ricky Galliani
# Hanna
# src/load.py

from src.asset_class import AssetClass
from src.portfolio import Portfolio
from src.robinhood_holding import RobinhoodHolding
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
    config_file = os.path.join(os.getcwd(), 'config', 'portfolio_config.json')
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
        
        ac_target_pct = float(a['target_percentage'])
        ac = AssetClass(a['name'], ac_target_pct)
        total_target_pct += ac_target_pct
        for sec_id in a['securities']:
            ac.add_security(Security(sec_id))
        
        portfolio.add_asset_class(ac)
    
    assert(abs(total_target_pct) - 1.0 < 1e-10)
    return portfolio


def load_robinhood_holdings(username, password):
    """
    Hits the Robinhood API to pull down user's holdings data.
    """
    # client = r.login(username, password)
    # robinhood_resp = r.build_holdings().values()
    robinhood_resp = json.load(open('test/data/response1.json', 'r'))
    holdings = []
    for s in robinhood_resp:
        holdings.append(
            RobinhoodHolding(
                s['id'],
                s['name'],
                float(s['price']),
                int(float(s['quantity'])),
                float(s['average_buy_price']),
                float(s['equity']),
                float(s['percentage']),
                float(s['percent_change']),
                float(s['equity_change']),
                s['type']
            )
        )
    return holdings
