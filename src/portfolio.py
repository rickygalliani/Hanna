# Ricky Galliani
# Hanna
# src/portfolio.py

from src.asset_class import AssetClass
from src.deposit import Deposit
from src.load import (
    load_account_profile,
    load_holding_info,
    load_security_info
)
from src.security import Security
from src.util import dollar_str, pct_str

from prettytable import PrettyTable

import json
import logging
import os


log = logging.getLogger(__name__)


class Portfolio:

    def __init__(self):
        """
        Initializes a portfolio using a user-specified configuration.
        """
        self.__asset_classes = {}
        self.__value = 0.0
        self.__cash = 0.0
        self.__num_shares = 0

        # Read portfolio configuration
        config = os.path.join(os.getcwd(), 'config', 'portfolio.json')
        self.load_from_config(config)
        log.info("Loaded portfolio configuration...")

    def load_from_config(self, config_file):
        """
        Loads the target investment portfolio (weights for asset classes and
        the securities underlying those asset classes) from the portfolio
        config.
        """
        co = open(config_file, 'r')
        portfolio_config = json.load(co)
        co.close()

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
            self.add_asset_class(ac)

        assert(abs(total_target_pct) - 1.0 < 1e-10)

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def get_asset_class_names(self):
        return self.__asset_classes.keys()

    def get_asset_classes(self):
        return self.__asset_classes.values()

    def get_cash(self):
        return self.__cash

    def get_value(self):
        return self.__value

    def get_num_shares(self):
        return self.__num_shares

    def add_value(self, amount):
        self.__value += amount

    def add_shares(self, num_shares):
        self.__num_shares += num_shares

    def subtract_value(self, amount):
        self.__value -= amount

    def subtract_shares(self, num_shares):
        self.__num_shares -= num_shares

    def subtract_cash(self, amount):
        self.__cash -= amount

    def set_cash(self, amount):
        self.__value -= self.__cash
        self.__cash = amount
        self.__value += self.__cash

    def add_asset_class(self, asset_class):
        self.__asset_classes[asset_class.get_name()] = asset_class
        self.add_value(asset_class.get_value())

    def to_dict(self):
        acs = [(ac.to_dict()) for ac in self.get_asset_classes()]
        return {
            'asset_classes': acs,
            'value': self.get_value(),
            'cash': self.get_cash(),
            'num_shares': self.get_num_shares()
        }

    def for_display(self):
        ac_cols = ['Asset Class', 'Target Percentage', 'Percentage', 'Value']
        sec_cols = [
            'Asset Class',
            'Security',
            'Symbol',
            'Restricted',
            'Shares',
            'Price',
            'Value',
            'Percentage',
        ]
        p_ac = PrettyTable(ac_cols)
        p_sec = PrettyTable(sec_cols)
        p_ac.title = 'Portfolio Asset Classes'
        p_sec.title = 'Portfolio Securities'
        acs = [(ac, ac.get_value()) for ac in self.get_asset_classes()]
        for ac, ac_value in sorted(acs, key=lambda x: x[1], reverse=True):
            ac_name = ac.get_name()
            p_ac.add_row([
                ac_name,
                pct_str(ac.get_target_percentage()),
                pct_str(self.get_asset_class_percentage(ac_name)),
                dollar_str(ac_value)
            ])
            hs = [
                (h, self.get_security_value(h.get_security().get_id())) for h
                in ac.get_holdings()
            ]
            for hol, hol_val in sorted(hs, key=lambda h: h[1], reverse=True):
                s = hol.get_security()
                p_sec.add_row([
                    ac_name,
                    s.get_name(),
                    s.get_symbol(),
                    s.get_buy_restricted(),
                    hol.get_num_shares(),
                    dollar_str(s.get_price()),
                    dollar_str(hol_val),
                    pct_str(self.get_security_percentage(s.get_id()))
                ])
        p_ac.add_row([
            'Cash',
            '-',
            pct_str(self.get_cash_percentage()),
            dollar_str(self.get_cash())
        ])
        p_ac.add_row([
            'Total', '100%', pct_str(1), dollar_str(self.get_value())
        ])
        p_sec.add_row([
            'Cash',
            '-',
            '-',
            '-',
            '-',
            '-',
            dollar_str(self.get_cash()),
            pct_str(self.get_cash_percentage()),
        ])
        p_sec.add_row([
            'Total',
            '-',
            '-',
            '-',
            self.get_num_shares(),
            '-',
            dollar_str(self.get_value()),
            pct_str(1)
        ])
        return "\n{}\n{}".format(p_ac, p_sec)

    def get_all_security_symbols(self):
        symbols = []
        for ac in self.get_asset_classes():
            for sec in ac.get_securities():
                symbols.append(sec.get_symbol())
        return symbols

    def contains_asset_class(self, asset_class_name):
        """
        Returns True if this portfolio contains an asset class with the given
        name.
        """
        return asset_class_name in self.get_asset_class_names()

    def contains_security(self, security_id):
        """
        Returns whether the portfolio contains the given security.
        """
        return any([
            a.contains_security(security_id) for a in self.get_asset_classes()
        ])

    def get_asset_class(self, asset_class_name):
        """
        Retrieves the asset class instance with the given name.
        """
        if self.contains_asset_class(asset_class_name):
            return self.__asset_classes[asset_class_name]
        raise Exception(
            "Portfolio does not contain a '{}' asset class.".format(
                asset_class_name
            )
        )

    def get_asset_class_for_security(self, security_id):
        """
        Returns the asset class object containing the given security.
        """
        for ac in self.get_asset_classes():
            if ac.contains_security(security_id):
                return ac
        raise Exception(
            "Portfolio does not contain security {}.".format(security_id)
        )

    def get_asset_class_value(self, asset_class_name):
        """
        Returns the value invested in the given asset class.
        """
        return self.get_asset_class(asset_class_name).get_value()

    def get_cash_percentage(self):
        """
        Returns the percentage of the portfolio value in cash.
        """
        total_value = self.get_value()
        if abs(total_value - 0 < 10e-10):
            return 0.0
        else:
            return 1.0 * self.get_cash() / total_value

    def get_asset_class_percentage(self, asset_class_name):
        """
        Returns the percentage of the portfolio invested in the given asset
        class.
        """
        total_value = self.get_value()
        if abs(total_value - 0 < 10e-10):
            return 0.0
        else:
            ac_value = self.get_asset_class_value(asset_class_name)
            return 1.0 * ac_value / total_value

    def get_security_value(self, security_id):
        """
        Returns the value invested in the given security.
        """
        ac = self.get_asset_class_for_security(security_id)
        return ac.get_holding(security_id).get_value()

    def get_security_percentage(self, security_id):
        """
        Returns the percentage of this portfolio invested in the given
        security.
        """
        return self.get_security_value(security_id) / self.get_value()

    def get_asset_class_target_value(self, asset_class_name):
        """
        Returns the amount that should be invested in the given asset class.
        """
        ac = self.get_asset_class(asset_class_name)
        return self.get_value() * ac.get_target_percentage()

    def get_asset_class_target_deviation(self, asset_class_name):
        """
        Returns the deviation between the target and the achieved amount
        invested in the given asset class.
        """
        ac = self.get_asset_class(asset_class_name)
        target = self.get_asset_class_target_value(asset_class_name)
        return ac.get_value() - target

    def get_asset_class_budgets(self, deposit_amount):
        """
        Returns the spending budgets for the asset classes in the portfolio
        for a given deposit.
        """
        # Temporarily pretend our portfolio has deposit's value added to it
        self.add_value(deposit_amount)
        remaining_value = deposit_amount
        ac_budgets = dict([
            (ac.get_name(), 0.0) for ac in self.get_asset_classes()
        ])
        ac_devs = []
        for ac in self.get_asset_classes():
            ac_name = ac.get_name()
            ac_dev = self.get_asset_class_target_deviation(ac.get_name())
            ac_devs.append((ac_name, ac_dev))
        ac_devs.sort(key=lambda x: x[1])
        for (n, ac_dev) in ac_devs:
            ac_budget = max(0, -1.0 * ac_dev)
            if ac_budget > remaining_value:
                ac_budget = remaining_value
            ac_budgets[n] = ac_budget
            remaining_value -= ac_budget
        # Remove deposit's value from portfolio
        self.subtract_value(deposit_amount)
        return ac_budgets

    def update(self, dry_run):
        """
        Updates this portfolio (and its underlying asset classes and
        securities) with the given Robinhood holdings.
        """
        account_profile = load_account_profile(dry_run)
        log.info("Pulled account profile from Robinhood...")

        security_symbols = self.get_all_security_symbols()
        securities = load_security_info(security_symbols, dry_run)
        log.info("Pulled security data from Robinhood...")

        holdings = load_holding_info(dry_run)
        log.info("Pulled holdings data from Robinhood...")

        cash = account_profile['margin_balances']['unallocated_margin_cash']
        self.set_cash(cash)
        for ac in self.get_asset_classes():
            for sec in ac.get_securities():
                sec_id = sec.get_id()
                sec_symbol = sec.get_symbol()
                sec_info = securities[sec_symbol]
                ac.update_security(sec_id, sec_info['name'], sec_info['price'])
                if sec_id in holdings:
                    hol_info = holdings[sec_id]
                    hol_shares = hol_info['quantity']
                    hol_value = hol_info['equity']
                    self.add_value(hol_value)
                    self.add_shares(hol_shares)
                    ac.update_holding(sec_id, hol_shares, hol_value)

    def plan_deposit(self, amount):
        """
        Returns the optimal purchases to make with deposit added to this
        portfolio.
        """
        # Compute purchases necessary to rebalance portfolio
        deposit = Deposit()
        budgets = sorted(
            self.get_asset_class_budgets(amount).items(),
            key=lambda x: x[1],
            reverse=True
        )
        rollover = 0.0  # Rollover allocations not spent in previous classes
        for (ac_name, budget) in budgets:
            ac = self.get_asset_class(ac_name)
            final_budget = budget + rollover
            if (ac_name, budget) == budgets[-1]:
                final_budget -= ac.get_purchase_buffer()
            ac_purchases = ac.plan_purchases(final_budget)
            ac_total = 0.0
            for purchase in ac_purchases.values():
                deposit.add_purchase(ac_name, purchase)
                ac_total += purchase.get_cost()
            rollover = final_budget - ac_total
        return deposit

    def make_deposit(self, deposit, dry_run):
        """
        Makes all the purchases in the given deposit, updating the state of
        this portfolio.
        """
        acs = [
            (ac, deposit.get_asset_class_expenditures(ac))
            for ac in deposit.get_involved_asset_classes()
        ]
        sorted_acs = sorted(acs, key=lambda x: x[1], reverse=True)
        for ac_name, _ in sorted_acs:
            ac = self.get_asset_class(ac_name)
            ps = deposit.get_purchases_for_asset_class(ac_name)
            purchases = sorted(ps, key=lambda x: x.get_cost(), reverse=True)
            for p in purchases:
                state = ac.buy(p.get_security(), p.get_num_shares(), dry_run)
                if state != 'failed':
                    m = "\t- Trade Status: {}\n".format(state.capitalize())
                    log.info(m)
                    cost = p.get_cost()
                    self.add_value(cost)
                    self.add_shares(p.get_num_shares())
                    self.subtract_cash(cost)
                else:
                    m = "\t- Trade Status: {}\n".format(state.capitalize())
                    log.error(m)
