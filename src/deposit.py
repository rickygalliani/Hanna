# Ricky Galliani
# Hanna
# src/deposit.py

from src.purchase import Purchase

import json

class Deposit:

    def __init__(self):
        self.total = 0.0  # Total spent on all purchases in deposit
        self.purchases = {}

    def __repr__(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        return {
            'purchases': dict(
                [(ac, [p.to_dict() for p in ps])
                for (ac, ps) in self.purchases.items()]
            )
        }

    def for_display(self):
        out = ['\n\nPurchases:']
        ac_purchases = sorted(
            self.purchases.items(),
            key=lambda x: self.get_asset_class_expenditures(x[0]),
            reverse=True
        )
        for asset_class_name, purchases in ac_purchases:
            out.append("\n\n{}".format(asset_class_name))
            for purchase in purchases:
                out.append(purchase.for_display())
        return ''.join(out)

    def add_purchase(self, asset_class_name, purchase):
        """
        Adds purchases related to an asset class to this deposit.
        """
        if asset_class_name in self.purchases:
            self.purchases[asset_class_name] += [purchase]
        else:
            self.purchases[asset_class_name] = [purchase]
        self.total += purchase.total

    def get_asset_class_expenditures(self, asset_class_name):
        """
        Returns the total expenditures in the given asset class.
        """
        ps = self.purchases[asset_class_name]
        return sum(p.total for p in ps)
