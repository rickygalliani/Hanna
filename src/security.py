# Ricky Galliani
# Hanna
# src/security.py

from src.robinhood_holding import RobinhoodHolding

import json


class Security:

    def __init__(self, security_id, name=None, price=None):
        self.__id = security_id  # no setter method
        self.set_name(name)
        self.set_price(price)

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def set_name(self, new_name):
        self.__name = new_name

    def set_price(self, new_price):
        self.__price = new_price

    def to_dict(self):
        return {
            'id': self.get_id(),
            'name': self.get_name(),
            'price': self.get_price()
        }

    def with_cents(self):
        """
        Returns this security but with monetary amounts represented in cents,
        not dollars.
        """
        return Security(
            self.get_id(), 
            self.get_name(),
            int(self.get_price() * 100)
        )

    def update(self, robinhood_holding):
        """
        Updates this security with given Robinhood holding data.
        """
        assert(isinstance(robinhood_holding, RobinhoodHolding))
        self.set_name(robinhood_holding.name)
        self.set_price(robinhood_holding.price)
