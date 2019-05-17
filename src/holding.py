# Ricky Galliani
# Hanna
# src/holdingclass Security:

import json


class Holding:

    def __init__(self, security_id, num_shares, value):
        self.__id = security_id
        self.__num_shares = num_shares
        self.__value = value

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def get_id(self):
        return self.__id

    def get_num_shares(self):
        return self.__num_shares

    def get_value(self):
        return self.__value

    def set_num_shares(self, num_shares):
        self.__num_shares = num_shares

    def set_value(self, value):
        self.__value = value

    def to_dict(self):
        return {
            'id': self.get_id(),
            'num_shares': self.get_num_shares(),
            'value': self.get_value()
        }

    def buy(self, num_shares, price):
        """
        Buys the specified quantity of this holding at the specified price,
        updating the state of this security.
        """
        self.set_num_shares(self.get_num_shares() + num_shares)
        self.set_value(self.get_value() + price * num_shares)
