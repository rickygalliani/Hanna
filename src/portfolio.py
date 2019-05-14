# Ricky Galliani
# Hanna
# src/portfolio.py

from src.asset_class import AssetClass
from src.deposit import Deposit
from src.security import Security

from prettytable import PrettyTable

import json

class Portfolio:

    def __init__(self):
        self.asset_classes = {}
        self.value = 0.0

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        acs = dict([(a, c.to_dict()) for (a, c) in self.asset_classes.items()])
        return {
            'asset_classes': acs,
            'value': self.value
        }

    def for_display(self):
        cols = ['Asset Class', 'Target Percentage', 'Percentage', 'Value']
        p = PrettyTable(cols)
        total_pct = 0.0
        acs = self.asset_classes.values()
        for ac in sorted(acs, key=lambda x: x.value, reverse=True):
            pct = self.get_asset_class_percentage(ac.name)
            total_pct += pct
            tgt_pct_str = "{}%".format(round(ac.target_percentage * 100, 2))
            pct_str = "{}%".format(round(pct * 100, 2))
            val_str = "${:,.2f}".format(ac.value)
            p.add_row([ac.name, tgt_pct_str, pct_str, val_str])
        tot_pct_str = "{}%".format(round(total_pct * 100, 2))
        tot_val_str = "${:,.2f}".format(self.value)
        p.add_row(['Total', '100%', tot_pct_str, tot_val_str])
        return "\n{}".format(p)

    def add_asset_class(self, asset_class):
        """
        Adds the given asset class to this portfolio.
        """
        self.asset_classes[asset_class.name] = asset_class
        self.value += asset_class.value

    def get_asset_class(self, asset_class_name):
        """
        Retrieves the asset class instance with the given name.
        """
        if asset_class_name in self.asset_classes:
            return self.asset_classes[asset_class_name]
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
            a.contains_security(security_id)
            for a in self.asset_classes.values()
        ])

    def get_asset_class_for_security(self, security_id):
        """
        Returns the asset class object containing the given security.
        """
        for ac in self.asset_classes.values():
            if ac.contains_security(security_id):
                return ac
        raise Exception(
            "Portfolio does not contain security {}.".format(security_id)
        )

    def get_asset_class_percentage(self, asset_class_name):
        """
        Returns the percentage of the portfolio invested in the given asset
        class.
        """
        ac = self.get_asset_class(asset_class_name)
        return ac.value / self.value

    def get_security_percentage(self, security_id):
        """
        Returns the percentage of this portfolio invested in the given
        security.
        """
        ac = self.get_asset_class_for_security(security_id)
        hol = ac.get_holding(security_id)
        return hol.value / self.value

    def get_asset_class_target_value(self, asset_class_name):
        """
        Returns the amount that should be invested in the given asset class.
        """
        ac = self.get_asset_class(asset_class_name)
        return self.value * ac.target_percentage

    def get_asset_class_target_deviation(self, asset_class_name):
        """
        Returns the deviation between the target and the achieved amount
        invested in the given asset class.
        """
        ac = self.get_asset_class(asset_class_name)
        target = self.get_asset_class_target_value(asset_class_name)
        return ac.value - target

    def get_asset_class_budgets(self, deposit):
        """
        Returns the spending budgets for the asset classes in the portfolio
        for a given deposit.
        """
        # Temporarily pretend our portfolio has deposit's value added to it
        self.value += deposit
        remaining_value = deposit
        ac_budgets = dict([(n, 0.0) for (n, ac) in self.asset_classes.items()])
        ac_devs = [
            (n, self.get_asset_class_target_deviation(n))
            for (n, ac) in self.asset_classes.items()
        ]
        ac_devs.sort(key=lambda x: x[1])
        for (n, ac_dev) in ac_devs:
            ac_budget = max(0, -1.0 * ac_dev)
            if ac_budget > remaining_value:
                ac_budget = remaining_value
            ac_budgets[n] = ac_budget
            remaining_value -= ac_budget
        # Remove deposit's value from portfolio
        self.value -= deposit
        return ac_budgets

    def update(self, robinhood_holdings):
        """
        Updates this portfolio (and its underlying asset classes and
        securities) with the given Robinhood holdings.
        """
        for rh in robinhood_holdings:
            # Add equity in this holding to portfolio total
            self.value += rh.equity

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
        rollover = 0.0  # Rollover allocations not spent in previous classes
        for (ac_name, budget) in self.get_asset_class_budgets(amount).items():
            ac = self.get_asset_class(ac_name)
            final_budget = budget + rollover
            ac_purchases = ac.plan_deposit(final_budget)
            ac_total = 0.0
            for sec_id, purchase in ac_purchases.items():
                deposit.add_purchase(ac.name, purchase)
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
                self.value += p.cost
                sec = Security(p.security_id, p.security_name, p.price)
                ac.add_holding(sec, p.num_shares)
