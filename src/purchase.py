# Ricky Galliani
# Hanna
# src/purchase.py

import json

class Purchase:

    def __init__(self, security_id, security_name, num_shares, price):
        self.security_id = security_id
        self.security_name = security_name
        self.num_shares = num_shares
        self.price = price
        self.cost = self.num_shares * self.price

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'security_id': self.security_id,
            'security_name': self.security_name,
            'num_shares': self.num_shares,
            'price': self.price,
            'cost': self.cost
        }

    def for_display(self):
        return ("\n\t{}"
                "\n\t\t- Quantity: {}"
                "\n\t\t- Price: ${:,.2f}"
                "\n\t\t- Cost: ${:,.2f}""".format(
                self.security_name,
                self.num_shares,
                self.price,
                self.cost
            )
        )