# Ricky Galliani
# Hanna
# src/purchase.py

import json


class Purchase:

    def __init__(self, security_id, security_name, num_shares, price):
        self.__security_id = security_id
        self.__security_name = security_name
        self.__num_shares = num_shares
        self.__price = price
        self.__cost = self.__num_shares * self.__price

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def get_security_id(self):
        return self.__security_id

    def get_security_name(self):
        return self.__security_name

    def get_num_shares(self):
        return self.__num_shares

    def get_price(self):
        return self.__price

    def get_cost(self):
        return self.__cost

    def to_dict(self):
        return {
            'security_id': self.get_security_id(),
            'security_name': self.get_security_name(),
            'num_shares': self.get_num_shares(),
            'price': self.get_price(),
            'cost': self.get_cost()
        }
