# Ricky Galliani
# Hanna
# src/purchase.py

import json

class Purchase:

    def __init__(self, security_id, security_name, price, quantity):
        self.security_id = security_id
        self.security_name = security_name
        self.price = price
        self.quantity = quantity
        self.total = self.price * self.quantity

    def __eq__(self, other):
        return self.to_dict() == other.to_dict()

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'security_id': self.security_id,
            'security_name': self.security_name,
            'price': self.price,
            'quantity': self.quantity,
            'total': self.total
        }

    def for_display(self):
        return ("\n\t{}"
                "\n\t\t- Quantity: {}"
                "\n\t\t- Price: ${:,.2f}"
                "\n\t\t- Total: ${:,.2f}""".format(
                self.security_name,
                self.quantity,
                self.price,
                self.total
            )
        )