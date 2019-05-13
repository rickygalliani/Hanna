# Ricky Galliani
# Hanna
# src/asset_class.py

from src.holding import Holding
from src.purchase import Purchase
from src.robinhood_holding import RobinhoodHolding

import json

class AssetClass:

    def __init__(self, name, target_percentage):
        self.name = name
        self.target_percentage = target_percentage
        self.securities = {}  # Financial products in asset class
        self.holdings = {}  # Actual holdings of the above financial products
        self.value = 0.0

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        secs = dict([(d, s.to_dict()) for (d, s) in self.securities.items()])
        hols = dict([(d, h.to_dict()) for (d, h) in self.holdings.items()])
        ac = {
            'name': self.name,
            'target_percentage': self.target_percentage,
            'securities': secs,
            'holdings': hols,
            'value': self.value
        }
        return ac

    def add_value(self, new_value):
        """
        Adds the given value to this asset class.
        """
        if self.value:
            self.value += new_value
        else:
            self.value = new_value

    def add_security(self, security):
        """
        Adds the given security to this asset class.
        """
        if security.id not in self.securities:
            self.securities[security.id] = security
        else:
            if security.name:
                self.securities[security.id].name = security.name
            if security.price:
                self.securities[security.id].price = security.price

    def contains_security(self, security_id):
        """
        Returns True if this asset class contains the given security.
        """
        return security_id in self.securities

    def get_security(self, security_id):
        """
        Returns the security for the given security id.
        """
        if security_id in self.securities:
            return self.securities[security_id]
        else:
            raise Exception(
                "{} is not in the '{}' asset class's securities.".format(
                    security_id,
                    self.name
                )
            )

    def add_holding(self, security, num_shares):
        """
        Adds num_shares of the given security to the holdings of this asset
        class.
        """
        value = num_shares * security.price
        self.add_value(value)
        if security.id not in self.holdings:
            holding = Holding(security.id, num_shares, value)
            self.holdings[security.id] = holding
        else:
            self.holdings[security.id].buy(num_shares, security.price)

    def contains_holding(self, security_id):
        """
        Returns True if this asset class contains a holding of the given
        security.
        """
        return security_id in self.holdings

    def get_holding(self, security_id):
        """
        Returns this asset class's holdings of the given security.
        """
        if security_id in self.holdings:
            return self.holdings[security_id]
        else:
            raise Exception(
                "{} is not in the '{}' asset class's holdings.".format(
                    security_id,
                    self.name
                )
            )

    def update(self, robinhood_holding):
        """
        Updates this asset class with the given Robinhood holding.
        """
        assert(isinstance(robinhood_holding, RobinhoodHolding))
        self.value += robinhood_holding.equity
        sec_id = robinhood_holding.id
        security = self.get_security(sec_id)
        security.update(robinhood_holding)
        if sec_id in self.holdings:
            holding = self.get_holding(sec_id)
            holding.update(robinhood_holding)
        else:
            self.holdings[sec_id] = Holding(
                sec_id,
                robinhood_holding.quantity,
                robinhood_holding.equity
            )

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
                        prev.num_shares + 1,
                        prev.price
                    )
                    break
            i = exp_i - securities_cents[j_id].price + 1
        return purchases
