# Ricky Galliani
# Hanna
# src/holdingclass Security:

from src.robinhood_holding import RobinhoodHolding

import json

class Holding:

    def __init__(self, security_id, num_shares, value):
        self.id = security_id
        self.num_shares = num_shares
        self.value = value

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'num_shares': self.num_shares,
            'value': self.value
        }

    def add_shares(self, num_shares):
        """
        Adds the given number of shares to this holding.
        """
        if self.num_shares:
            self.num_shares += num_shares
        else:
            self.num_shares = num_shares

    def add_value(self, new_value):
        """
        Adds the given value to this holding.
        """
        if self.value:
            self.value += new_value
        else:
            self.value = new_value

    def update(self, robinhood_holding):
        """
        Updates this holding with given Robinhood holding data.
        """
        assert(isinstance(robinhood_holding, RobinhoodHolding))
        self.name = robinhood_holding.name
        self.num_shares = robinhood_holding.quantity
        self.value = robinhood_holding.equity

    def buy(self, num_shares, price):
        """
        Buys the specified quantity of this holding at the specified price,
        updating the state of this security.
        """
        self.add_shares(num_shares)
        self.add_value(price * num_shares)
