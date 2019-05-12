# Ricky Galliani
# Hanna
# src/asset_class.py

from src.purchase import Purchase
from src.robinhood_holding import RobinhoodHolding

import json

class AssetClass:

    def __init__(self,
                 name,
                 target_percentage):
        self.name = name
        self.target_percentage = target_percentage
        self.holdings = 0.0
        self.securities = {}

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        secs = dict([(d, s.to_dict()) for (d, s) in self.securities.items()])
        ac = {
            'name': self.name,
            'target_percentage': self.target_percentage,
            'securities': secs,
            'holdings': self.holdings
        }
        return ac

    def add_holdings(self, new_holdings):
        """
        Adds the given holdings to this asset class.
        """
        if self.holdings:
            self.holdings += new_holdings
        else:
            self.holdings = new_holdings

    def add_security(self, security):
        """
        Adds the given security to this asset class.
        """
        if security.quantity and security.price:
            self.add_holdings(security.price * security.quantity)
        if security.id not in self.securities:
            self.securities[security.id] = security
        elif security.quantity and security.price:
            self.securities[security.id].buy(security.quantity, security.price)

    def contains_security(self, security_id):
        """
        Returns whether this asset class contains the given security.
        """
        return security_id in self.securities

    def get_security(self, security_id):
        """
        Returns the Security object for the given security id.
        """
        if security_id in self.securities:
            return self.securities[security_id]
        else:
            raise Exception("{} is not in the '{}' asset class.".format(
                security_id,
                self.name
            ))

    def update(self, robinhood_holding):
        """
        Updates this asset class with the given Robinhood holding.
        """
        assert(isinstance(robinhood_holding, RobinhoodHolding))
        self.holdings += robinhood_holding.equity
        security = self.get_security(robinhood_holding.id)
        security.update(robinhood_holding)

    def plan_deposit(self, budget):
        """
        Uses a Dynamic Program to determine how to optimally spend the budget
        on the asset class's securities. This is the well known Unbounded
        Knapsack problem.
        """
        def no_purchases():
            return dict([
                (s_id, Purchase(s.id, s.name, 0, s.price))
                for (s_id, s) in self.securities.items()
            ])

        budget_cents = int(budget * 100)
        if budget_cents < 0:
            return no_purchases()

        securities_cents = dict([
            (s_id, s.with_cents()) for (s_id, s) in self.securities.items()
        ])

        # Purchase at T[i] maximizes expenditure with budget i
        T = [0 for x in range(budget_cents + 1)]
        for i in range(budget_cents + 1):
            for j, (j_id, s) in enumerate(securities_cents.items()):
                j_price = s.price
                # Check if budget of i allows for a purchase of j
                if j_price <= i:
                    # Check if buying it increases expenditures
                    cur_exp = T[i]
                    new_exp = T[i - j_price] + j_price
                    if new_exp > cur_exp:
                        # Optimal purchases at budget i now includes buying j
                        T[i] = new_exp

        # Backtrack thru T to construct set of optimal purchases
        purchases = no_purchases()
        i = len(T) - 1
        while T[i]:
            exp_i = T[i]  # Optimal amount spent at budget i
            # Find last security purchased
            for j, (j_id, sec_j) in enumerate(securities_cents.items()):
                j_price = sec_j.price
                # If buying security j brought us to optimal expenditures at
                # budget i
                if T[exp_i - j_price] + j_price == exp_i:
                    prev = purchases[j_id]
                    purchases[j_id] = Purchase(
                        prev.security_id,
                        prev.security_name,
                        prev.quantity + 1,
                        prev.price
                    )
                    break
            i = exp_i - securities_cents[j_id].price + 1
        return purchases
