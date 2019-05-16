# Ricky Galliani
# Hanna
# src/portfolio.py

from src.deposit import Deposit
from src.security import Security

from prettytable import PrettyTable

import json


class Portfolio:

    def __init__(self):
        self.__asset_classes = {}
        self.__value = 0.0

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def get_asset_class_names(self):
        return self.__asset_classes.keys()

    def get_asset_classes(self):
        return self.__asset_classes.values()

    def get_value(self):
        return self.__value

    def add_value(self, amount):
        self.__value += amount

    def subtract_value(self, amount):
        self.__value -= amount

    def to_dict(self):
        acs = [(ac.to_dict()) for ac in self.get_asset_classes()]
        return {'asset_classes': acs, 'value': self.get_value()}

    def for_display(self):
        ac_cols = ['Asset Class', 'Target Percentage', 'Percentage', 'Value']
        sec_cols = ['Asset Class', 'Security', 'Shares', 'Percentage', 'Value']
        p_ac = PrettyTable(ac_cols)
        p_sec = PrettyTable(sec_cols)
        ac_tot_pct = 0.0
        sec_tot_pct = 0.0
        sec_tot_value = 0.0
        acs = self.get_asset_classes()
        for ac in sorted(acs, key=lambda x: x.get_value(), reverse=True):
            ac_name = ac.get_name()
            ac_pct = self.get_asset_class_percentage(ac_name)
            ac_tot_pct += ac_pct
            tgt_pct_str = '{:.1%}'.format(ac.get_target_percentage())
            pct_str = '{:.1%}'.format(ac_pct)
            val_str = "${:,.2f}".format(ac.get_value())
            p_ac.add_row([ac_name, tgt_pct_str, pct_str, val_str])
            hs = [(h, self.get_security_value(h.id)) for h in ac.get_holdings()]
            for hol, hol_val in sorted(hs, key=lambda h: h[1], reverse=True):
                sec = ac.get_security(hol.id).get_name()
                h_pct = self.get_security_percentage(hol.id)
                h_shares = hol.num_shares
                sec_tot_pct += h_pct
                sec_tot_value += hol_val
                h_pct_str = '{:.1%}'.format(h_pct)
                h_val_str = "${:,.2f}".format(hol_val)
                p_sec.add_row([ac_name, sec, h_shares, h_pct_str, h_val_str])
        ac_tot_pct_str = '{:.1%}'.format(ac_tot_pct)
        ac_tot_val_str = "${:,.2f}".format(self.get_value())
        sec_tot_pct_str = '{:.1%}'.format(sec_tot_pct)
        sec_tot_val_str = "${:,.2f}".format(sec_tot_value)
        p_ac.add_row(['Total', '100%', ac_tot_pct_str, ac_tot_val_str])
        p_sec.add_row(['Total', '-', '-', sec_tot_pct_str, sec_tot_val_str])
        return "\n{}\n{}".format(p_ac, p_sec)

    def contains_asset_class(self, asset_class_name):
        """
        Returns True if this portfolio contains an asset class with the given
        name.
        """
        return asset_class_name in self.__asset_classes

    def add_asset_class(self, asset_class):
        """
        Adds the given asset class to this portfolio.
        """
        self.__asset_classes[asset_class.get_name()] = asset_class
        self.__value += asset_class.get_value()

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

    def contains_security(self, security_id):
        """
        Returns whether the portfolio contains the given security.
        """
        return any([
            a.contains_security(security_id) for a in self.get_asset_classes()
        ])

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

    def get_asset_class_percentage(self, asset_class_name):
        """
        Returns the percentage of the portfolio invested in the given asset
        class.
        """
        return self.get_asset_class_value(asset_class_name) / self.get_value()

    def get_security_value(self, security_id):
        """
        Returns the value invested in the given security.
        """
        ac = self.get_asset_class_for_security(security_id)
        return ac.get_holding(security_id).value

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

    def get_asset_class_budgets(self, deposit):
        """
        Returns the spending budgets for the asset classes in the portfolio
        for a given deposit.
        """
        # Temporarily pretend our portfolio has deposit's value added to it
        self.add_value(deposit)
        remaining_value = deposit
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
        self.subtract_value(deposit)
        return ac_budgets

    def update(self, robinhood_holdings):
        """
        Updates this portfolio (and its underlying asset classes and
        securities) with the given Robinhood holdings.
        """
        for rh in robinhood_holdings:
            # Add equity in this holding to portfolio total
            self.add_value(rh.equity)

            # Update asset class data (and relevant underlying security data)
            if self.contains_security(rh.id):
                ac = self.get_asset_class_for_security(rh.id)
                ac.update(rh)
            else:
                # TODO: handle case where user has holdings not in portfolio
                #       config
                pass

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
            ac_purchases = ac.plan_deposit(final_budget)
            ac_total = 0.0
            for sec_id, purchase in ac_purchases.items():
                deposit.add_purchase(ac_name, purchase)
                ac_total += purchase.cost
            rollover = final_budget - ac_total
        return deposit

    def make_deposit(self, deposit):
        """
        Makes all the purchases in the given deposit, updating the state of
        this portfolio.
        """
        for (ac_name, purchases) in deposit.purchases.items():
            ac = self.get_asset_class(ac_name)
            for p in purchases:
                self.add_value(p.cost)
                sec = Security(p.security_id, p.security_name, p.price)
                ac.add_holding(sec, p.num_shares)
