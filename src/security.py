# Ricky Galliani
# Hanna
# src/security.py

from src.robinhood_holding import RobinhoodHolding

import json

class Security:

    def __init__(self,
                 security_id,
                 name=None,
                 quantity=None,
                 price=None,
                 holdings=None):
        """
        Security initialization:
          1) sec = Security('sec')
          2) sec = Security('sec', 'sec_name', 1, 25.0, 100.0)
        """
        def all_undefined():
            return not any([name, quantity, price, holdings])

        def all_defined():
            return all([name, quantity, price, holdings])
        assert(all_undefined or all_defined())
        self.id = security_id
        self.name = name
        self.quantity = quantity
        self.price = price
        self.holdings = holdings     

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'quantity': self.quantity,
            'price': self.price,
            'holdings': self.holdings
        }

    def with_cents(self):
        """
        Returns this Security but with dollar amounts represented in cents,
        not dollars.
        """
        return Security(
            self.id,
            self.name,
            self.quantity,
            int(self.price * 100),
            self.holdings
        )

    def add_shares(self, num_shares):
        """
        Adds the given number of shares to this security.
        """
        if self.quantity:
            self.quantity += num_shares
        else:
            self.quantity = num_shares

    def add_holdings(self, new_holdings):
        """
        Adds the given holdings to this security.
        """
        if self.holdings:
            self.holdings += new_holdings
        else:
            self.holdings = new_holdings

    def update(self, robinhood_holding):
        """
        Updates this security with given Robinhood holding data.
        """
        assert(isinstance(robinhood_holding, RobinhoodHolding))
        self.name = robinhood_holding.name
        self.quantity = robinhood_holding.quantity
        self.price = robinhood_holding.price
        self.holdings = robinhood_holding.equity

    def buy(self, quantity, price):
        """
        Buys the specified quantity of this security at the specified price,
        updating the state of this security.
        """
        self.price = price
        self.add_shares(quantity)
        self.add_holdings(price * quantity)
