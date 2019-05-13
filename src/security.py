# Ricky Galliani
# Hanna
# src/security.py

from src.robinhood_holding import RobinhoodHolding

import json

class Security:

    def __init__(self, security_id, name=None, price=None):
        self.id = security_id
        self.name = name
        self.price = price  

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

    def with_cents(self):
        """
        Returns this security but with monetary amounts represented in cents,
        not dollars.
        """
        return Security(self.id, self.name, int(self.price * 100))

    def update(self, robinhood_holding):
        """
        Updates this security with given Robinhood holding data.
        """
        assert(isinstance(robinhood_holding, RobinhoodHolding))
        self.name = robinhood_holding.name
        self.price = robinhood_holding.price
