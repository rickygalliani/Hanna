# Ricky Galliani
# Hanna
# src/portfolio.py

from src.asset_class import AssetClass
from src.deposit import Deposit
from src.security import Security

import json

class Portfolio:

    def __init__(self):
        self.asset_classes = {}
        self.total_holdings = None 

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        acs = dict([(a, c.to_dict()) for (a, c) in self.asset_classes.items()])
        return {
            'asset_classes': acs,
            'total_holdings': self.total_holdings
        }

    def for_display(self):
        ac_len = 25
        hold_len = 20
        pct_len = 18
        tgt_pct_len = 20
        sep = '\n\t' + '-' * (ac_len + hold_len + pct_len + tgt_pct_len)
        out = [
            '\n\nPortfolio:',
            '\n\n\t',
            'Asset Class'.ljust(ac_len),
            'Holdings'.ljust(hold_len),
            'Percentage'.ljust(pct_len),
            'Target Percentage'.ljust(tgt_pct_len),
            sep
        ]
        total_pct = 0.0
        acs = self.asset_classes.values()
        for ac in sorted(acs, key=lambda x: x.holdings, reverse=True):
            pct = self.get_asset_class_percentage(ac.name)
            total_pct += pct
            hold = "${:,.2f}".format(ac.holdings).ljust(hold_len)
            pct_str = "{}%".format(str(round(pct * 100, 2))).ljust(pct_len)
            tgt_pct = "{}%".format(
                str(round(ac.target_percentage * 100, 2))).ljust(tgt_pct_len)
            out.append("\n\t{name}{hold}{pct_str}{tgt_pct}".format(
                name=ac.name.ljust(ac_len),
                hold=hold,
                pct_str=pct_str,
                tgt_pct=tgt_pct
            ))
        tot_hold = "${:,.2f}".format(self.total_holdings).ljust(hold_len)
        tot_pct = "{}%".format(str(round(total_pct * 100, 2))).ljust(pct_len)
        out += [
            sep,
            "\n\t{name}{hold}{pct_str}{tgt_pct}".format(
                name="Total".ljust(ac_len),
                hold=tot_hold,
                pct_str=tot_pct,
                tgt_pct="100%"
            ),
        ]
        out.append('\n')
        return ''.join(out)

    def add_asset_class(self, asset_class):
        """
        Adds the given asset class to this portfolio.
        """
        self.asset_classes[asset_class.name] = asset_class
        if asset_class.holdings:
            if self.total_holdings:
                self.total_holdings += asset_class.holdings
            else:
                self.total_holdings = asset_class.holdings

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

    def get_asset_class_percentage(self, asset_class_name):
        """
        Returns the percentage of the portfolio invested in the given asset
        class.
        """
        ac = self.get_asset_class(asset_class_name)
        return ac.holdings / self.total_holdings

    def get_asset_class_target_holdings(self, asset_class_name):
        """
        Returns the amount that should be invested in the given asset class.
        """
        ac = self.get_asset_class(asset_class_name)
        return self.total_holdings * ac.target_percentage

    def get_asset_class_target_deviation(self, asset_class_name):
        """
        Returns the deviation between the target and the achieved amount
        invested in the given asset class.
        """
        ac = self.get_asset_class(asset_class_name)
        target = self.get_asset_class_target_holdings(asset_class_name)
        return ac.holdings - target

    def get_asset_class_budgets(self, deposit):
        """
        Returns the spending budgets for the asset classes in the portfolio
        for a given deposit.
        """
        # Temporarily pretend our portfolio has deposit's value added to it
        self.total_holdings += deposit
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
        self.total_holdings -= deposit
        return ac_budgets

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

    def get_security_percentage(self, security_id):
        """
        Returns the percentage of this portfolio invested in the given
        security.
        """
        sec = get_asset_class_for_security(security_id).get_security()
        return sec.holdings / self.total_holdings

    def update(self, robinhood_holdings):
        """
        Updates this portfolio (and its underlying asset classes and
        securities) with the given Robinhood holdings.
        """
        for rh in robinhood_holdings:
            # Add equity in this holding to portfolio total
            if self.total_holdings:
                self.total_holdings += rh.equity
            else:
                self.total_holdings = rh.equity

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
            for purchase in ac_purchases:
                deposit.add_purchase(ac.name, purchase)
                ac_total += purchase.total
            rollover = final_budget - ac_total
        return deposit
