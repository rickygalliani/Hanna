# Ricky Galliani
# Hanna
# src/security.py

import json


class Security:

    def __init__(self,
                 security_id,
                 symbol,
                 name=None,
                 price=None,
                 buy_restricted=1):
        if price and price <= 0:
            raise Exception(
                "Must pass a positive price (or None) to instantiate a Security"
            )
        self.__id = security_id
        self.__symbol = symbol
        self.__name = name
        self.__price = price
        self.__buy_restricted = buy_restricted
        if price:
            self.__purchase_buffer = 0.15 * price
        else:
            self.__purchase_buffer = 0.0

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def get_id(self):
        return self.__id

    def get_symbol(self):
        return self.__symbol

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_purchase_buffer(self):
        return self.__purchase_buffer

    def get_buy_restricted(self):
        return self.__buy_restricted

    def set_name(self, name):
        self.__name = name

    def set_price(self, price):
        if price <= 0:
            raise Exception("Security price must be positive")
        self.__price = price
        self.__purchase_buffer = 0.15 * price

    def restrict_buy(self):
        self.__buy_restricted = 1

    def enable_buy(self):
        self.__buy_restricted = 0

    def to_dict(self):
        return {
            'id': self.get_id(),
            'symbol': self.get_symbol(),
            'name': self.get_name(),
            'price': self.get_price(),
            'purchase_buffer': self.get_purchase_buffer(),
            'buy_restricted': self.get_buy_restricted()
        }

    def with_cents(self):
        """
        Returns this security but with monetary amounts represented in cents,
        not dollars.
        """
        return Security(
            self.get_id(),
            self.get_symbol(),
            self.get_name(),
            int(self.get_price() * 100),
            self.get_buy_restricted()
        )
