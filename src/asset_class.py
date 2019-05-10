# Ricky Galliani
# Minerva
# asset_class.py

from purchase import Purchase
from robinhood_holding import RobinhoodHolding

import json

class AssetClass:

    def __init__(self,
                 name,
                 target_percentage,
                 holdings=None):
        self.name = name
        self.target_percentage = target_percentage
        self.holdings = 0.0
        self.securities = {}

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        ac = {
            'name': self.name,
            'target_percentage': self.target_percentage,
            'securities': [s.to_dict() for s in self.securities.values()]
        }
        if self.holdings:
            ac['holdings'] = self.holdings
        return ac

    def add_security(self, security):
        """
        Adds the given security to this asset class.
        """
        self.securities[security.id] = security
        if security.holdings:
            self.holdings += security.holdings

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

    def plan_deposit(self, deposit):
        """
        Uses a Dynamic Program to determine how to optimally spend the budget
        on the given securities. This is the well known Unbounded Knapsack
        problem.
        """
        def no_purchases():
            return [
                Purchase(s.id, s.name, s.price, 0)
                for s in self.securities.values()
            ]

        deposit_cents = int(deposit * 100)
        if deposit_cents < 0:
            return no_purchases()

        securities_cents = [s.with_cents() for s in self.securities.values()]

        # Purchase at T[i] maximizes expenditure with budget i
        T = [0 for x in range(deposit_cents + 1)]
        for i in range(deposit_cents + 1):
            for j, s in enumerate(securities_cents):
                j_id = s.id
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
            for j, sec in enumerate(securities_cents):
                j_price = sec.price
                # If buying security j brought us to optimal expenditures at
                # budget i
                if T[exp_i - j_price] + j_price == exp_i:
                    prev = purchases[j]
                    purchases[j] = Purchase(
                        prev.security_id,
                        prev.security_name,
                        prev.price,
                        prev.quantity + 1
                    )
                    break
            i = exp_i - securities_cents[j].price + 1
        return purchases
