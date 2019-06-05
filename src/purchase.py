# Ricky Galliani
# Hanna
# src/purchase.py

import json


class Purchase:

    def __init__(self, security, num_shares):
        if not security.get_price():
            raise Exception(
                "Purchase must be instantiated with a Security "
                "that has a non-None price"
            )
        if num_shares <= 0:
            raise Exception(
                "Purchase must be instantiated with num_shares >= 0"
            )
        self.__security = security
        self.__num_shares = num_shares
        self.__cost = self.__security.get_price() * self.__num_shares

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def get_security(self):
        return self.__security

    def get_num_shares(self):
        return self.__num_shares

    def get_cost(self):
        return self.__cost

    def to_dict(self):
        return {
            'security': self.get_security().to_dict(),
            'num_shares': self.get_num_shares(),
            'cost': self.get_cost()
        }
