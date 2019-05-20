# Ricky Galliani
# Hanna
# src/asset_class.py

from src.holding import Holding
from src.purchase import Purchase

import json


class AssetClass:

    def __init__(self, name, target_percentage):
        self.__name = name
        self.__target_percentage = target_percentage
        self.__securities = {}
        self.__holdings = {}
        self.__value = 0.0

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def get_name(self):
        return self.__name

    def get_target_percentage(self):
        return self.__target_percentage

    def get_securities(self):
        return self.__securities.values()

    def get_holdings(self):
        return self.__holdings.values()

    def get_value(self):
        return self.__value

    def to_dict(self):
        ac = {
            'name': self.get_name(),
            'target_percentage': self.get_target_percentage(),
            'securities': [s.to_dict() for s in self.get_securities()],
            'holdings': [h.to_dict() for h in self.get_holdings()],
            'value': self.get_value()
        }
        return ac

    def add_value(self, new_value):
        """
        Adds the given value to this asset class.
        """
        if self.__value:
            self.__value += new_value
        else:
            self.__value = new_value

    def contains_security(self, security_id):
        """
        Returns True if this asset class contains the given security.
        """
        return security_id in self.__securities

    def add_security(self, security):
        """
        Adds the given security to this asset class.
        """
        sec_id = security.get_id()
        if not self.contains_security(sec_id):
            self.__securities[sec_id] = security
        else:
            raise Exception(
                "{} was already added to the '{}' asset class.".format(
                    sec_id,
                    self.get_name()
                )
            )  

    def add_holding(self, holding):
        """
        Adds the given holding to this asset class.

        1) HS / HH -> user already added holding and security, raise error
        2) !HS / HH -> impossible in theory, raise error
        3) HS / !HH -> good use case
        4) !HS / !HH -> user needs to add security first, raise error
        """
        sec_id = holding.get_security().get_id()
        has_security = self.contains_security(sec_id)
        has_holding = self.contains_holding(sec_id)
        if has_security and not has_holding:
            self.__holdings[sec_id] = holding
        elif not has_security:
            m = "Must add {} to '{}' before adding it as a holding."
            raise Exception(m.format(security_id, self.get_name()))
        else:
            m = "A holding for {} was already added to the '{}' asset class."
            raise Exception(m.format(security_id, self.get_name()))  

    def get_security(self, security_id):
        """
        Returns the security for the given security id.
        """
        if self.contains_security(security_id):
            return self.__securities[security_id]
        else:
            m = "{} is not in the '{}' asset class's securities."
            raise Exception(m.format(security_id, self.get_name()))

    def contains_holding(self, security_id):
        """
        Returns True if this asset class contains a holding of the given
        security.
        """
        return security_id in self.__holdings

    def get_holding(self, security_id):
        """
        Returns this asset class's holdings of the given security.
        """
        if self.contains_holding(security_id):
            return self.__holdings[security_id]
        else:
            m = "{} is not in the '{}' asset class's holdings."
            raise Exception(m.format(security_id, self.get_name()))

    def update_security(self, security_id, security_info):
        """
        Updates the given security with name and latest price data.
        """
        sec = self.get_security(security_id)
        sec.set_name(security_info['name'])
        sec.set_price(security_info['price'])

    def update_holding(self, security, holding_info):
        """
        Updates the given holding with new holding data.
        """
        hol_shares = holding_info['quantity']
        hol_value = holding_info['equity']
        self.__value += hol_value
        sec_id = holding_info['id']
        if self.contains_holding(sec_id):
            hol = self.get_holding(sec_id)
            hol.set_num_shares(hol_shares)
            hol.set_value(hol_value)
        else:
            self.__holdings[sec_id] = Holding(security, hol_shares, hol_value)

    def buy(self, security, num_shares):
        """
        Adds num_shares of the given security to the holdings of this asset
        class.
        """
        value = num_shares * security.get_price()
        self.add_value(value)
        sec_id = security.get_id()
        if not self.contains_holding(sec_id):
            self.__holdings[sec_id] = Holding(security, num_shares, value)
        else:
            self.__holdings[sec_id].buy(num_shares, security.get_price())

    def plan_purchases(self, budget):
        """
        Uses a Dynamic Program to determine how to optimally spend the budget
        on the asset class's securities. This is the well known Unbounded
        Knapsack problem.
        """
        def no_purchases():
            return dict([
                (s.get_id(), Purchase(s, 0))
                for s in self.get_securities() if not s.get_buy_restricted()
            ])

        budget_cents = int(budget * 100)
        if budget_cents < 0:
            return no_purchases()

        securities_cents = dict([
            (s.get_id(), s.with_cents())
            for s in self.get_securities() if not s.get_buy_restricted()
        ])

        # Purchase at T[i] maximizes expenditure with budget i
        T = [0 for x in range(budget_cents + 1)]
        for i in range(budget_cents + 1):
            for j, (j_id, s) in enumerate(securities_cents.items()):
                j_price = s.get_price()
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
                j_price = sec_j.get_price()
                # If buying security j brought us to optimal expenditures at
                # budget i
                if T[exp_i - j_price] + j_price == exp_i:
                    prev = purchases[j_id]
                    purchases[j_id] = Purchase(prev.get_security(),
                                               prev.get_num_shares() + 1)
                    break
            i = exp_i - securities_cents[j_id].get_price() + 1
        return purchases
